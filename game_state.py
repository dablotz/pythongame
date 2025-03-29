# GameState class
class GameState:
    def __init__(self):
        self.player_health = 3
        self.boss_health = 5
        self.game_over = False
        self.level_complete = False

    def player_take_damage(self, amount=1):
        self.player_health -= amount
        if self.player_health <= 0:
            self.player_health = 0
            self.game_over = True

    def boss_take_damage(self, amount=1):
        self.boss_health -= amount
        if self.boss_health <= 0:
            self.boss_health = 0
            self.level_complete = True

    def reset(self):
        self.__init__()