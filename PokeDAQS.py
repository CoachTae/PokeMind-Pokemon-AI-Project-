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
