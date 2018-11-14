# MIT License
# 
# Copyright (c) 2018 Peter Allin
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pygame
import random
import time


class Player:
    def __init__(self, rect, area):
        self.rect = rect
        self.speed_pixels_per_draw = 2
        self.area = area
        self.alive = True

    def move(self, player_input):
        if player_input.down and self.rect.bottom < self.area.bottom:
            self.rect.y = self.rect.y + self.speed_pixels_per_draw
        if player_input.up and self.rect.top > self.area.top:
            self.rect.y = self.rect.y - self.speed_pixels_per_draw
        if player_input.right and self.rect.right < self.area.right:
            self.rect.x = self.rect.x + self.speed_pixels_per_draw
        if player_input.left and self.rect.left > self.area.left:
            self.rect.x = self.rect.x - self.speed_pixels_per_draw


class PlayerShot:
    def __init__(self, rect):
        self.rect = rect
        self.speed_pixels_per_draw = 5

    def update(self):
        self.rect.x = self.rect.x + self.speed_pixels_per_draw


class AlienShot:
    def __init__(self, rect, speed_x, speed_y):
        self.rect = rect
        self.x = rect.x
        self.y = rect.y
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.x = self.x + self.speed_x
        self.rect.x = self.x
        self.y = self.y + self.speed_y
        self.rect.y = self.y


class Alien:
    def __init__(self, rect, movement_area, extra_speed):
        self.rect = rect
        self.movement_area = movement_area
        self.speed_pixels_per_draw = 1 + extra_speed
        self.moving_left = True

    def update(self):
        if self.rect.left <= self.movement_area.left:
            self.moving_left = False

        if self.rect.right >= self.movement_area.right and not self.moving_left:
            self.moving_left = True

        if self.moving_left:
            self.rect.x = self.rect.x - self.speed_pixels_per_draw
        else:
            self.rect.x = self.rect.x + self.speed_pixels_per_draw


class PlayerInput:
    def __init__(self):
        self.stop = False
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.fire = False

    def update(self):
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                self.stop = True

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_a:
                    self.left = True
                if e.key == pygame.K_d:
                    self.right = True
                if e.key == pygame.K_s:
                    self.down = True
                if e.key == pygame.K_w:
                    self.up = True
                if e.key == pygame.K_RETURN:
                    self.fire = True

            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_a:
                    self.left = False
                if e.key == pygame.K_d:
                    self.right = False
                if e.key == pygame.K_s:
                    self.down = False
                if e.key == pygame.K_w:
                    self.up = False
                if e.key == pygame.K_RETURN:
                    self.fire = False


class Graphics:
    def __init__(self):
        self.player = pygame.image.load("player.png").convert_alpha()
        self.player_shot = pygame.image.load("basic_shot.png").convert_alpha()
        self.alien = pygame.image.load("enemy1.png").convert_alpha()
        self.alien_shot = pygame.image.load("enemy1_shot.png").convert_alpha()
        self.status_font = pygame.font.Font(None, 40)


