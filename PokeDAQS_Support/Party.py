import sys
import PokeDAQS_Support.Byte_Unpacker as Byte_Unpacker
import Constants.Pokemon_IDs as Pokemon_IDs

class Party:
    def __init__(self, pyboy):
        '''
        Pulls all the details about the Pokemon in your party
        '''
        self.pyboy = pyboy

        # Count how many RAM addresses are used for each Pokemon in a party
        # We use the ending and starting addresses for the 1st pokemon
        # 1 added at the end to get to the starting point of the next pokemon
        self.num_addresses = 0xD196 - 0xD16B + 1

    def get_party_count(self):
        # Number of Pokemon in party
        self.count = self.pyboy.memory[0xD163]
        return self.count

    def get_pokemon_info(self, party_number):
        '''
        party_number is expected to be a value between 0 and 5

        return: Dictionary of values
        '''

        start_address = 0xD16B + party_number * self.num_addresses

        end_address = 0xD16B + (party_number + 1) * self.num_addresses

        data = self.pyboy.memory[start_address:end_address]

        poke_data = {}

        game_ID = data[0]
        poke_ID = Pokemon_IDs.Poke_IDs[game_ID]
        poke_data['Pokemon'] = poke_ID
        poke_data['Current HP'] = sum(data[1:3])
        poke_data['Status'] = data[4]
        poke_data['Types'] = (data[5], data[6])
        poke_data['Moves'] = data[8:12]
        poke_data['Experience'] = sum(data[14:17])
        poke_data['HP EV'] = sum(data[17:19])
        poke_data['Attack EV'] = sum(data[19:21])
        poke_data['Defense EV'] = sum(data[21:23])
        poke_data['Speed EV'] = sum(data[23:25])
        poke_data['Special EV'] = sum(data[25:27])

        # Attack and Defense IVs are shared in a single byte
        attack, defense = Byte_Unpacker.byte_divider(data[27], 2, dec=True)
        poke_data['Attack IV'] = attack
        poke_data['Defense IV'] = defense

        # Speed and Special IVs are shared in a single byte
        speed, spec = Byte_Unpacker.byte_divider(data[28], 2, dec=True)
        poke_data['Speed IV'] = speed
        poke_data['Spec IV'] = spec
        
        poke_data['Move PPs'] = data[29:33]
        poke_data['Level'] = data[33]
        poke_data['Max HP'] = sum(data[34:36])
        poke_data['Attack'] = sum(data[36:38])
        poke_data['Defense'] = sum(data[38:40])
        poke_data['Speed'] = sum(data[40:42])
        poke_data['Special'] = sum(data[42:])

        return poke_data

    def get_party(self):
        '''
        Gets dictionaries from the above function for each pokemon in the party.

        return: Tuple of dictionaries
        '''

        party = tuple(self.get_pokemon_info(i) for i in range(6))

        return party

            
            
