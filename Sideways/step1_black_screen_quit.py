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


class PlayerInput:
    def __init__(self):
        self.stop = False

    def update(self):
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                self.stop = True


def paint_screen(window):
    window.fill((0, 0, 0))
    pygame.display.flip()


def main_loop():
    pygame.init()
    screen_width = 800
    screen_height = 600
    window = pygame.display.set_mode((screen_width, screen_height))

    player_input = PlayerInput()

    while not player_input.stop:
        pygame.time.delay(5)
        player_input.update()
        paint_screen(window)
    pygame.quit()


main_loop()
