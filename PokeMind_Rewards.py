import json

class Rewards:
    def __init__(self, pyboy, PokeMind):
        '''
        POTENTIAL CASE OF ABUSE:
            If player has pokemon in party and pokemon of same ID in PC,
                they can swap these 2 and get infinite rewards.
                This bug comes from the "level" function only being able to
                check pokemon IDs and make sure they're the same.
        '''
        
        self.pyboy = pyboy
        self.PokeMind = PokeMind
        
        self.seen_tiles = {}
        self.vision = 0
        self.time = 0
        self.time_penalty = 0
        self.fitness = 0
        # Experimentally found by printing flag values upon new game
        self.initial_flags = [165, 0, 126, 1, 12, 65, 2, 0, 16, 16, 0, 0, 12, 0, 2, 0, 128, 1, 0, 0, 0, 0, 0, 0, 0, 0, 64, 158, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.flags_reward = 0 # Incremented when current flags differ from initial
        self.pokedex_reward = 0
        self.badge_reward = 0
        self.level_reward = 0
        self.party_levels = [0, 0, 0, 0, 0, 0]
        self.party_IDs = [0, 0, 0, 0, 0, 0]

        try:
            with open('Reward Object Save State.json', 'r') as file:
                state = json.load(file)

            self.seen_tiles = state['seen_tiles']
            self.vision = state['vision']
            self.time = state['time']
            self.time_penalty = state['time_penalty']
            self.fitness = state['fitness']
            self.flags_reward = state['flags_reward']
            self.pokedex_reward = state['pokedex_reward']
            self.badge_reward = state['badge_reward']
            self.level_reward = state['level_reward']
            self.party_levels = state['party_levels']
            self.party_IDs = state['party_IDs']
        except:
            pass

    def save_state(self):
        state_dict = {}

        state_dict['seen_tiles'] = self.seen_tiles
        state_dict['vision'] = self.vision
        state_dict['time'] = self.time
        state_dict['time_penalty'] = self.time_penalty
        state_dict['fitness'] = self.fitness
        state_dict['flags_reward'] = self.flags_reward
        state_dict['pokedex_reward'] = self.pokedex_reward
        state_dict['badge_reward'] = self.badge_reward
        state_dict['level_reward'] = self.level_reward
        state_dict['party_levels'] = self.party_levels
        state_dict['party_IDs'] = self.party_IDs

        with open('Reward Object Save State.json', 'w') as file:
            json.dump(state_dict, file, indent=4)
        
    def fog_of_war(self, state):
        '''
        Determine what tiles player has seen.
        Rewards player for seeing new tiles from tilemap.

        state: Might also be referred to as "data". Main item given by the DAQ

        Does NOT return anything. Just changes the value of the rewards.
        '''
        
        # Get map ID
        ID = state['Map Data']['ID']

        # Get player coordinates
        pos = state['Sprite Data'][0]['Coordinates']

        # Create list that will host the tiles current showing on screen
        tiles_in_vision = []

        # Get map dimensions so we can filter out out-of-bound tiles easier
        map_width, map_height = state['Map Data']['Dimensions']

        # Some kind of conversion? Are map dimensions in 2x2 blocks of blocks?
            # That is to say, a block is a 2x2 of tiles, but could this be 2x2 of blocks?
        map_width *= 2
        map_height *= 2

        # Create the grid 4 tiles in any direction from the player
        for i in range(9):
            for j in range(9):
                # the -4 is because i and j start at 0, but we want to start 4 to the left/down
                x_shift = pos[0] - 4 + j
                y_shift = pos[1] - 4 + i

                # Turn these coordinates into a list
                tile = [x_shift, y_shift]

                # If tile is out-of-bounds, don't add to list
                if tile[0] < 0 or tile[1] < 0 or tile[0] > map_width-1 or tile[1] > map_height-1:
                    continue

                tiles_in_vision.append(tile)

        # If Map ID is not currently in dictionary, make a list with that ID
        if str(ID) not in self.seen_tiles:
            self.seen_tiles[str(ID)] = []

        # For all tiles in vision, add them to seen_tiles if not already there
        for tile in tiles_in_vision:
            if tile not in self.seen_tiles[str(ID)]:
                self.seen_tiles[str(ID)].append(tile)
                self.vision += 1

    def time_elapsed(self, state):
        _, seconds, minutes, hours = state['Clock']

        self.time = seconds + 60*minutes + 3600*hours
        self.time_penalty = -self.time

    def flags(self, state):
        flags = state['Flags']
        
        flag_counter = 0 # Counts how many flags differ from original
        for i in range(len(flags)):
            if flags[i] != self.initial_flags[i]:
                flag_counter += 1

        self.flags_reward = flag_counter

    def pokedex(self, state):
        pokedex = state['Pokedex']

        pokedex_counter = 0
        for i in range(len(pokedex)):
            if pokedex[i] == 1:
                pokedex_counter += 1

        self.pokedex_reward = pokedex_counter


    def badges(self, state):
        badges = state['Inventory']['Badges']

        badge_counter = 0
        for badge in badges:
            if badge == 1:
                badge_counter += 1

        self.badge_reward = badge_counter

    def levels(self, state):
        '''
        Gives reward based on levels gained.

        Reward is equal to the newly attained level.
            So going from 23 -> 24 yields a reward of 24 (with a weight of 1)
            This is to incentivize higher level pokemon

        '''
        # Make sure level count doesn't get messed up by switching pokemon
        for i in range(6):
            if state['Party'][i]['Pokemon'] == 0:
                continue
            # If Pokemon hasn't been changed and levels are different, add reward
            if state['Party'][i]['Pokemon'] == self.party_IDs[i]:
                if state['Party'][i]['Level'] != self.party_levels[i]:
                    self.party_levels[i] = state['Party'][i]['Level']
                    self.level_reward += self.party_levels[i]

            # If Pokemon has been changed, update the IDs and levels
            else:
                self.party_IDs[i] = state['Party'][i]['Pokemon']
                self.party_levels[i] = state['Party'][i]['Pokemon']
            
        
        

    def calculate_fitness(self, state, save=True):
        self.fog_of_war(state)
        self.time_elapsed(state)
        self.flags(state)
        self.pokedex(state)
        self.badges(state)
        self.levels(state)
        fitness_array = [self.vision,
                         self.time_penalty,
                         self.flags_reward,
                         self.pokedex_reward,
                         self.badge_reward,
                         self.level_reward
                         ]
        
        Lambdas = [1, # Vision weight
                   1/60, # Time Penalty weight (greater number = more punishment)
                   1000, # Flag weight
                   1000, # Pokedex weight
                   50000, # Badge weight
                   100    # Level weight (1 means reward = (newly attained level))
                   ] 

        fitness = 0
        for i in range(len(Lambdas)):
            fitness += Lambdas[i] * fitness_array[i]

        self.fitness = fitness

        if save:
            self.save_state()
        
