class Map:
    def __init__(self, pyboy):
        self.pyboy = pyboy

    def get_map_dimensions(self):
        '''
        return: Tuple of dimensions (width, height)
        '''
        width = self.pyboy.memory[0xD369]
        height = self.pyboy.memory[0xD368]

        return (width, height)

    def get_map_id(self):
        return self.pyboy.memory[0xD35E]

    def get_map_data(self):
        '''
        Combines all other methods.

        return: Dictionary
        '''

        map_data = {}

        map_data['ID'] = self.get_map_id()
        map_data['Dimensions'] = self.get_map_dimensions()

        return map_data
