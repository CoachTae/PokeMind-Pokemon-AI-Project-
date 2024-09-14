import PokeDAQS_Support.Byte_Unpacker as Byte_Unpacker
import Constants.Pokemon_IDs as Pokemon_IDs

class PC:
    def __init__(self, pyboy):
        self.pyboy = pyboy

        # Count how many RAM addresses are used for each Pokemon in a party
        # We use the ending and starting addresses for the 1st pokemon
        # 1 added at the end to get to the starting point of the next pokemon
        self.num_addresses = 0xDAB6 - 0xDA96 + 1

    def get_pc_items(self):
        '''
        Gets information on items stored in PC.

        return: List of lists of shape [ID, Quantity]
        '''
        
        all_items = self.pyboy.memory[0xD53B:0xD59F]

        pc_items = []

        i = 0
        while 2*i + 1 < len(all_items):
            ID = all_items[2*i]
            quant = all_items[2*i + 1]

            item_info = [ID, quant]

            pc_items.append(item_info)

            i += 1

        return pc_items

    def get_pokemon_info(self, box_number):
        '''
        box_number is expected to be a value between 0 and 19 (20 total)

        return: Dictionary of values
        '''

        start_address = 0xDA96 + box_number * self.num_addresses

        end_address = 0xDA96 + (box_number + 1) * self.num_addresses

        data = self.pyboy.memory[start_address:end_address]

        poke_data = {}

        game_ID = data[0]
        poke_ID = Pokemon_IDs.Poke_IDs[game_ID]
        poke_data['Pokemon'] = poke_ID
        poke_data['Current HP'] = sum(data[1:3])
        poke_data['Level'] = data[3]
        poke_data['Status'] = data[4]
        poke_data['Types'] = (data[5], data[6])
        poke_data['Moves'] = data[8:12]
        poke_data['Experience'] = data[16] + 255*data[15] + 65025*data[14]
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

        return poke_data
        
    def get_num_box_pokemon(self):
        '''
        Gets number of Pokemon stored in current box.

        return: Integer
        '''
        return self.pyboy.memory[0xDA80]

    def get_box_pokemon(self):
        '''
        Gets dictionaries from the above function for each pokemon in the box.

        return: Tuple of dictionaries
        '''

        box = tuple(self.get_pokemon_info(i) for i in range(20))

        return box

    def get_pc_data(self):
        '''
        Combines the previous functions into a single dictionary.

        return: Dictionary of above values
        '''

        pc_data = {}

        pc_data["Items"] = self.get_pc_items()
        pc_data["Pokemon"] = self.get_box_pokemon()

        return pc_data
    
