import sys
import PokeDAQS_Support.Vision as Vision
import PokeDAQS_Support.Sprites as Sprites
import PokeDAQS_Support.Menu as Menu
import PokeDAQS_Support.PokeMart as PokeMart
import PokeDAQS_Support.Pokedex as Pokedex
import PokeDAQS_Support.Game_Corner as Game_Corner
import PokeDAQS_Support.Battle as Battle
import PokeDAQS_Support.Inventory as Inventory
import PokeDAQS_Support.Map as Map
import PokeDAQS_Support.PC as PC
import PokeDAQS_Support.Flags as Flags
import PokeDAQS_Support.Wild_Pokemon as Wild_Pokemon
import PokeDAQS_Support.Party as Party
import PokeDAQS_Support.Opponent_Pokemon as Opponent_Pokemon
import PokeDAQS_Support.Clock as Clock


class DAQ:
    def __init__(self, pyboy, PokeMind):
        """
        Initialize DAQ object to pull game state data

        pyboy: Instance of PyBoy emulator object
        PokeMind: Instance of PyBoy Pokemon Wrapper object
        """

        # Initialize data collection objects
        self.pyboy = pyboy
        self.PokeMind = PokeMind
        self.Vision = Vision.Vision(pyboy, PokeMind)
        self.Sprites = Sprites.Sprites(pyboy)
        self.Menu = Menu.Menu(pyboy)
        self.PokeMart = PokeMart.PokeMart(pyboy)
        self.Pokedex = Pokedex.Pokedex(pyboy)
        self.Game_Corner = Game_Corner.Game_Corner(pyboy)
        self.Battle = Battle.Battle(pyboy)
        self.Inventory = Inventory.Inventory(pyboy)
        self.Map = Map.Map(pyboy)
        self.PC = PC.PC(pyboy)
        self.Flags = Flags.Flags(pyboy)
        self.Wild_Pokemon = Wild_Pokemon.Wild_Pokemon(pyboy)
        self.Party = Party.Party(pyboy)
        self.Opponent_Pokemon = Opponent_Pokemon.Opponent_Pokemon(pyboy)
        self.Clock = Clock.Clock(pyboy)

        self.data = {"Screen Image": None,   # PIL Image Object
                     "Sprite Data": None,    # List of 16 dictionaries. Keys found in Sprites.py
                     "Menu Data": None,      # Dictionary of menu information
                     "PokeMart Items": None, # List of up to 10 available PokeMart items
                     }

    def get_game_state(self):
        """
        Collects all data deemed important into self.data dictionary
        """
        try:
            self.data["Screen Image"] = self.Vision.get_screen()
            self.data["Sprite Data"] = self.Sprites.get_sprite_data()
            self.data["Menu Data"] = self.Menu.get_menu_data()
            self.data["PokeMart Items"] = self.PokeMart.get_mart_items()
            self.data["Pokedex"] = self.Pokedex.get_owned() # Not including seen/unseen
            self.data["Game Corner"] = self.Game_Corner.get_game_corner_data()
            self.data["Battle Info"] = self.Battle.get_battle_data()
            self.data["Inventory"] = self.Inventory.get_inventory_data()
            self.data["Map Data"] = self.Map.get_map_data()
            self.data["PC"] = self.PC.get_pc_data()
            self.data["Flags"] = self.Flags.get_event_flags()
            self.data["Wild Pokemon"] = self.Wild_Pokemon.get_wild_pokemon_data()
            self.data["Party"] = self.Party.get_party()
            self.data["Opponent Pokemon"] = self.Opponent_Pokemon.get_opponent_party()
            self.data["Clock"] = self.Clock.get_game_time()
            
            

        except AttributeError as e:
            print("Message from PokeDAQS:")
            print("get_game_state function as failed :(")
            print(f"Error message given: {e}")
            sys.exit()

        return self.data


    def flatten_data(self):
        self.flat_data = {}

        sprites = self.data["Sprite Data"]
        battle = self.data['Battle Info']

        for i in range(16):
            ID = sprites[i]["Identifier"]   # Number, categorical
            coords = sprites[i]["Coordinates"]  # Tuple of numbers, numerical
            face = sprites[i]["Face Direction"] # Number, categorical
            self.flat_data[f"Sprite {i}"] = (ID, coords, face)  # Tuple of the above
            
        self.flat_data['Cursor Coordinate'] = self.data["Menu Data"]["Cursor Coordinate"]   # Tuple, numerical
        self.flat_data['Current Selection'] = self.data['Menu Data']['Current Selection']   # Number, categorical
        self.flat_data['Select Item'] = self.data['Menu Data']['Select Item']   # Number, categorical

        self.flat_data['PokeMart Items'] = self.data['PokeMart Items']  # List, categorical

        self.flat_data['Pokedex'] = self.data['Pokedex']    # List, boolean

        self.flat_data['Turn Count'] = battle['Turn Count'] # Number, numerical
        self.flat_data['Substitute HP'] = battle['Substitute HP']   # Number, numerical
        self.flat_data['Menu Type'] = battle['Menu Type']   # Number, categorical
        self.flat_data['Move Choice'] = battle['Move Choice']   # List of 2 numbers, categorical
        self.flat_data['Stat Modifiers'] = battle['Stat Modifiers'] # Tuple of tuples, numerical
        self.flat_data['Escape Factor'] = battle['Escape Factor']   # Number, numerical?
        self.flat_data['Bait Factor'] = battle['Bait Factor']   # Number, numerical?
        self.flat_data['Your Move'] = [battle['Move Data']['ID'][0],    # Number, categorical
                                       battle['Move Data']['Effect'][0], # Number, categorical
                                       battle['Move Data']['Power'][0], # Number, numerical
                                       battle['Move Data']['Type'][0],  # Number, categorical
                                       battle['Move Data']['Accuracy'][0]] # Number, numerical

        self.flat_data['Enemy Move'] = [battle['Move Data']['ID'][1],    # Number, categorical
                                       battle['Move Data']['Effect'][1], # Number, categorical
                                       battle['Move Data']['Power'][1], # Number, numerical
                                       battle['Move Data']['Type'][1],  # Number, categorical
                                       battle['Move Data']['Accuracy'][1]] # Number, numerical

        self.flat_data['Your Pokemon Data'] = [battle['Move Data']['ID'][0],    # Categorical
                                               battle['Move Data']['HP'][0],    # Numerical
                                               battle['Move Data']['Level'][0], # Numerical
                                               battle['Move Data']['Status'][0],# Categorical
                                               battle['Move Data']['Types'][0], # Tuple, Categorical
                                               battle['Move Data']['Moves'][0], # Tuple, Categorical
                                               battle['Move Data']['Attack DVs'][0], # Numerical
                                               battle['Move Data']['Defense DVs'][0],# Numerical
                                               battle['Move Data']['Speed DVs'][0],  # Numerical
                                               battle['Move Data']['Special DVs'][0],# Numerical
                                               battle['Move Data']['Max HP'][0],    # Numerical
                                               battle['Move Data']['Attack'][0],    # Numerical
                                               battle['Move Data']['Defense'][0],   # Numerical
                                               battle['Move Data']['Speed'][0],     # Numerical
                                               battle['Move Data']['Special'][0],   # Numerical
                                               battle['Move Data']['PP'][0]]        # Numerical

        self.flat_data['Enemy Pokemon Data'] = [battle['Move Data']['ID'][1],    # Categorical
                                               battle['Move Data']['HP'][1],    # Numerical
                                               battle['Move Data']['Level'][1], # Numerical
                                               battle['Move Data']['Status'][1],# Categorical
                                               battle['Move Data']['Types'][1], # Tuple, Categorical
                                               battle['Move Data']['Moves'][1], # Tuple, Categorical
                                               battle['Move Data']['Attack DVs'][1], # Numerical
                                               battle['Move Data']['Defense DVs'][1],# Numerical
                                               battle['Move Data']['Speed DVs'][1],  # Numerical
                                               battle['Move Data']['Special DVs'][1],# Numerical
                                               battle['Move Data']['Max HP'][1],    # Numerical
                                               battle['Move Data']['Attack'][1],    # Numerical
                                               battle['Move Data']['Defense'][1],   # Numerical
                                               battle['Move Data']['Speed'][1],     # Numerical
                                               battle['Move Data']['Special'][1],   # Numerical
                                               battle['Move Data']['PP'][1]]        # Numerical

        self.flat_data['Battle Type'] = battle['Battle Type']   # Tuple, Categorical
        self.flat_data['Leader Music'] = battle['Leader Music'] # Boolean?
        self.flat_data['Crit Flag'] = battle['Crit Flag'] # Categorical
        self.flat_data['Fishing Flag'] = battle['Fishing Flag'] # Boolean? Categorical?
        self.flat_data['Your Battle Status'] = battle['Battle Status'][0]   # List, Boolean
        self.flat_data['Enemy Battle Status'] = battle['Battle Status'][1]

        self.flat_data['Inventory Items'] = self.data['Inventory']['Items'] # List of tuples, (Categorical, Numerical)
        self.flat_data['Money'] = self.data['Inventory']['Money']   # Numerical
        self.flat_data['Badges'] = self.data['Inventory']['Badges'] # List, Boolean

        self.flat_data['Map ID'] = self.data['Map Data']['ID']  # Categorical
        self.flat_data['Map Dimensions'] = self.data['Map Data']['Dimensions'] # Tuple, Numerical

        self.flat_data['PC Items'] = self.data['PC']['Items']   # List of tuples, (Categorical, Numerical)
        self.flat_data['PC Pokemon'] = []

        for pokemon in self.data['PC']['Pokemon']:
            pokemon_data = []
            pokemon_data.append(pokemon['Pokemon']) # Categorical
            pokemon_data.append(pokemon['Current HP']) # Numerical
            pokemon_data.append(pokemon['Level']) # Numerical
            pokemon_data.append(pokemon['Status']) # Categorical
            pokemon_data.append(pokemon['Types']) # Tuple, Categorical
            pokemon_data.append(pokemon['Moves']) # List, Categorical
            pokemon_data.append(pokemon['Experience']) # Numerical
            pokemon_data.append(pokemon['HP EV']) # Numerical
            pokemon_data.append(pokemon['Attack EV']) # Numerical
            pokemon_data.append(pokemon['Defense EV']) # Numerical
            pokemon_data.append(pokemon['Speed EV']) # Numerical
            pokemon_data.append(pokemon['Special EV']) # Numerical
            pokemon_data.append(pokemon['Attack IV']) # Numerical
            pokemon_data.append(pokemon['Defense IV']) # Numerical
            pokemon_data.append(pokemon['Speed IV']) # Numerical
            pokemon_data.append(pokemon['Spec IV']) # Numerical
            pokemon_data.append(pokemon['Move PPs']) # Numerical
            self.flat_data['PC Pokemon'].append(pokemon_data)
            
        self.flat_data['Flags'] = self.data['Flags'] # List, Categorical

        self.flat_data['Common Pokemon'] = self.data['Wild Pokemon']['Common'] # List of tuples (Categorical, Numerical)
        self.flat_data['Uncommon Pokemon'] = self.data['Wild Pokemon']['Uncommon'] # List of tuples (Categorical, Numerical)
        self.flat_data['Rares'] = self.data['Wild Pokemon']['Rares'] # List of tuples (Categorical, Numerical)

        self.flat_data['Party'] = []

        for pokemon in self.data['Party']:
            pokemon_data = []
            pokemon_data.append(pokemon['Pokemon']) # Categorical
            pokemon_data.append(pokemon['Current HP']) # Numerical
            pokemon_data.append(pokemon['Max HP']) # Numerical
            pokemon_data.append(pokemon['Level']) # Numerical
            pokemon_data.append(pokemon['Status']) # Categorical
            pokemon_data.append(pokemon['Types']) # Tuple, Categorical
            pokemon_data.append(pokemon['Moves']) # List, Categorical
            pokemon_data.append(pokemon['Experience']) # Numerical
            pokemon_data.append(pokemon['Attack']) # Numerical
            pokemon_data.append(pokemon['Defense']) # Numerical
            pokemon_data.append(pokemon['Speed']) # Numerical
            pokemon_data.append(pokemon['Special']) # Numerical
            pokemon_data.append(pokemon['HP EV']) # Numerical
            pokemon_data.append(pokemon['Attack EV']) # Numerical
            pokemon_data.append(pokemon['Defense EV']) # Numerical
            pokemon_data.append(pokemon['Speed EV']) # Numerical
            pokemon_data.append(pokemon['Special EV']) # Numerical
            pokemon_data.append(pokemon['Attack IV']) # Numerical
            pokemon_data.append(pokemon['Defense IV']) # Numerical
            pokemon_data.append(pokemon['Speed IV']) # Numerical
            pokemon_data.append(pokemon['Spec IV']) # Numerical
            pokemon_data.append(pokemon['Move PPs']) # Numerical
            self.flat_data['Party'].append(pokemon_data)

        self.flat_data['Opponent Pokemon'] = []

        for pokemon in self.data['Opponent Pokemon']:
            pokemon_data = []
            pokemon_data.append(pokemon['Pokemon']) # Categorical
            pokemon_data.append(pokemon['Current HP']) # Numerical
            pokemon_data.append(pokemon['Max HP']) # Numerical
            pokemon_data.append(pokemon['Level']) # Numerical
            pokemon_data.append(pokemon['Status']) # Categorical
            pokemon_data.append(pokemon['Types']) # Tuple, Categorical
            pokemon_data.append(pokemon['Moves']) # List, Categorical
            pokemon_data.append(pokemon['Attack']) # Numerical
            pokemon_data.append(pokemon['Defense']) # Numerical
            pokemon_data.append(pokemon['Speed']) # Numerical
            pokemon_data.append(pokemon['Special']) # Numerical
            pokemon_data.append(pokemon['HP EV']) # Numerical
            pokemon_data.append(pokemon['Attack IV']) # Numerical
            pokemon_data.append(pokemon['Defense IV']) # Numerical
            pokemon_data.append(pokemon['Speed IV']) # Numerical
            pokemon_data.append(pokemon['Spec IV']) # Numerical
            pokemon_data.append(pokemon['Move PPs']) # Numerical
            self.flat_data['Opponent Pokemon'].append(pokemon_data)

        self.flat_data['Clock'] = self.data['Clock'] # Tuple, Numerical
