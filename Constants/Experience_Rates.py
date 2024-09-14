import pandas as pd
import time
import json
import Pokemon_Rates as PR

'''
Function reads the CSV file and creates dictionaries based on total exp needed
    to reach a certain level.

Various experience rates are saved as json files.

Can load the dictionaries through json

Dictionary keys and values are all integers.
'''

def create_exp_tables():
    start_time = time.time()
    file_path = 'Experience Rate Charts.csv'
    df = pd.read_csv(file_path)

    # Convert to dictionaries
    slow = dict(zip(df['Level'], df['Slow']))
    med_slow = dict(zip(df['Level'], df['Medium Slow']))
    med_fast = dict(zip(df['Level'], df['Medium Fast']))
    fast = dict(zip(df['Level'], df['Fast']))

    print("Time Elapsed: ", time.time() - start_time)


    with open('Slow.json', 'w') as file:
        json.dump(slow, file, indent=4)

    with open("MedSlow.json", 'w') as file:
        json.dump(med_slow, file, indent=4)

    with open("MedFast.json", 'w') as file:
        json.dump(med_fast, file, indent=4)

    with open("Fast.json", 'w') as file:
        json.dump(fast, file, indent=4)
    

def load_exp_rates():
    '''
    Returns experience rate dictionaries.

    Keys are the levels.

    Values are the total exp needed to achieve said level.
    '''
    
    with open("Slow.json", 'r') as file:
        slow = json.load(file)

    with open("MedSlow.json", 'r') as file:
        med_slow = json.load(file)

    with open("MedFast.json", 'r') as file:
        med_fast = json.load(file)

    with open("Fast.json", 'r') as file:
        fast = json.load(file)

    return slow, med_slow, med_fast, fast


def get_exp_at_level(pokeID, level, rates):
    '''
    pokeID is the pokedex ID for the pokemon

    level will grab the exp needed to achieve the chosen level

    rates should be a list [slow, med_slow, med_fast, fast] of dictionaries
    '''
    
    rate = PR.poke_rates[pokeID]

    if rate == 1:
        return rates[0][level]
    elif rate == 2:
        return rates[1][level]
    elif rate == 3:
        return rates[2][level]
    else:
        return rates[3][level]
