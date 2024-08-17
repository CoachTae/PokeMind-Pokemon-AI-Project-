from random import randrange
import random as rand
import sys

class Hands:
    def __init__(self, pyboy):
        self.pyboy = pyboy
        self.previous = None


    def press_a(self):
        self.pyboy.button('a')

    def press_b(self):
        self.pyboy.button('b')

    def press_up(self):
        self.pyboy.button('up', 5)
        self.previous = 'up'

    def press_down(self):
        self.pyboy.button('down', 5)
        self.previous = 'down'

    def press_right(self):
        self.pyboy.button('right', 5)
        self.previous = 'right'

    def press_left(self):
        self.pyboy.button('left', 5)
        self.previous = 'left'

    def press_start(self):
        self.pyboy.button('start')

    def press_select(self):
        self.pyboy.button('select')

    def press_nothing(self):
        pass

    def press_random(self):
        choice = randrange(0,9)
        while True:
            if choice == 0:
                self.press_a()
                break

            elif choice == 1:
                self.press_b()
                break

            elif choice == 2 and self.previous != 'down':
                self.press_up()
                break

            elif choice == 3 and self.previous != 'up':
                self.press_down()
                break

            elif choice == 4 and self.previous != 'left':
                self.press_right()
                break

            elif choice == 5 and self.previous != 'right':
                self.press_left()
                break

            elif choice == 6:
                self.press_start()
                break

            elif choice == 7:
                self.press_select()
                break

            elif choice == 8:
                self.press_nothing()
                break

            elif self.previous == 'up':
                choice = randrange(3, 6)

            elif self.previous == 'down':
                choice = rand.choice([2, 4, 5])

            elif self.previous == 'right':
                choice = rand.choice([2,3,5])

            elif self.previous == 'left':
                choice = randrange(2,5)

    def num_to_action(self, number):
        if number == 0:
            self.press_a()
        elif number == 1:
            self.press_b()
        elif number == 2:
            self.press_up()
        elif number == 3:
            self.press_down()
        elif number == 4:
            self.press_left()
        elif number == 5:
            self.press_right()
        elif number == 6:
            self.press_start()
        elif number == 7:
            self.press_select()
        elif number == 8:
            self.press_nothing()
        else:
            print('Message from PokeMind_Commands.py')
            print('Bad argument for num_to_actions method.')
            print(f'Argument given: {number}.')
            print("Arguments expected to be between 0 and 8 inclusive.")
            sys.exit()

    def name_the_action(self, number):
        if number == 0:
            return "A"
        elif number == 1:
            return "B"
        elif number == 2:
            return "Up"
        elif number == 3:
            return "Down"
        elif number == 4:
            return "Left"
        elif number == 5:
            return "Right"
        elif number == 6:
            return "Start"
        elif number == 7:
            return "Select"
        elif number == 8:
            return "Nothing"

    def random_weighted(self, weighted_move, move_weight):
        '''
        weighted_move should be a number between 0 and 8 (inclusive)

        move_weight should be 0 <= weight <= 1
        '''
        
        choice = rand.random()
        moves = range(0,9)
        weights = [(1 - move_weight) / 8] * 9
        weights[weighted_move] = move_weight

        cumulative = 0
        for i, weight in enumerate(weights):
            cumulative += weight
            if choice <= cumulative:
                self.num_to_action(moves[i])
                break
        
        
        
