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


class Player:
    def __init__(self, rect, area):
        self.rect = rect
        self.speed_pixels_per_draw = 2
        self.area = area

    def move(self, player_input):
        if self.rect.right < self.area.right:
            self.rect.x = self.rect.x + self.speed_pixels_per_draw

        if self.rect.bottom < self.area.bottom:
            self.rect.y = self.rect.y + self.speed_pixels_per_draw


class PlayerInput:
    def __init__(self):
        self.stop = False

    def update(self):
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                self.stop = True


class Graphics:
    def __init__(self):
        self.player = pygame.image.load("player.png").convert_alpha()


class GameState:
    def __init__(self, graphics, game_area):
        self.game_area = game_area
        player_center = (game_area.width // 2, game_area.height // 2)
        player_rect = graphics.player.get_rect(center=player_center)
        self.player = Player(player_rect, game_area)

    def update(self, player_input):
        self.player.move(player_input)


def paint_screen(window, game_state, graphics):
    window.fill((0, 0, 0))
    window.blit(graphics.player, game_state.player.rect)
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
        game_state.update(player_input)
        paint_screen(window, game_state, graphics)
    pygame.quit()


main_loop()
