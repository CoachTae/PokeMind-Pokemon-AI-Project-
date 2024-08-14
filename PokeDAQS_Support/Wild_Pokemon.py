import Constants.Pokemon_IDs as Pokemon_IDs

class Wild_Pokemon:
    def __init__(self, pyboy):
        self.pyboy = pyboy


    def get_wild_pokemon_data(self):
        '''
        Gets the encounter rate of pokemon in the region,
        the level of each encounter,
        and the "data value" of each encounter.

        Data value I presume is the pokemon ID?

        Data value and level are paired.

        return: Dictionary with an integer encounter rate and tuples of (Value, Level)
        '''
        
        wild_pokemon_data_list = self.pyboy.memory[0xD887:0xD89C]

        wild_pokemon_data = {}

        wild_pokemon_data['Encounter Rate'] = wild_pokemon_data_list[0]

        wild_pokemon_data_list = wild_pokemon_data_list[1:]

        i = 0

        commons = []
        uncommons = []
        rares = []

        while i < 10:
            level = wild_pokemon_data_list[2*i]
            data_value = wild_pokemon_data_list[2*i + 1]
            poke_ID = Pokemon_IDs.Poke_IDs[data_value]
            pokemon_data = (poke_ID, level)

            if i < 4:
                commons.append(pokemon_data)


            elif 4 <= i < 8:
                uncommons.append(pokemon_data)

            elif 8 <= i < 10:
                rares.append(pokemon_data)

            i += 1

        wild_pokemon_data['Common'] = commons
        wild_pokemon_data['Uncommon'] = uncommons
        wild_pokemon_data['Rares'] = rares

        return wild_pokemon_data        
