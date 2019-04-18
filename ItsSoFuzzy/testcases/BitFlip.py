#!/usr/bin/env python3


from random import randrange, randint, choice
from sys import path
path.append('../seed/')
from GenerateSeed import *


class BitFlip():

    
    def select_seed(self, option):
        
        switcher = {
                'random_printable': random_printable_seed,
                'random': random_seed,
                'exhaustive': exhaustive_seed
                }
        func = switcher.get(option)
        return func
    
    
    def flip_one(length, option, string):
        
        obj = BitFlip()
        
        if option == 'none':
            mutated_inputstring = ""
            input_list = []
            
            for letter in string:
                input_list.append(letter)
            
            index = randrange(len(input_list))
            bit = 1 << randrange(8)
            input_list[index] = chr(ord(input_list[index]) ^ bit)
            
            mutated_inputstring = ''.join(input_list)
           
            return mutated_inputstring

        else:    
            seed_func = obj.select_seed(option)
            input_string = ""
            input_string = seed_func(length)

            input_list = []
            for letter in input_string:
                input_list.append(letter)

            mutated_inputlist = []
            mutated_inputlist.append(input_string)
            for i in range(0, len(input_list)):
                temp_character = input_list[i]
                
                bit = 1 << randint(0, 8)
                new_character = chr(ord(temp_character) ^ bit)
                input_list[i] = new_character
                
                mutated_string = ''.join(input_list)
                mutated_inputlist.append(mutated_string)
                mutated_string = ""
       
            return mutated_inputlist

    
    def flip_one_restore(length, option, string):
        
        obj = BitFlip()

        seed_func = obj.select_seed(option)

        input_string = ""
        input_string = seed_func(length)

        input_list = []
        for letter in input_string:
            input_list.append(letter)

        mutated_inputlist = []
        temp_list = []
        mutated_inputlist.append(input_string)
        for i in range(0, len(input_list)):
            temp_list[:] = input_list
            temp_character = temp_list[i]
            
            bit = 1 << randint(0, 8)
            new_character = chr(ord(temp_character) ^ bit)
            temp_list[i] = new_character
                
            mutated_string = ''.join(temp_list)
            mutated_inputlist.append(mutated_string)
            mutated_string = ""

        return mutated_inputlist

    
    def flip_all(length, option, string):
        
        obj = BitFlip()
        
        if option == 'none':
            mutated_inputstring = ""
            input_list = []
            for letter in string:
                input_list.append(letter)

            for i in range(0, len(input_list)):
                for j in range(0,8):
                    bit = 1 << j
                    input_list[i] = chr(ord(input_list[i]) ^ bit)
            
            mutated_inputstring  = ''.join(input_list)
            
            return mutated_inputstring

        else:
            seed_func = obj.select_seed(option)

            input_string = ""
            input_string = seed_func(length)

            input_list = []
            for letter in input_string:
                input_list.append(letter)

            mutated_inputlist = []
            temp_list = []
            mutated_inputlist.append(input_string)
            for i in range(0, len(input_list)):
                temp_list[:] = input_list
                temp_character = temp_list[i]
            
            for j in range(0,8):   
                bit = 1 << j
                new_character = chr(ord(temp_character) ^ bit)
                temp_list[i] =  new_character
                mutated_string = ''.join(temp_list)
                mutated_inputlist.append(mutated_string)
                mutated_string = ""
            
            return mutated_inputlist



    def flip_two(length, option, string):
        
        obj = BitFlip()

        if option == 'none':
            mutated_inputstring = ""
            input_list = []

            for letter in string:
                input_list.append(letter)

            index = randrange(len(input_list))
            bit1 = 1 << randrange(8)
            bit2 = 1 << randrange(8)
            while bit1 == bit2:
                    bit2 = randint(0,8)

            input_list[index] = chr(ord(input_list[index]) ^ bit1)
            input_list[index] = chr(ord(input_list[index]) ^ bit2)

            mutated_inputstring = ''.join(input_list)
            
            return mutated_inputstring

        else:
            seed_func = obj.select_seed(option)

            input_string = ""
            input_string = seed_func(length)

            input_list = []
            for letter in input_string:
                input_list.append(letter)

            mutated_inputlist = []
            mutated_inputlist.append(input_string)
            for i in range(0, len(input_list)):
                temp_character = input_list[i]

                bit_1 = randint(0, 8)
                bit_2 = randint(0,8)
                while bit_1 == bit_2:
                    bit_2 = randint(0,8)
                bit_1 = 1 << bit_1
                bit_2 = 1 << bit_2

                temp_character = chr(ord(temp_character) ^ bit_1)
                new_character = chr(ord(temp_character) ^ bit_2)
                input_list[i] = new_character

                mutated_string = ''.join(input_list)
                mutated_inputlist.append(mutated_string)
                mutated_string = ""

            return mutated_inputlist

    
    def flip_two_restore(length, option, string):
        
        obj = BitFlip()

        seed_func = obj.select_seed(option)

        input_string = ""
        input_string = seed_func(length)

        input_list = []
        for letter in input_string:
            input_list.append(letter)

        mutated_inputlist = []
        temp_list = []
        mutated_inputlist.append(input_string)
        for i in range(0, len(input_list)):
            temp_list[:] = input_list
            temp_character = temp_list[i]

            bit_1 = randint(0, 8)
            bit_2 = randint(0,8)
            while bit_1 == bit_2:
                bit_2 = randint(0,8)
            bit_1 = 1 << bit_1
            bit_2 = 1 << bit_2
            temp_character = chr(ord(temp_character) ^ bit_1)
            new_character = chr(ord(temp_character) ^ bit_2)
            temp_list[i] = new_character

            mutated_string = ''.join(temp_list)
            mutated_inputlist.append(mutated_string)
            mutated_string = ""

        return mutated_inputlist

