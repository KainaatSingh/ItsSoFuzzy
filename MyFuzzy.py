#!/usr/bin/env python3

#from FuzzData import *
from subprocess import *
from argparse import *
from pickle import *
import os
from sys import path
path.append('seed/')
from GenerateSeed import *
path.append('testcases')
from BitFlip import *
from ByteArithmetic import *

path.append('coverage/')
import Cov
import LineCov

'''
    * Generate the input string for the passed length
    *
    *
    * @param integer len_string      length of input string to be generated
    * @return string
'''


def get_Input(length, mutation, seed, string):
    strings = [] 
            
    switcher = {
            'flip_one': BitFlip.flip_one,
            'flip_one_restore': BitFlip.flip_one_restore,
            'flip_all': BitFlip.flip_all,
            'flip_two': BitFlip.flip_two,
            'flip_two_restore': BitFlip.flip_two_restore,
            'byte_arithmetic': ByteArithmetic.byte_arithmetic,
            'byte_arithmetic_restore': ByteArithmetic.byte_arithmetic_restore,
            'byte_swap': ByteArithmetic.byte_swap
            }

    func = switcher.get(mutation)
    strings[:] = func(length, seed, string)
    
    return strings


def random_mutation(length, mutation, seed, string):

     switcher = {
            BitFlip.flip_one,
            BitFlip.flip_all,
            BitFlip.flip_two,
            ByteArithmetic.byte_arithmetic,
            ByteArithmetic.byte_swap
            }

     func = choice(tuple(switcher))
     input_string = func(length, seed, string)
     return input_string

def check_inputfile(filename):
    if(os.path.isfile(args.PROGRAM_PATH)==0):
            print("ERROR:   Invalid Input Program Path '%s'\nPlease enter valid program path" % args.PROGRAM_PATH)
            exit(0)
    else:
        return


def check_outputfile(filename):
    os.chdir('output/')
    if(os.path.isfile(args.OUTPUT_FILE)==0):
            try:
                open(args.OUTPUT_FILE, "w+")
            except OSError as err:
                print("OSError: {0}".format(err))

    elif(os.stat(args.OUTPUT_FILE).st_size!=0):
            try:
                open(args.OUTPUT_FILE,"w").close()
            except OSError as err:
                print("OSError: {0}".format(err))

    os.chdir('../')
    return


def check_mutation(name):
    mutation_method = ["random", "flip_one", "flip_one_restore", "flip_all", "flip_two", "flip_two_restore", "byte_arithmetic", "byte_arithmetic_restore", "byte_swap"]
    
    if args.MUTATION_OPTION in mutation_method:
        return
    else:
        print("ERROR:   Invalid Mutation Method!!")
        exit(0)


def check_seed(name):
    seed_method = ["random_printable", "random", "exhaustive"]
    if args.SEED_OPTION in seed_method:
       return
    else:
       print("ERROR:   Invalid Seed Generation Method!!")
       exit(0)


'''
    * Main function
    * 
    * Run the input program with input string
'''
if __name__ == "__main__":
    
    parser = ArgumentParser()
    parser.add_argument("PROGRAM_PATH", help="Enter the program path", type=str)
    #parser.add_argument("NUM_TEST_CASES", help="Enter number of test cases to run", type=int)
    #parser.add_argument("LEN_INPUT_STRING", help="Enter length of input string", type=int)
    parser.add_argument("-o", action="store", dest="OUTPUT_FILE", default='output.txt', help="Enter output file name", type=str)  
    parser.add_argument("-m", action="store", dest="MUTATION_OPTION", default='random', help="Enter mutation method. See Documentation for meaning:\nrandom\nflip_one\nflip_one_restore\nflip_all\nflip_two\nflip_two_restore\nbyte_arithmetic\nbyte_arithmetic_restore\nbyte_swap", type=str)  
    parser.add_argument("-s", action="store", dest="SEED_OPTION", default="random_printable", help="Enter seed generation method. See Documentation for meaning:\nrandom_printable\nrandom\nexhaustive", type=str) 
    parser.add_argument("-c", action="store", dest="COVERAGE", default='path', help="Enter coverage type:\npath\nblock", type=str)
    
    args = parser.parse_args()

    
    try:
        check_inputfile(args.PROGRAM_PATH)
        check_outputfile(args.OUTPUT_FILE)
        check_mutation(args.MUTATION_OPTION)
        check_seed(args.SEED_OPTION)
       
        if(args.PROGRAM_PATH.endswith("p")):
                OUT_FILE = args.PROGRAM_PATH.replace(".cpp", "")
        elif(args.PROGRAM_PATH.endswith("c")):
                OUT_FILE = args.PROGRAM_PATH.replace(".c", "")
        
        os.chdir('output/')
        with open(args.OUTPUT_FILE, "a") as fo:
            os.chdir('../')
            length = 1
            seeds = set()            
            if args.MUTATION_OPTION == "random":
                    seeds = create_seed()
            
            if args.COVERAGE == "path":
                    paths_seen = set()
 
            #while True: 
            for i in range(0,10):
                input_strings = []

                if args.MUTATION_OPTION == "random":
                    args.SEED_OPTION = "none"
                    random_seed = pick_seed(seeds)
                    input_strings.append(random_mutation(length, args.MUTATION_OPTION, args.SEED_OPTION, random_seed))
                    
                else:
                    input_strings[:] = get_Input(length, args.MUTATION_OPTION, args.SEED_OPTION, "")

                
                for i in range(0, len(input_strings)):
                    temp_string = input_strings[i]
                     
                    Cov.compile_program(args.PROGRAM_PATH, OUT_FILE)
                    result = run([OUT_FILE], stdout=DEVNULL, stderr=DEVNULL, input=temp_string, encoding='utf-8')
                    Cov.generate_gcov(args.PROGRAM_PATH)                 
                    Cov.clean_gcov(OUT_FILE)

                    if args.COVERAGE == "path":
                        coverage = frozenset(LineCov.get_line_coverage(args.PROGRAM_PATH))
                        
                    #exhaustive
                    #for j in range(0, len(temp_string)):
                     #   result = run([args.PROGRAM_PATH], stdout=DEVNULL, stderr=DEVNULL, input=temp_string[j], encoding='ascii')
                    if(result.returncode != 0 and result.returncode != -1):
                           # print(args.MUTATION_OPTION)
                            fo.write("Input String causing crash:   %s\n  Return code is:     %d\n\n" %(temp_string, result.returncode))
                            temp_string = ByteArithmetic.add_character(temp_string)
                            if args.MUTATION_OPTION == "random":
                                continue
                            else:
                                seeds = add_seed(seeds, temp_string)

                    elif(result.returncode == -1):
                        continue
                    
                    elif coverage not in paths_seen:
                            paths_seen.add(coverage)
                            seeds = add_seed(seeds, temp_string)

                        #print(temp_string)
                            print(coverage)
                            print(paths_seen)

                        

           #     print(length)
                length += 1

    except KeyboardInterrupt:
           print("\nyou pressed ctrl+c to quit")

'''
#command line arguments
for i in range(0, args.NUM_TEST_CASES):
    input_string = data(args.LEN_INPUT_STRING)
    result = run([args.PROGRAM_PATH,input_string , "-h"])     #, stdout=PIPE)
    print(result.stdout)
    print(result.returncode)
    '''
