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
import json

with open('RandomArmyRewards.json', 'r') as file:
    Rewards = json.load(file)

pprint.pprint(Rewards)