class GameState:
    def __init__(self, graphics, game_area):
        self.graphics = graphics
        self.game_area = game_area
        player_center = (game_area.width // 2, game_area.height // 2)
        player_rect = graphics.player.get_rect(center=player_center)
        self.player = Player(player_rect, game_area)
        self.player_shots = []
        self.has_shot = False
        self.wave_number = 0
        self.aliens = make_wave(graphics, game_area, self.wave_number)
        self.alien_shots = []
        self.lives = 2
        self.time_of_death = 0

    def update(self, player_input, graphics):
        if not self.player.alive and self.lives > 0 and time.time() - self.time_of_death > 2:
            self.alien_shots = []
            self.aliens = make_wave(graphics, self.game_area, self.wave_number)
            self.player.rect.midleft = (0, self.game_area.height // 2)
            self.player.x = self.player.rect.x
            self.player.y = self.player.rect.y
            self.player.alive = True
            self.lives = self.lives - 1

        if not self.player.alive and self.lives == 0 and time.time() - self.time_of_death > 2:
            pygame.quit()
            exit()

        self.player.move(player_input)


        may_fire = not self.has_shot and self.player.alive
        if player_input.fire and may_fire:
            shot_coord = self.player.rect.midright
            new_shot = PlayerShot(graphics.player_shot.get_rect(center=shot_coord))
            self.player_shots.append(new_shot)
            self.has_shot = True
        elif not player_input.fire:
            self.has_shot = False

        for shot in self.player_shots:
            shot.rect.x = shot.rect.x + shot.speed_pixels_per_draw
        self.reap_outsiders(self.player_shots)

        if len(self.aliens) == 0:
            self.wave_number = self.wave_number + 1
            self.aliens = make_wave(graphics, self.game_area, self.wave_number)

        for alien in self.aliens:
            alien.update()

            if random.randint(1, 10000) > 9990:
                center = alien.rect.center
                rect = self.graphics.alien_shot.get_rect(center=center)
                if alien.rect.left < self.player.rect.right:
                    direction_x = 1
                else:
                    direction_x = -1
                if alien.rect.top < self.player.rect.bottom:
                    direction_y = 1
                else:
                    direction_y = -1

                shot = AlienShot(rect, direction_x * 5, random.uniform(-1 + 0.8 * direction_y,
                                                                       1 + 0.8 * direction_y))
                self.alien_shots.append(shot)

        for shot in self.alien_shots:
            shot.update()
        self.reap_outsiders(self.alien_shots)

        for shot in list(self.player_shots):
            for alien in list(self.aliens):
                if shot.rect.colliderect(alien.rect):
                    if shot in self.player_shots:
                        self.player_shots.remove(shot)
                    if alien in self.aliens:
                        self.aliens.remove(alien)

        for shot in list(self.alien_shots):
            if shot.rect.colliderect(self.player.rect) and self.player.alive:
                self.player.alive = False
                self.time_of_death = time.time()

    def reap_outsiders(self, objects):
        for obj in list(objects):
            if not self.game_area.colliderect(obj.rect):
                objects.remove(obj)


def make_alien(graphics, game_area, x, y, extra_speed):
    width = game_area.width
    height = game_area.height
    alien_rect = graphics.alien.get_rect(center=(width + x, height // 2 + y))
    alien = Alien(alien_rect, game_area, extra_speed)
    return alien


def make_wave(graphics, game_area, wave_number):
    extra_speed = wave_number // 3

    if wave_number % 3 == 0:
        return [make_alien(graphics, game_area, 10, 0, extra_speed),
                make_alien(graphics, game_area, 100, 0, extra_speed),
                make_alien(graphics, game_area, 200, 0, extra_speed),
                make_alien(graphics, game_area, 300, 0, extra_speed),
                make_alien(graphics, game_area, 400, 0, extra_speed)]

    elif wave_number % 3 == 1:
        return [make_alien(graphics, game_area, 10, 0, extra_speed),
                make_alien(graphics, game_area, 100, 50, extra_speed),
                make_alien(graphics, game_area, 100, -50, extra_speed),
                make_alien(graphics, game_area, 200, 100, extra_speed),
                make_alien(graphics, game_area, 200, -100, extra_speed)]
    else:
        return [make_alien(graphics, game_area, 10, 0, extra_speed),
                make_alien(graphics, game_area, 100, -50, extra_speed),
                make_alien(graphics, game_area, 100, 0, extra_speed),
                make_alien(graphics, game_area, 100, 50, extra_speed),
                make_alien(graphics, game_area, 200, -100, extra_speed),
                make_alien(graphics, game_area, 200, -50, extra_speed),
                make_alien(graphics, game_area, 200, 0, extra_speed),
                make_alien(graphics, game_area, 200, 50, extra_speed),
                make_alien(graphics, game_area, 200, 100, extra_speed)]


def paint_screen(window, game_state, graphics):
    window.fill((0, 0, 0))
    if game_state.player.alive:
        window.blit(graphics.player, game_state.player.rect)
    for shot in game_state.player_shots:
        window.blit(graphics.player_shot, shot.rect)
    for alien in game_state.aliens:
        window.blit(graphics.alien, alien.rect)
    for shot in game_state.alien_shots:
        window.blit(graphics.alien_shot, shot.rect)
    lives_text = "Lives: " + str(game_state.lives)
    text_image = graphics.status_font.render(lives_text, True, (150, 150, 150))
    screen_rect = window.get_rect()
    text_rect = text_image.get_rect(topright=screen_rect.topright).move(0, 8)
    window.blit(text_image, text_rect)
    pygame.display.flip()


def main_loop():
    pygame.init()
    screen_width = 800
    screen_height = 600
    window = pygame.display.set_mode((screen_width, screen_height))

    graphics = Graphics()
    game_state = GameState(graphics, window.get_rect())
    player_input = PlayerInput()

    while not player_input.stop:
        pygame.time.delay(5)
        player_input.update()
        game_state.update(player_input, graphics)
        paint_screen(window, game_state, graphics)
    pygame.quit()


main_loop()
