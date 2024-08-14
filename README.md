# PokeMind (Pokemon AI Project)
## Introduction
Being self taught with code and ML/AI, I wanted to find a fun project that, as I learned concepts in ML/AI, I could immediately start putting them to use and iteratively improve it until it could do some grand task. That grand task, I figured, would be to play a Pokemon game. Inspired by a youtube video by a lad named pdubs, I was introduced to PyBoy and a relatively easy way to get an agent to interact with the game. And so my adventure began.

## Structure
The Data Acquisition System, or DAQ, and aptly renamed PokeDAQS, is the class used to pull the game state from the emulated RAM from PyBoy. It utilizes the PokeDAQS_Support package full of classes that pull various types of information about the game. The PokeDAQS is just a way to combine all of these different objects into 1 for a seamless method of collecting and storing various data types in a (hopefully) intuitive form.

The name "PokeMind", while generally referring to this project, also has its name appear in the code. Originally used as a placeholder for the game wrapper object while I was testing things out, I ended up keeping that name-object combination for no other reason than I couldn't think of another name at the time, and now it's just become convention.

The Commands module is used to contain various different forms and methods of pressing buttons.

The Rewards module loads and saves (optional) game current reward states into a JSON file. It attempts to load this file each time to resume where it left off. This will likely be changed in the near future.

Rewards are based off of tiles seen (to encourage exploration), time passing (negative reward to encourage speed and efficiency), number of unique pokemon captured, levels gained, badges, and number of event-flags triggered.

## Purely Random Moves
First I tried a "model" that did purely random movements. There was nothing else to this. Within 1.5-2 game-hours, we got our first pokemon (J, the Charmander) and even beat our rival! We then ran around the town mindlessly, occasionally touching Route 1. Charmander hit lvl 61 by the time I intervened for the model's first update.

I realized that, while taking steps (24 frames per step) all inputs except for the start button would be blocked off and not allowed through. This means that, for each step, we'd have 24 chances to roll "start", causing us to pause after the step. This takes up a lot of time being on the pause menu that often. My fix was to only allow inputs every 24 frames. This had the unintended effect of allowing J to evolve to a Charmeleon, and again into a Charizard. After all, we have 1/24 the chance of hitting B during evolution.

I also implemented into the Commands' "random move" method, logic that denies us the ability to make a directional move if the move immediately prior was in the opposite direction. So if our last move was Up, we cannot go Down. Instead, if we roll Down, we will roll another random directional input instead.

J perished as a lvl 69 Charizard when my save function was coded improperly and it corrupted the save file, destroying it. He was the best Charizard.

## Random Army
The Random Army method is a primitive model that I developed as something to do while I studied more RL algorithms, but before I had the ability to build any yet. So I came up with my own. An agent plays the game. The agent needs to make a move. N*9 subagents load the main agent's game state and make one of the 9 possible moves (nothing is considered a move). After that first move, they do k random moves after that. After the random moves, the subagents' total rewards are added, and grouped by their first move. The main agent then takes the action corresponding to the first action of the subagent group that had the highest reward. So if Up was the group that accumulated the most reward, the main agent would go up.

This allowed me to practice parallelization as well which was super neat to get working, and speeds things up a lot!

We had a nearly perfectly optimal start. We left our beginning house in an almost perfectly optimal path, beelined to Gary's house just to poke our heads in for 1 second to get the vision rewards for the new place, then immediately left and triggered the Oak event.

This was seeming very promising, as we got our first Pokemon within 3 game-minutes, about 30x faster than the purely random model. But that's where the hype ended. We've since been trapped in Oak's lab, refusing to fight our rival. I must figure this out before I'm capable of building a real RL model!