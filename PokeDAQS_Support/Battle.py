import sys
import PokeDAQS_Support.Byte_Unpacker as Byte_Unpacker
import Constants.Pokemon_IDs as Pokemon_IDs

class Battle:
    def __init__(self, pyboy):
        '''
        Pulls battle state information

        pyboy: Instance of PyBoy emulator object
        '''

        self.pyboy = pyboy

    def get_numturns(self):
        '''
        return: Integer value of the number of turns in the current battle
        Unsure if it starts at 0 or 1.
        '''

        try:
            return self.pyboy.memory[0xCCD5]

        except AttributeError as e:
            print("Message from Battle.py:")
            print("Error pulling number of turns.")
            print(f"Error: {e}")
            sys.exit()

    def get_substitute_hp(self):
        '''
        return: List of shape [player_substitute_HP, enemy_substitute_HP]
        '''

        try:
            player_sub_hp = self.pyboy.memory[0xCCD7:0xCCD9]

        except AttributeError as e:
            print("Message from Battle.py:")
            print("Error pulling substitute HP.")
            print(f"Error: {e}")
            sys.exit()

    def get_move_menu_type(self):
        '''
        0 is regular
        1 is mimic
        others are text boxes (learn move, PP-refill...)

        return: Integer value of the menu type
        '''

        try:
            return self.pyboy.memory[0xCCDB]

        except AttributeError as e:
            print("Message from Battle.py:")
            print("Error pulling battle move-menu type.")
            print(f"Error: {e}")
            sys.exit()

    def get_move_choices(self):
        '''
        Player-selected move updates on hovering a new choice
        Enemy-selected move updates upon you making a move choice

        Not sure if it's numbers 1-4 based on move order or if it's a move ID

        return: List of shape [player_move, enemy_move]
        '''

        try:
            return self.pyboy.memory[0xCCDC:0xCCDD+1]

        except AttributeError as e:
            print("Message from Battle.py:")
            print("Error pulling move choices.")
            print(f"Error: {e}")
            sys.exit()

    def get_stat_modifiers(self):
        '''
        Pulls the modifiers to each stat for each Pokemon in battle.

        return: List of Lists of shape (player_atk_mod, enemy_atk_mod), etc
        '''

        try:
            atk_mods = [self.pyboy.memory[0xCD1A], self.pyboy.memory[0xCD2E]]
            def_mods = [self.pyboy.memory[0xCD1B], self.pyboy.memory[0xCD2F]]
            speed_mods = [self.pyboy.memory[0xCD1C], self.pyboy.memory[0xCD30]]
            spec_mods = [self.pyboy.memory[0xCD1D], self.pyboy.memory[0xCD31]]
            acc_mods = [self.pyboy.memory[0xCD1E], self.pyboy.memory[0xCD32]]
            evasion_mods = [self.pyboy.memory[0xCD1F], self.pyboy.memory[0xCD33]]

            stat_mods = [atk_mods, def_mods, speed_mods,spec_mods, acc_mods, evasion_mods]

            return stat_mods

        except AttributeError as e:
            print("Message from Battle.py:")
            print("Error pulling stat modifiers.")
            print(f"Error: {e}")
            sys.exit()


    def get_escape_factor(self):
        '''
        Refers to a wild Pokemon's ability to escape in the Safari Zone

        return: Integer escape factor
        '''

        return self.pyboy.memory[0xCCE8]

    def get_bait_factor(self):
        '''
        Refers to using bait in the Safari Zone

        return: Integer bait factor
        '''

        return self.pyboy.memory[0xCCE9]


    def get_current_move_data(self):
        '''
        Retrieves data about the moves being used in battle.

        return: Dictionary of these values in shape (your_pokemon, their_pokemon)
        '''

        moves_dict = {}
        
        # Move IDs
        your_ID = self.pyboy.memory[0xCFD2]
        enemy_ID = self.pyboy.memory[0xCFCC]
        moves_dict['ID'] = (your_ID, enemy_ID)
        

        # Move Effects
        your_effect = self.pyboy.memory[0xCFD3]
        enemy_effect = self.pyboy.memory[0xCFCD]
        moves_dict['Effect'] = (your_effect, enemy_effect)
        

        # Move Power
        your_power = self.pyboy.memory[0xCFD4]
        enemy_power = self.pyboy.memory[0xCFCE]
        moves_dict['Power'] = (your_power, enemy_power)

        # Move Type
        your_type = self.pyboy.memory[0xCFD5]
        enemy_type = self.pyboy.memory[0xCFCF]
        moves_dict['Type'] = (your_type, enemy_type)

        # Move Accuracy
        your_acc = self.pyboy.memory[0xCFD6]
        enemy_acc = self.pyboy.memory[0xCFD0]
        moves_dict['Accuracy'] = (your_acc, enemy_acc)

        return moves_dict


    def get_pokemon_data(self):
        '''
        Pulls data about the Pokemon that are in battle right now.

        return: Dictionary with all values of shape (your_pokemon, enemy_pokemon)
        '''

        poke_data = {}

        # Pokemon number (Game ID converted to Pokedex ID)
        your_ID = self.pyboy.memory[0xD014]
        your_ID = Pokemon_IDs.Poke_IDs[your_ID]
        enemy_ID = self.pyboy.memory[0xCFE5]
        enemy_ID = Pokemon_IDs.Poke_IDs[enemy_ID]
        poke_data['ID'] = (your_ID, enemy_ID)

        # HP (takes 2 RAM slots. Added together)
        # Remember that slices are exclusive
        your_HP = sum(self.pyboy.memory[0xD015:0xD017])
        enemy_HP = sum(self.pyboy.memory[0xCFE6:0xCFE8])
        poke_data['HP'] = (your_HP, enemy_HP)

        # Level
        your_level = self.pyboy.memory[0xD022]
        enemy_level = self.pyboy.memory[0xCFF3]
        poke_data['Level'] = (your_level, enemy_level)

        # Status
        your_status = self.pyboy.memory[0xD018]
        enemy_status = self.pyboy.memory[0xCFE9]
        poke_data['Status'] = (your_status, enemy_status)

        # Types
        your_types = (self.pyboy.memory[0xD019], self.pyboy.memory[0xD01A])
        enemy_types = (self.pyboy.memory[0xCFEA], self.pyboy.memory[0xCFEB])
        poke_data['Types'] = (your_types, enemy_types)

        # Move Slots
        your_moves = self.pyboy.memory[0xD01C:0xD020]
        enemy_moves = self.pyboy.memory[0xCFED:0xCFF1]
        poke_data['Moves'] = (your_moves, enemy_moves)

        # DVs
        # Attack and Defense combined together. Same with Speed and Special.
        # Split them into their own variables, then combine them
        atk_def = self.pyboy.memory[0xD020]
        speed_spec = self.pyboy.memory[0xD021]
        
        your_atk, your_def  = Byte_Unpacker.byte_divider(atk_def, 2, dec=True)
        your_spd, your_spec = Byte_Unpacker.byte_divider(speed_spec, 2, dec=True)

        enemy_atk_def = self.pyboy.memory[0xCFF1]
        enemy_spd_spec = self.pyboy.memory[0xCFF2]

        enemy_atk, enemy_def = Byte_Unpacker.byte_divider(enemy_atk_def, 2, dec=True)
        enemy_spd, enemy_spec = Byte_Unpacker.byte_divider(enemy_spd_spec, 2, dec=True)

        poke_data['Attack DVs'] = (your_atk, enemy_atk)
        poke_data['Defense DVs'] = (your_def, enemy_def)
        poke_data['Speed DVs'] = (your_spd, enemy_spd)
        poke_data['Special DVs'] = (your_spec, enemy_spec)


        # Max HP (takes 2 RAM slots. Added together for total)
        your_max_hp = sum(self.pyboy.memory[0xD023:0xD025])
        enemy_max_hp = sum(self.pyboy.memory[0xCFF4:0xCFF6])
        poke_data['Max HP'] = (your_max_hp, enemy_max_hp)

        # Attack (takes 2 RAM slots)
        your_attack = sum(self.pyboy.memory[0xD025:0xD027])
        enemy_attack = sum(self.pyboy.memory[0xCFF6:0xCFF8])
        poke_data['Attack'] = (your_attack, enemy_attack)

        # Defense (takes 2 RAM slots)
        your_defense = sum(self.pyboy.memory[0xD027:0xD029])
        enemy_defense = sum(self.pyboy.memory[0xCFF8:0xCFFA])
        poke_data['Defense'] = (your_defense, enemy_defense)

        # Speed (takes 2 RAM slots)
        your_speed = sum(self.pyboy.memory[0xD029:0xD02B])
        enemy_speed = sum(self.pyboy.memory[0xCFFA:0xCFFC])
        poke_data['Speed'] = (your_speed, enemy_speed)

        # Special (takes 2 RAM slots)
        your_spec = sum(self.pyboy.memory[0xD02B:0xD02D])
        enemy_spec = sum(self.pyboy.memory[0xCFFC:0xCFFE])
        poke_data['Special'] = (your_spec, enemy_spec)

        # PP for slots 1-4
        your_pp = self.pyboy.memory[0xD02D:0xD031]
        enemy_pp = self.pyboy.memory[0xCFFE:0xD002]
        poke_data['PP'] = (your_pp, enemy_pp)

        return poke_data

    def get_battle_type(self):
        # D057 is listed as "Type of battle" while D05A is listed as "Battle Type"
        # Not sure what the difference is. I'll assume the AI can figure it out

        return (self.pyboy.memory[0xD057], self.pyboy.memory[0xD05A])

    def is_leader_music_playing(self):
        # Not sure which values are True or False
        # I assume the model might be able to use this to identify it as an important battle

        return self.pyboy.memory[0xD05C]

    def crit_flag(self):
        # 00 if nothing I assume
        # 01 if Critical Hit!
        # 02 if One-Hit KO!

        return self.pyboy.memory[0xD05E]

    def fishing_flag(self):
        # Not sure of return values but I think it's a boolean
        return self.pyboy.memory[0xD05F]

    def get_battle_status(self):
        '''
        Below explains the known values.
        Each byte (RAM address has 8 bits)
        Each bit corresponds to a status
        
        First byte:
            bit 0 = Bide
            bit 1 = Thrash / petal dance
            bit 2 = Attacking multiple times (e.g. Double Kick)
            bit 3 = Flinch
            bit 4 = Charging up for attack
            bit 5 = Using multi-turn move (e.g. Wrap)
            bit 6 = Invulnerable to normal attacks (using fly or dig)
            bit 7 = Confusion

        Second byte:
            bit 0 = X Accuracy effect
            bit 1 = Protected by "mist"
            bit 2 = focus energy effect
            bit 3 = (Undocumented or unused)
            bit 4 = has a substitute
            bit 5 = need to recharge
            bit 6 = rage
            bit 7 = leech seeded

        Third byte:
            bit 0 = Toxic
            bit 1 = Light Screen
            bit 2 = Reflect
            bit 3 = Transformed

        return: List of tuples of shape (yours, enemy's)
        '''

        your_status_bytes = self.pyboy.memory[0xD062:0xD065]
        enemy_status_bytes = self.pyboy.memory[0xD067:0xD06A]

        your_status = []
        enemy_status = []

        for i in range(3):
            your_bits = Byte_Unpacker.unpack_bits(your_status_bytes[i])
            enemy_bits = Byte_Unpacker.unpack_bits(enemy_status_bytes[i])
            
            for j in range(len(your_bits)):
                your_status.append(your_bits[j])
                enemy_status.append(enemy_bits[j])

        return (your_status, enemy_status)

    
            
    def get_battle_data(self):
        '''
        Combines all data from other methods in the class.

        return: Dictionary
        '''

        battle = {}

        battle['Turn Count'] = self.get_numturns()
        battle['Substitute HP'] = self.get_substitute_hp()
        battle['Menu Type'] = self.get_move_menu_type()
        battle['Move Choice'] = self.get_move_choices()
        battle['Stat Modifiers'] = self.get_stat_modifiers()
        battle['Escape Factor'] = self.get_escape_factor()
        battle['Bait Factor'] = self.get_bait_factor()
        battle['Move Data'] = self.get_current_move_data()
        battle['Pokemon Data'] = self.get_pokemon_data()
        battle['Battle Type'] = self.get_battle_type()
        battle['Leader Music'] = self.is_leader_music_playing()
        battle['Crit Flag'] = self.crit_flag()
        battle['Fishing Flag'] = self.fishing_flag()
        battle['Battle Status'] = self.get_battle_status()

        return battle

        
