import sys

class PokeMart:
    def __init__(self, pyboy):
        '''
        Provides the Identifiers of the PokeMart items available.

        return: List of IDs
        '''

        self.pyboy = pyboy

    def get_mart_items(self):
        '''
        Pulls Identifiers for each PokeMart item.

        All items initialize on 0.
        It's possible that 0 is more specifically "no item".

        The following situations are not documented:
        - Do the values update on entering a map or when opening shop?
        - What is the value for not having an item in that slot?

        return: List of IDs
        '''

        try:
            return self.pyboy.memory[0xCF7C:0xCF86]

        except:
            print("Error pulling PokeMart items. See PokeMart.py")
            sys.exit()
