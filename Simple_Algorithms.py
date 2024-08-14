from pyboy import PyBoy
import time
import numpy as np
import threading # Used for debugging by executing a function every X seconds
import PokeDAQS
import pprint
import PokeMind_Commands
import PokeMind_Rewards
from multiprocessing import Pool
import random
import torch
import sys
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor


def purely_random():
    '''
    Inputs are purely random with no
    '''
    # Create PyBoy Object
    pyboy = PyBoy('PokemonBlue.gb')

    # Set game speed
    pyboy.set_emulation_speed(0)

    # Implement game wrapper
    PokeMind = pyboy.game_wrapper

    # Load State
    game_state = open('PurelyRandom.state', 'rb')
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
        save = open('PurelyRandom.state', 'wb')
        pyboy.save_state(save)


    def run_every_interval(interval, test_func, pyboy):
        next_call = time.time()
        while True:
            test_func(pyboy)
            next_call += interval
            time.sleep(next_call - time.time())

    thread = threading.Thread(target=run_every_interval, args=(10, test_func, pyboy))
    thread.start()
    #------------------PYBOY TICK LOOP---------------------------------
    while pyboy.tick(24, True):
        Hands.press_random()
    pyboy.stop()











#---------------------------SUPPORT FUNCTIONS FOR THE ARMY FUNCTION--------------------
def make_env(gb_path, headless=True):
    # Create 1 pyboy object to load the game       
    return PyBoy(gb_path,
                 window='null',
                 debug=False,
                 no_input=False,
                 log_level='CRITICAL')

def parallel_agent_run(action, num_steps, gb_path, device):
    try:
        # Runs an instance of a subagent with a given first action
            # comes back with the reward for that action
        reward = run_instance(action, num_steps, gb_path, device)

        return (action, reward)
        
    except Exception as e:
        print(f"Error in subagent with action {action}: {e}")
        

def run_instance(action, num_steps, gb_path, device):         
    # Create a headless pyboy object
    pyboy = make_env(gb_path)
    pyboy.set_emulation_speed(0)   
    PokeMind = pyboy.game_wrapper        
    game_state_file = open('RandomArmy.state', 'rb')            
    pyboy.load_state(game_state_file)
    Hands = PokeMind_Commands.Hands(pyboy)
    Rewards = PokeMind_Rewards.Rewards(pyboy, PokeMind)
    PokeDAQ = PokeDAQS.DAQ(pyboy, PokeMind)
    
    # Perform initial action
    Hands.num_to_action(action)

    pyboy.tick(24, True)

            
    # Take additional random steps
    try:
        for _ in range(num_steps - 1):
            state = PokeDAQ.get_game_state()
            Rewards.calculate_fitness(state, save=False)
            Hands.press_random()
            pyboy.tick(24, True)
        pyboy.stop(False)
        return Rewards.fitness
    except AttributeError as e:
        with open('Troubleshooting Log.txt', 'a') as file:
            file.write(f'{e}.\n')

def process_results(result):
    global action_rewards, results_received
    action, reward = result
    action_rewards[action] += reward
    results_received += 1

#--------------------END OF SUPPORT FUNCTIONS FOR ARMY FUNCTION------------------------









def random_army():
    '''
    1 main agent
    900 subagents get deployed
        100 subagents per possible action (including doing nothing)
        Each subagent then does 49 random steps
    After 50 steps for each subagent, add their rewards
    The 100-group with the most total reward wins
    Winning subgroup casts their first move onto agent A
    '''
    
    global action_rewards, results_received
    
    gb_path = 'PokemonBlue.gb'
    num_steps = 50
    num_subagents = 10
    #device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    
    # Create primary agent
    MainAgent = PyBoy(gb_path)
    MainAgent.set_emulation_speed(0)
    Main_PokeMind = MainAgent.game_wrapper
    game_state = open('RandomArmy.state', 'rb')
    MainAgent.load_state(game_state)
    Main_Hands = PokeMind_Commands.Hands(MainAgent)
    Main_PokeDAQ = PokeDAQS.DAQ(MainAgent, Main_PokeMind)
    Main_Rewards = PokeMind_Rewards.Rewards(MainAgent, Main_PokeMind)

    #mp.set_start_method('spawn') # Instead of forking processes which doesn't end them
    
    move_counter = 0
    while MainAgent.tick(24, True):
        # Save the current state
        with open('RandomArmy.state', 'wb') as file:
            MainAgent.save_state(file)
        
        # Create list of first actions for each agent
        first_moves = []
        for j in range(9):
            for i in range(num_subagents):
                first_moves.append(j)

        # Create a list of parameters for each agent
        first_actions = [(action, num_steps, gb_path, 'cpu') for action in first_moves]
        
        
        # Collect results
        action_rewards = {action: 0 for action in range(0,9)}
        results_received = 0

        # Attempt at multiprocessing
        pool = Pool()
        results = pool.starmap(parallel_agent_run, first_actions)
        pool.close()
        pool.join()
        
        '''results = []
        for action_args in first_actions:
            result = parallel_agent_run(*action_args)
            action_rewards[result[0]] += result[1]'''

        for result in results:
            action_rewards[result[0]] += result[1]
        
        #print(*action_rewards.values(), sep='\t')
        #print(Main_Rewards.vision)
        #print(Main_Rewards.time_penalty/60)
        #print(Main_Rewards.flags_reward*1000)
        #print(Main_Rewards.pokedex_reward*1000)
        #print(Main_Rewards.badge_reward*50000)
        #print(Main_Rewards.level_reward*100)
        #sys.exit()
        
        # Select the best action
        # First, see if all values were equal. If so, do random move
        max_reward = max(action_rewards.values())
        min_reward = min(action_rewards.values())
        if max_reward - min_reward < 2:
            Main_Hands.press_random()
            print("Best action: Random")
        else:
            best_action = max(action_rewards, key=action_rewards.get)

            print("Best action: ", Main_Hands.name_the_action(best_action))
            # Primary agent takes action
            Main_Hands.num_to_action(best_action)
        
        move_counter += 1

        if move_counter == 10:
            with open("RandomArmy.state", 'wb') as file:
                MainAgent.save_state(file)
            move_counter = 0

    MainAgent.stop()
