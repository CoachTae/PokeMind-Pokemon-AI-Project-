class Game_Corner:
    def __init__(self, pyboy):
        self.pyboy = pyboy

    def get_game_corner_prizes(self):
        # List of (prize1, prize2, prize3)
        return self.pyboy.memory[0xD13D:0xD13F+1]

    def get_coin_count(self):
        # 2 RAM addresses to get the amount of coins player has
        return sum(self.pyboy.memory[0xD5A4:0xD5A6])

    def get_game_corner_data(self):
        '''
        Gets the information from the other methods and combines them.

        return: Dictionary
        '''

        game_corner_dict = {}

        game_corner_dict['Coins'] = self.get_coin_count()
        game_corner_dict['Prizes'] = self.get_game_corner_prizes()

        return game_corner_dict
