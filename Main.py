from pyboy import PyBoy
import time
import numpy as np
import threading # Used for debugging by executing a function every X seconds
import PokeDAQS
import pprint
import PokeMind_Commands
import PokeMind_Rewards
import Simple_Algorithms as simple
import sys


# Given by someone in the PokeRL discord
# Shows how to make a headless version of the game
# Headless allows AI to parallelize training without opening a bunch of windows
'''def make_env(gb_path, headless=True, quiet=False, **kwargs):
    gb_path='pokemon_red.gb'
    game = PyBoy(
        gb_path,
        debugging=False,
        window_type='headless' if headless else 'SDL2',
        hide_window=quiet,
        **kwargs,
    )'''

#if __name__ == "__main__":
#    simple.random_army()
#    sys.exit()

# Create PyBoy Object
pyboy = PyBoy('PokemonBlue.gb')

# Set game speed
pyboy.set_emulation_speed(0)

# Implement game wrapper
PokeMind = pyboy.game_wrapper

# Load State
game_state = open('Fresh Start.gb.state', 'rb')
pyboy.load_state(game_state)


# Create Command Object for inputs
Hands = PokeMind_Commands.Hands(pyboy)

# Create DAQ object
PokeDAQ = PokeDAQS.DAQ(pyboy, PokeMind)

# Create Rewards objects
Rewards = PokeMind_Rewards.Rewards(pyboy, PokeMind)

# Get data
state = PokeDAQ.get_game_state()

#-----------DEBUGGING TOOL------------------------------------------

# Debug function run every X seconds
def test_func(pyboy):
    state = PokeDAQ.get_game_state()
    #Rewards.calculate_fitness(state)
    print(state['Screen Image'].size)


def run_every_interval(interval, test_func, pyboy):
    next_call = time.time()
    while True:
        test_func(pyboy)
        next_call += interval
        time.sleep(next_call - time.time())

thread = threading.Thread(target=run_every_interval, args=(10, test_func, pyboy))
thread.start()
#------------------PYBOY TICK LOOP---------------------------------

while pyboy.tick():
    #Hands.press_random()
    pass
pyboy.stop()
