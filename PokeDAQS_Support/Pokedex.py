import PokeDAQS_Support.Byte_Unpacker as Byte_Unpacker

class Pokedex:
    def __init__(self, pyboy):
        '''
        Tracks seen and captured pokemon.

        0 = Not seen/captured
        1 = Seen/captured

        Provides a list for "seen/unseen" and a list for "captured/not captured"
        '''

        self.pyboy = pyboy


    def get_owned(self):
        '''
        Grabs list of binary integers.
        0 = not owned
        1 = owned

        return: List of integers
        '''
        
        owned_bytes = self.pyboy.memory[0xD2F7:0xD30A]

        owned = []
        
        for byte in owned_bytes:
            bits = Byte_Unpacker.unpack_bits(byte)
            bits.reverse()

            for bit in bits:
                owned.append(bit)

        return owned

    def get_seen(self):
        '''
        Grabs list of binary integers.
        0 = unseen
        1 = seen

        return: List of integers
        '''
        
        seen_bytes = self.pyboy.memory[0xD30A:0xD31D]

        seen = []

        for byte in seen_bytes:
            bits = Byte_Unpacker.unpack_bits(byte)

            for bit in bits:
                seen.append(bit)

        return seen
