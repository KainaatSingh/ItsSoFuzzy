#!/usr/bin/env python3


from random import randrange, randint, choice
from string import printable
from itertools import product



def random_printable_seed(length):
        
        string = ""
        
        for i in range(0, length):
            string += chr(randrange(0,128))

        return string

    
def random_seed(length):
        
        string = ""

        for i in range(0, length):
            string += chr(randrange(0,256))
        
        return string

    
def exhaustive_seed(length):
        
        dictionary = printable

        strings = [''.join(i) for i in product(dictionary, repeat=length)]

        return strings

    
def create_seed():
        
        #print('create_seeds')
        
        seeds = set()
        
        for i in range(0,10):
            length = randrange(1,70)
            seeds.add(random_printable_seed(length))

        return seeds

    
def pick_seed(seeds):
        #print('picking')
        return choice(tuple(seeds))

    
def add_seed(seeds, string):
        
        seeds.add(string)

        return seeds
