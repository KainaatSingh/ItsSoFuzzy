#!/usr/bin/env python3


from random import randrange, randint
from string import printable
from itertools import product

class GenerateSeed():


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
