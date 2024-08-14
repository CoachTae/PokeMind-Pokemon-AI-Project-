import PokeDAQS_Support.Byte_Unpacker as Byte_Unpacker

class Inventory:
    def __init__(self, pyboy):
        self.pyboy = pyboy

    def get_inventory(self):
        '''
        Retrieves items in inventory.

        return: List of tuples of shape (ID, Quantity)
        '''
        
        item_info = self.pyboy.memory[0xD31E:0xD346]

        inventory = []

        i = 0
        while 2*i + 1 < len(item_info):
            ID = item_info[2*i]
            quant = item_info[2*i + 1]

            item_info = (ID, quant)

            inventory.append(item_info)

            
            i += 1

        return inventory


    def get_money(self):
        return sum(self.pyboy.memory[0xD347:0xD34A])

    def get_badges(self):
        '''
        0 = No badge
        1 = Badge

        bit 1 = 1st Gym
        bit 2 = 2nd Gym
        .
        .
        .

        
        return: List of binary integers
        '''
        
        badges_byte = self.pyboy.memory[0xD356]

        badges = Byte_Unpacker.unpack_bits(badges_byte)

        return badges

    def get_inventory_data(self):
        '''
        Compiles the data from the other methods.

        return: Dictionary
        '''

        full_inventory = {}

        full_inventory['Items'] = self.get_inventory()
        full_inventory['Money'] = self.get_money()
        full_inventory['Badges'] = self.get_badges()

        return full_inventory
