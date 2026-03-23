""" Hazard class """

import pygame

class Hazard: # pylint: disable=too-few-public-methods
    """ Hazard class representing a hazard in the game. """
    def __init__(self, x, y, w, h):
        """ Initialize the hazard with its position and size. """
        self.rect = pygame.Rect(x, y, w, h)
