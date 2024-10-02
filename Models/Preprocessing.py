import json
import sys
import math
from ..Constants import Experience_Rates as ER

class Preprocessor:
    def __init__(self):
        self.slow, self.med_slow, self.med_fast, self.fast = ER.load_exp_rates()
        self.rates = [self.slow, self.med_slow, self.med_fast, self.fast]
        try:
            with open("Max Values.json", 'r') as file:
                maxvals = json.load(file)

        except:
            print("Error loading 'Max Values.json'.")
            input("Press anything to continue the prgoram and create this file.")
            maxvals = {'Cursor Coordinate': 0,
                       'Max HP': 0,
                       'Map Dimensions': [0,0],
                       'Frames': 30,
                       }


    def normalize(self, state):
        '''
        Normalizes numerical values from the flattened state.

        Does NOT make adjustments to categorical data.

        return: state object with normalized numerical values
        '''

        # We set this to true if new max values are found for anything
        # This will save the json file at the end of the method if True
        new_maxes = False

        # Sprite Coordinates
        # Index 1 selects sprite coordinates, index 0 selects x pos
        if 'Sprite 0' in state and 'Map Dimensions' in state:
            for i in range(16):
                norm_x = state[f'Sprite {i}'][1][0] / state['Map Dimensions'][0]
                norm_y = state[f'Sprite {i}'][1][1] / state['Map Dimensions'][1]

                # Check validity of normalization
                if norm_x > 1 or norm_y > 1:
                    print("Normalizer.py returned an error.")
                    print("Error normalizing sprite coordinates. Sprite coords lie outside of the map dimensions.")
                    sys.exit()
                    
                norm_coords = (norm_x, norm_y)
                state[f'Sprite {i}'][1] =  norm_coords
        elif ('Sprite 0' in state and 'Map Dimensions' not in state):
            print("Error from Normalizer.py")
            print("Sprite coordinates could not be normalized.")
            print("Map dimensions not given for normalization.")
            sys.exit()
        else:
            pass


        
        # Cursor Coordiantes
        # Check if current coordinate is larger than max
        if 'Cursor Coordinate' in state:
            if (state['Cursor Coordinate'][0] > maxvals['Cursor Coordinate'][0] or
                state['Cursor Coordinate'][1] > maxvals['Cursor Coordinate'][1]):
                
                maxvals['Cursor Coordinate'] = state['Cursor Coordinate']
                new_maxes = True

            norm_curs_coord = state['Cursor Coordinate'] / maxvals['Cursor Coordinate']
            state['Cursor Coordinate'] = norm_curs_coord
        else:
            pass


        # Turn Count
        if 'Turn Count' in state:
            state['Turn Count'] = math.log(1 + state['Turn Count'], 10)
        else:
            pass


        # Substitute HP
        if 'Substitute HP' in state:
            state['Substitute HP'] = math.log(1 + state['Substitute HP'], 10)
        else:
            pass


        # Stat Modifiers
        if 'Stat Modifiers' in state:
            for stat in state['Stat Modifiers']:
                stat[0] = stat[0] / 6
                stat[1] = stat[1] / 6
        else:
            pass
        

        # Safari Zone stats
        if 'Escape Factor' in state:
            state['Escape Factor'] = math.log(1 + state['Escape Factor'], 10)
        if 'Bait Factor' in state:
            state['Bait Factor'] = math.log(1 + state['Bait Factor'], 10)

        # Move power and accuracy
        if 'Your Move' in state:
            state['Your Move'][2] = math.log(1 + state['Your Move'][2], 10)
            state['Your Move'][4] = state['Your Move'][4] / 100
        if 'Enemy Move' in state:
            state['Enemy Move'][2] = math.log(1 + state['Enemy Move'][2], 10)
            state['Enemy Move'][4] = state['Enemy Move'][4] / 100

        # Pokemon Data (During Battle)
        yours = state['Your Pokemon Data']
        theirs = state['Enemy Pokemon Data']

        yours[1] = yours[1] / yours[10] # Current HP / Max
        theirs[1] = theirs[1] / theirs[10]

        yours[2] = math.log(1 + yours[2], 10)   # Levels
        theirs[2] = math.log(1 + theirs[2], 10)

        yours[6] = math.log(1 + yours[6], 10)   # Attack DV
        theirs[6] = math.log(1 + theirs[6], 10)

        yours[7] = math.log(1 + yours[7], 10)   # Defense DV
        theirs[7] = math.log(1 + theirs[7], 10)

        yours[8] = math.log(1 + yours[8], 10)   # Speed DV
        theirs[8] = math.log(1 + theirs[8], 10)

        yours[9] = math.log(1 + yours[9], 10)   # Special DV
        theirs[9] = math.log(1 + theirs[9], 10)

        # Check for new highest seen max HP
        if yours[10] > maxvals['Max HP']:
            maxvals['Max HP'] = yours[10]
            new_maxes = True
        if theirs[10] > maxvals['Max HP']:
            maxvals['Max HP'] = theirs[10]
            new_maxes = True
            
        yours[10] = yours[10] / maxvals['Max HP'] # Max HP
        theirs[10] = theirs[10] / maxvals['Max HP']
        
        stat_indices = [11, 12, 13, 14]

        # Attack, Defense, Speed, Special
        for i in stat_indices:
            yours[i] = math.log(1 + yours[i], 10)
            theirs[i] = math.log(1 + theirs[i], 10)

        # PP values (can't identify the moves to find max values for so idk...)
        for i in range(4):
            yours[15][i] = math.log(1 + yours[15][i], 10)
            theirs[15][i] = math.log(1 + theirs[15][i], 10)

        # Inventory Items (normalizing the item count)
        for item in state['Inventory Items']:
            item[1] = math.log(1 + item[1], 10)

        # Money
        state['Money'] = math.log(1 + state['Money'], 10)

        # Map Dimensions
        if state['Map Dimensions'][0] > maxvals['Map Dimensions'][0]:
            maxvals['Map Dimensions'][0] = state['Map Dimensions'][0]
            new_maxes = True
        if state['Map Dimensions'][1] > maxvals['Map Dimensions'][1]:
            maxvals['Map Dimensions'][1] = state['Map Dimensions'][1]
            new_maxes = True

        state['Map Dimensions'][0] = state['Map Dimensions'][0] / maxvals['Map Dimensions'][0]
        state['Map Dimensions'][1] = state['Map Dimensions'][1] / maxvals['Map Dimensions'][1]

        for item in state['PC Items']:
            item[1] = math.log(1 + item[1], 10)

        for pokemon in state['PC Pokemon']:
            pokemon[1] = 1 # HP doesn't really matter since they're full HP in PC

            # For exp we use formula (x - ac) / (an - ac)
                # x  = current experience amount
                # "a" just being a constant with subscript c or n
                # ac = Exp needed to achieve current level
                # an = Exp needed to achieve next level
            x = pokemon[6]
            ac = ER.get_exp_at_level(pokemon[0], pokemon[2], self.rates)
            an = ER.get_exp_at_level(pokemon[0], pokemon[2] + 1, self.rates)
            pokemon[6] = (x - ac) / (an - ac)


            pokemon[2] = math.log(1 + pokemon[2], 10) # Levels
            pokemon[7] = math.log(1 + pokemon[7], 100) # HP EV (EV's get very large, so we use base 100)
            pokemon[8] = math.log(1 + pokemon[8], 100) # Attack EV
            pokemon[9] = math.log(1 + pokemon[9], 100) # Defense EV
            pokemon[10] = math.log(1 + pokemon[10], 100) # Speed EV
            pokemon[11] = math.log(1 + pokemon[11], 100) # Special EV
            pokemon[12] = pokemon[12] / 15
            pokemon[13] = pokemon[13] / 15
            pokemon[14] = pokemon[14] / 15
            pokemon[15] = pokemon[15] / 15

            for move in pokemon[16]:
                move = 1 # PP doesn't matter

        for pokemon in state['Common Pokemon']:
            pokemon[1] = math.log(1 + pokemon[1], 10)

        for pokemon in state['Uncommon Pokemon']:
            pokemon[1] = math.log(1 + pokemon[1], 10)

        for pokemon in state['Rares']:
            pokemon[1] = math.log(1 + pokemon[1], 10)

        for pokemon in state['Party']:
            pokemon[1] = pokemon[1] / pokemon[2] # HP / Max HP

            # Check for new highest seen max HP
            if pokemon[2] > maxvals['Max HP']:
                maxvals['Max HP'] = pokemon[2]
                new_maxes = True
        
            pokemon[2] = pokemon[2] / maxvals['Max HP'] # Max HP
            pokemon[3] = math.log(1 + pokemon[3], 10)
            
            # For exp we use formula (x - ac) / (an - ac)
            # x  = current experience amount
            # "a" just being a constant with subscript c or n
            # ac = Exp needed to achieve current level
            # an = Exp needed to achieve next level
            x = pokemon[7]  # Experience
            ac = ER.get_exp_at_level(pokemon[0], pokemon[3], self.rates)
            an = ER.get_exp_at_level(pokemon[0], pokemon[3] + 1, self.rates)
            pokemon[7] = (x - ac) / (an - ac)

            pokemon[8] = math.log(1 + pokemon[8], 10) # Attack
            pokemon[9] = math.log(1 + pokemon[9], 10) # Defense
            pokemon[10] = math.log(1 + pokemon[10], 10) # Speed
            pokemon[11] = math.log(1 + pokemon[11], 10) # Special
            pokemon[12] = math.log(1 + pokemon[12], 10) # HP EV
            pokemon[13] = math.log(1 + pokemon[13], 10) # Attack EV
            pokemon[14] = math.log(1 + pokemon[14], 10) # Defense EV
            pokemon[15] = math.log(1 + pokemon[15], 10) # Speed EV
            pokemon[16] = math.log(1 + pokemon[16], 10) # Special EV
            pokemon[17] = pokemon[17] / 15 # Attack IV
            pokemon[18] = pokemon[18] / 15 # Defense IV
            pokemon[19] = pokemon[19] / 15 # Speed IV
            pokemon[20] = pokemon[20] / 15 # Special IV

            for move in pokemon[21]: # Set PP 
                move = 1 # I don't know of a way to normalize this...


        for pokemon in state['Opponent Pokemon']:
            pokemon[1] = pokemon[1] / pokemon[2] # HP / Max HP

            # Check for new highest seen max HP
            if pokemon[2] > maxvals['Max HP']:
                maxvals['Max HP'] = pokemon[2]
                new_maxes = True
        
            pokemon[2] = pokemon[2] / maxvals['Max HP'] # Max HP
            pokemon[3] = math.log(1 + pokemon[3], 10)
            

            pokemon[7] = math.log(1 + pokemon[7], 10) # Attack
            pokemon[8] = math.log(1 + pokemon[8], 10) # Defense
            pokemon[9] = math.log(1 + pokemon[9], 10) # Speed
            pokemon[10] = math.log(1 + pokemon[10], 10) # Special
            pokemon[11] = math.log(1 + pokemon[11], 10) # HP EV
            pokemon[12] = math.log(1 + pokemon[12], 10) # Attack EV
            pokemon[13] = math.log(1 + pokemon[13], 10) # Defense EV
            pokemon[14] = math.log(1 + pokemon[14], 10) # Speed EV
            pokemon[15] = math.log(1 + pokemon[15], 10) # Special EV
            pokemon[16] = pokemon[16] / 15 # Attack IV
            pokemon[17] = pokemon[17] / 15 # Defense IV
            pokemon[18] = pokemon[18] / 15 # Speed IV
            pokemon[19] = pokemon[19] / 15 # Special IV

            for move in pokemon[20]: # Set PP 
                move = 1 # I don't know of a way to normalize this...


        if state['Clock'][0] > maxvals['Frames']:
            maxvals['Frames'] = state['Clock'][0]
            
        state['Clock'][0] = state['Clock'][0] / maxvals['Frames']
        state['Clock'][1] = state['Clock'][1] / 60
        state['Clock'][2] = state['Clock'][2] / 60
        state['Clock'][3] = state['Clock'][3] / 255
        

        if new_maxes:
            with open("Max Values.json", 'w') as file:
                json.dump(maxvals, file, indent=4)

        return state

    def one_hot_encoder(self, state):
        
