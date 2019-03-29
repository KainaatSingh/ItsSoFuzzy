#!/usr/bin/env python3

from random import randrange, randint
from sys import path
path.append('seed/')
from GenerateSeed import *


class ByteArithmetic():

    
    def select_seed(self, option):

        switcher = {
                'random_printable': random_printable_seed,
                'random': random_seed,
                'exhaustive': exhaustive_seed
                }
        func = switcher.get(option)
        return func


    def byte_arithmetic(length, option, string):

        obj = ByteArithmetic()
        
        if option == 'none':
            
            r = randint(0,35)
            mutated_inputstring = ""
            input_array = bytearray(string, 'utf-8')


            index = randrange(len(input_array))
            input_array[index] = input_array[index]+r

        
            mutated_inputstring  = "".join( chr(x) for x in input_array)
            
            return mutated_inputstring

        else:

            seed_func = obj.select_seed(option)

            input_string = ""
            input_string = seed_func(length)

            mutated_inputlist = []
            mutated_inputlist.append(input_string)
            mutated_inputarray = bytearray(input_string, 'utf-8')
        
            for i in range(0, len(input_string)): 

                r = randint(0,35)

                new_character = mutated_inputarray[i]+r
                mutated_inputarray[i] = new_character

                new_array = "".join( chr(x) for x in mutated_inputarray)
                mutated_inputlist.append(new_array)

            return mutated_inputlist

    
    
    def byte_arithmetic_restore(length, option, string):

        obj = ByteArithmetic()
       
        seed_func = obj.select_seed(option)

        input_string = ""
        input_string = seed_func(length)

        mutated_inputlist = []
        mutated_inputlist.append(input_string)
        for i in range(0, len(input_string)):
            mutated_inputarray = bytearray(input_string, 'utf-8')
            temp_array = []

            r = randint(0,35)

            temp_array[:] = mutated_inputarray

            new_character = temp_array[i]+r
            temp_array[i] = new_character

            new_array = "".join( chr(x) for x in temp_array)
            del temp_array[:]
            mutated_inputlist.append(new_array)
        
        return mutated_inputlist


    def byte_swap(length, option, string):

        obj = ByteArithmetic()

        if option == 'none':
            
            mutated_inputstring = ""

            mutated_inputstring = ''.join([string[x:x+2][::-1] for x in range(0, len(string), 2)])

            return mutated_inputstring


        else:
            
            seed_func = obj.select_seed(option)

            input_string = ""
            input_string = seed_func(length)

            mutated_inputlist = []
            mutated_inputlist.append(input_string)
            new_string = input_string
            for i in range(2, len(input_string)-1):
                new_string = ''.join([ new_string[x:x+i][::-1] for x in range(0, len(new_string), i)])
            
                mutated_inputlist.append(new_string)

            return mutated_inputlist

    
    def add_character(string):
        
        random_character = chr(randrange(0,128))
        mutated_string = ""
        temp_list = []
        
        for letter in string:
                temp_list.append(letter)

        index = randrange(len(temp_list))
        temp_list.insert(index, random_character)

        mutated_string = ''.join(temp_list)

        return mutated_string
