import pygame
from constants import *


class Button(pygame.sprite.Sprite):

    # Constructor
    def __init__(self, pos_tup, text, font_render, color=WHITE, active_condition=True, hovered=False):
        super(Button, self).__init__()
        self.text = text  # the text of the button
        self.color = color  # the text's color
        self.x = pos_tup[0]  # the position of the button
        self.y = pos_tup[1]
        self.text_surface = font_render.render(text, True, color)
        self.rect = self.text_surface.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.active_condition = active_condition  # at what condition can the button be pressed
        self.hovered = hovered  # is the mouse on the button

    # Getters
    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def get_pos(self):
        return self.rect.x, self.rect.y

    def get_text(self):
        return self.text

    def get_text_surface(self):
        return self.text_surface

    def get_active(self):
        return self.active_condition

    def get_color(self):
        return self.color

    def get_hovered(self):
        return self.hovered

    # Setters
    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def set_color(self, font_render, color):
        self.color = color
        self.text_surface = font_render.render(self.text, True, color)

    def set_text(self, font_render, text):
        self.text = text
        self.text_surface = font_render.render(self.text, True, self.color)
        self.rect = self.text_surface.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def set_active(self, condition):
        self.active_condition = condition

    def set_hovered(self, bool):
        self.hovered = bool

    def is_hovered(self):
        """

        :return: boolean indicating if the mouse is on top of the button
        """
        #  check if the clicks position was in the button
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)
