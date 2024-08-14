def unpack_bits(byte):
    '''
    Turns a single byte value into a list of integer, binary bit values.

    return: List of binary bit values
    '''
    
    binary_string = bin(byte)

    bits = []

    # See how many digits are given by the bit string
    num_values = len(binary_string[2:])

    # Find out how many 0s we need to put at the beginning of the list
    num_zeros = 8 - num_values

    for i in range(num_zeros):
        bits.append(0)


    for i in range(num_values):
            bits.append(int(binary_string[2+i]))

    return bits


def bin_to_dec(bits: list):
    num_digits = len(bits)

    total = 0

    for i in range(num_digits):
        if bits[i] == 0:
            continue
        else:
            total += bits[i] * 2**(num_digits - 1 - i)

    return total

def byte_divider(byte, num_divisions, dec=False):
    '''
    Some bytes have multiple pieces of data stored within it. Separates them.

    num_divisions: Integer of value 2, 4, or 8.
        Will return 2, 4, or 8 values back

    dec = False gives back values in binary lists (e.g. [1,1,0,0])
    dec = True gives back the decimal value of that division (e.g. 12)

    return: 2, 4, or 8 lists (if dec=False) or integers (if dec=True)
    '''
    
    bits = unpack_bits(byte)

    if num_divisions == 2:
        item1 = bits[:4]
        item2 = bits[4:]

        if dec == True:
            item1 = bin_to_dec(item1)
            item2 = bin_to_dec(item2)

        return item1, item2

    if num_divisions == 4:
        item1 = bits[:2]
        item2 = bits[2:4]
        item3 = bits[4:6]
        item4 = bits[6:8]

        if dec == True:
            item1 = bin_to_dec(item1)
            item2 = bin_to_dec(item2)
            item3 = bin_to_dec(item3)
            item4 = bin_to_dec(item4)

        return item1, item2, item3, item4

    if num_divisions == 8:
        item1 = bits[0]
        item2 = bits[1]
        item3 = bits[2]
        item4 = bits[3]
        item5 = bits[4]
        item6 = bits[5]
        item7 = bits[6]
        item8 = bits[7]

        if dec == True:
            item1 = bin_to_dec(item1)
            item2 = bin_to_dec(item2)
            item3 = bin_to_dec(item3)
            item4 = bin_to_dec(item4)
            item5 = bin_to_dec(item5)
            item6 = bin_to_dec(item6)
            item7 = bin_to_dec(item7)
            item8 = bin_to_dec(item8)

        return item1, item2, item3, item4, item5, item6, item7, item8
        
    
