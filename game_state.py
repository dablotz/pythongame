""" 
This module defines the GameState class, which manages the state of the game, 
including player and boss health, and whether the game is over or the level is complete.
"""

class GameState:
    """ GameState class representing the state of the game. """
    def __init__(self):
        """ Initialize the game state with default values. """
        self.player_health = 3
        self.boss_health = 5
        self.game_over = False
        self.level_complete = False

    def player_take_damage(self, amount=1):
        """ Reduce player health by the specified amount. """
        self.player_health -= amount
        if self.player_health <= 0:
            self.player_health = 0
            self.game_over = True

    def boss_take_damage(self, amount=1):
        """ Reduce boss health by the specified amount. """
        self.boss_health -= amount
        if self.boss_health <= 0:
            self.boss_health = 0
            self.level_complete = True

    def reset(self):
        """ Reset the game state to the initial values. """
        self.player_health = 3
        self.boss_health = 5
        self.game_over = False
        self.level_complete = False
