class Flags:
    def __init__(self, pyboy):
        self.pyboy = pyboy


    def get_event_flags(self):
        '''
        Gets event flags.
        Values are unknown, but suspect that 0 = False and 1 = True.

        return: List of flags
        '''

        flags = []
        # Missable Objects (flags for every (dis)appearing sprites,
            # like the guard in Cerulean City, or the Pokeballs in Oak's Lab)
        for address in range(0xD5A6, 0xD5C6):
            flags.append(self.pyboy.memory[address])

        # Have Town map?
        flags.append(self.pyboy.memory[0xD5F3])

        # Have Oak's Parcel?
        flags.append(self.pyboy.memory[0xD60D])

        # Safari Zone Time (2 bytes)
        time = sum(self.pyboy.memory[0xD70D:0xD70F])
        flags.append(time)

        # Safari Balls
        flags.append(self.pyboy.memory[0xDA47])

        # Fossilized Pokemon? (I think it's "if player has obtained it")
        flags.append(self.pyboy.memory[0xD710])

        # Fought Articuno yet?
        flags.append(self.pyboy.memory[0xD782])

        # Fought Zapdos yet?
        flags.append(self.pyboy.memory[0xD7D4])

        # Fought Vermillion Snorlax yet?
        flags.append(self.pyboy.memory[0xD7D8])

        # Fought Celadon Snorlax yet?
        flags.append(self.pyboy.memory[0xD7E0])

        # Fought Moltres yet?
        flags.append(self.pyboy.memory[0xD7EE])

        # Is SS Anne here?
        flags.append(self.pyboy.memory[0xD803])

        return flags
