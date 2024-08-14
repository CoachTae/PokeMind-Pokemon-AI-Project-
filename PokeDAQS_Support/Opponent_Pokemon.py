import PokeDAQS_Support.Byte_Unpacker as Byte_Unpacker
import Constants.Pokemon_IDs as Pokemon_IDs

class Opponent_Pokemon:
    def __init__(self, pyboy):
        '''
        Gets party information for opponent trainer.
        Probably has nothing to do with wild pokemon, but unsure.
        '''
        
        self.pyboy = pyboy

        # Count how many RAM addresses are used for each Pokemon in a party
        # We use the ending and starting addresses for the 1st pokemon
        # 1 added at the end to get to the starting point of the next pokemon
        self.num_addresses = 0xD8CF - 0xD8A4 + 1


    def get_pokemon_info(self, party_number):
        '''
        party_number is expected to be a value between 0 and 5

        return: Dictionary of single pokemon values
        '''

        start_address = 0xD8A4 + party_number * self.num_addresses

        end_address = 0xD8A4 + (party_number + 1) * self.num_addresses

        data = self.pyboy.memory[start_address:end_address]

        poke_data = {}

        game_ID = data[0]
        poke_ID = Pokemon_IDs.Poke_IDs[game_ID]
        poke_data['Pokemon'] = poke_ID
        poke_data['Current HP'] = sum(data[1:3])
        poke_data['Status'] = data[4]
        poke_data['Types'] = (data[5], data[6])
        poke_data['Moves'] = data[8:12]
        poke_data['HP EV'] = sum(data[17:19])

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
    
    def get_opponent_party(self):
        '''
        Pulls party information for the trainer you're currently fighting.

        returns: List of dictionaries from the function above
        '''
        party = tuple(self.get_pokemon_info(i) for i in range(6))

        return party
