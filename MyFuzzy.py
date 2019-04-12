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
from time import time, asctime
path.append('coverage/')
import Cov
import LineCov
import BlockCov

'''
    * Generate the input string for the passed length
    *
    *
    * @param integer len_string      length of input string to be generated
    * @return string
'''

def get_Input(length, mutation, seed, string):
    input_string = []

    switcher = {
            'flip_one': BitFlip.flip_one,
            'flip_all': BitFlip.flip_all,
            'flip_two': BitFlip.flip_two,
            'byte_arithmetic': ByteArithmetic.byte_arithmetic,
            'byte_swap': ByteArithmetic.byte_swap
            }

    func = switcher.get(mutation)
    input_string = func(length, seed, string)
   
    return input_string


def get_Input_Exhaustive(length, mutation, seed, string):
    input_strings = [] 
            
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
    input_strings[:] = func(length, seed, string)
    
    return input_strings


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
    mutation_method = ["random", "flip_one", "flip_all", "flip_two", "byte_arithmetic", "byte_swap"]
    
    if name in mutation_method:
        return
    else:
        print("ERROR:   Invalid Mutation Method!!")
        exit(0)


def check_seed(name):
    seed_method = ["random_printable", "random", "exhaustive"]
    if name in seed_method:
       return
    else:
       print("ERROR:   Invalid Seed Generation Method!!")
       exit(0)

def check_coverage(name):
    coverage_method = ["path", "block"]
    
    if name in coverage_method:
       return
    else:
       print("ERROR:   Invalid Code Coverage Method!!")
       exit(0)

def check_exhaustive(name):

    mutation_method = ["", "flip_one", "flip_one_restore", "flip_all", "flip_two", "flip_two_restore", "byte_arithmetic", "byte_arithmetic_restore", "byte_swap"]

    if name in mutation_method:
        return
    else:
        print("ERROR:   Invalid Exhaustive Mutation Method!!")
        exit(0)

def check_iterations(iterations):

    if iterations < 10:
        print("Minimum number of iterations should be 100000")
        exit(0)
    else:
        return


'''
    * Main function
    * 
    * Run the input program with input string
'''
if __name__ == "__main__":
    
    parser = ArgumentParser()
    parser.add_argument("PROGRAM_PATH", help="Enter the absolute program path", type=str)
    #parser.add_argument("NUM_TEST_CASES", help="Enter number of test cases to run", type=int)
    #parser.add_argument("LEN_INPUT_STRING", help="Enter length of input string", type=int)
    parser.add_argument("TEST_CASES", help="Enter absolute path of file containing testcases", type=str)
    parser.add_argument("-o", action="store", dest="OUTPUT_FILE", default='output.txt', help="Enter output file name", type=str)  
    parser.add_argument("-m", action="store", dest="MUTATION_OPTION", default='random', help="Enter mutation method. See Documentation for meaning:\nrandom\nflip_one\nflip_all\nflip_two\nbyte_arithmetic\nbyte_swap", type=str)  
    parser.add_argument("-s", action="store", dest="SEED_OPTION", default="random_printable", help="Enter seed generation method. See Documentation for meaning:\nrandom_printable\nrandom\nexhaustive", type=str) 
    parser.add_argument("-c", action="store", dest="COVERAGE", default='path', help="Enter coverage type:\npath\nblock", type=str)
    parser.add_argument("-e", action="store", dest="EXHAUSTIVE_MUTATION", default='', help="Enter mutation method. See Documentation for meaning:\nflip_one\nflip_one_restore\nflip_all\nflip_two\nflip_two_restore\nbyte_arithmetic\nbyte_arithmetic_restore\nbyte_swap", type=str) 
    parser.add_argument("-i", action="store", dest="ITERATIONS", default=10, help="Enter the number of iterations for each run", type=int)
    parser.add_argument("-t", action="store", dest="TIME", default=1, help="Enter the time for fuzzer timeout", type=int)


    args = parser.parse_args()

    
    try:
        check_inputfile(args.PROGRAM_PATH)
        check_inputfile(args.TEST_CASES)
        print('1. checked test cases file')
        check_outputfile(args.OUTPUT_FILE)
        check_mutation(args.MUTATION_OPTION)
        check_seed(args.SEED_OPTION)
        check_coverage(args.COVERAGE)
        check_exhaustive(args.EXHAUSTIVE_MUTATION)
        check_iterations(args.ITERATIONS)

        if args.EXHAUSTIVE_MUTATION:
            args.MUTATION_OPTION =''
       
        if(args.PROGRAM_PATH.endswith("p")):
                OUT_FILE = args.PROGRAM_PATH.replace(".cpp", "")
        elif(args.PROGRAM_PATH.endswith("c")):
                OUT_FILE = args.PROGRAM_PATH.replace(".c", "")
        
        cases = set(line.rstrip('\n') for line in open(args.TEST_CASES))
        print('2. got cases')
        print(cases)

        os.chdir('output/')
        with open(args.OUTPUT_FILE, "a") as fo:
            os.chdir('../')
            
            '''
                *path coverage algorithm
                *only for mutation methods
            '''
            #cases = set(line.rstrip('\n') for line in open(args.TEST_CASES))
            #print('2. got cases')
            #print(cases)
            end_time = time() + 60 * args.TIME

            if args.COVERAGE == "path":
                paths_seen = set()
                iterations = args.ITERATIONS 
                if args.MUTATION_OPTION != "":
                    if len(cases) != 0:
                        seeds = cases.copy()
                    #else:
                        length = 1
                    #    seeds = create_seed(length)
                 
                while True: 
                        
                    if time() > end_time:
                        exit(0)
                    current_paths = paths_seen.copy()
                    random_seed = pick_seed(seeds)
                    args.ITERATIONS = iterations
                    while(args.ITERATIONS>0):
                    
                        input_strings = []

                        if args.MUTATION_OPTION == "random":
                            args.SEED_OPTION = "none"
                            #random_seed = pick_seed(seeds)
                            input_strings.append(random_mutation(length, args.MUTATION_OPTION, args.SEED_OPTION, random_seed))
                        
                        elif args.MUTATION_OPTION != '' and args.MUTATION_OPTION != "random":
                            args.SEED_OPTION = "none"
                            #random_seed = pick_seed(seeds)
                            input_strings.append(get_Input(length, args.MUTATION_OPTION, args.SEED_OPTION, random_seed))

                        if  args.EXHAUSTIVE_MUTATION:
                            input_strings[:] = get_Input_Exhaustive(length, args.EXHAUSTIVE_MUTATION, args.SEED_OPTION, "")

                
                        for i in range(0, len(input_strings)):
                            temp_string = input_strings[i]
                     
                            Cov.compile_program(args.PROGRAM_PATH, OUT_FILE)
                            result = run([OUT_FILE], stdout=DEVNULL, stderr=DEVNULL, input=temp_string, encoding='utf-8')
                            Cov.generate_gcov(args.PROGRAM_PATH, args.COVERAGE)                 
                            Cov.clean_gcov(OUT_FILE)

                            coverage = frozenset(LineCov.get_line_coverage(args.PROGRAM_PATH))
                        
                    #exhaustive
                    #for j in range(0, len(temp_string)):
                     #   result = run([args.PROGRAM_PATH], stdout=DEVNULL, stderr=DEVNULL, input=temp_string[j], encoding='ascii')
                            if(result.returncode != 0 and result.returncode != -1):
                                print('writing to disk')
                                fo.write("Input String causing crash:   %s\n  Return code is:     %d\n\n" %(temp_string, result.returncode))
                                #temp_string = ByteArithmetic.add_character(temp_string)
                                seeds = add_seed(seeds, temp_string)

                            elif(result.returncode == -1):
                                continue
                    
                            elif coverage not in paths_seen and args.EXHAUSTIVE_MUTATION == '':
                                paths_seen.add(coverage)
                                #temp_string = ByteArithmetic.add_character(temp_string)
                                seeds = add_seed(seeds, temp_string)

                        args.ITERATIONS -= 1

                    if current_paths != paths_seen:
                        print('got new path')
                        continue
                    else:
                        print('no new path found')
                        update_seed = ByteArithmetic.add_character(random_seed)
                        seeds = remove_seed(seeds, random_seed)
                        seeds = add_seed(seeds, update_seed)
                       
                
        #block coverage
        #only for random mutations

            elif args.COVERAGE == 'block':
                #print('1. block cov')
                if args.EXHAUSTIVE_MUTATION != "":
                    print("Exhaustive option is disabled!")
                    exit(0)
                iterations = args.ITERATIONS
                if args.MUTATION_OPTION != "":
                    if len(cases) != 0:
                 #       print('2. cases found\n')
                        seeds = cases.copy()
                        print(seeds)
                    #else:
                        length = 1
                     #   seeds = create_seed(length)
 
                #while True:
                for i in range(0,2):
                        #if len(full_seeds)==0:
                        #    full_seeds[:] = optimal_seeds
                        
                        #    full_seeds.extend(create_seed(length))
                        
                        args.ITERATIONS = iterations
                        input_string = ""
                        max_candidate = ""
                        current_candidate =""
                        max_candidate_coverage = set()
                        print('3. iterations')
                        print(iterations)
                        #for j in range(0, len(full_seeds)):
                        random_seed = pick_seed(seeds)
                        new_block_seeds = 0

                        while args.ITERATIONS > 0:
                            print(random_seed) 
                            length = 1
                            if args.MUTATION_OPTION == "random":
                                args.SEED_OPTION = "none"
                                input_string = random_mutation(length, args.MUTATION_OPTION, args.SEED_OPTION, random_seed)

                            elif args.MUTATION_OPTION != '' and args.MUTATION_OPTION != "random":
                                args.SEED_OPTION = "none"
                                input_string = get_Input(length, args.MUTATION_OPTION, args.SEED_OPTION, random_seed)
         
                            Cov.compile_program(args.PROGRAM_PATH, OUT_FILE)
                            result = run([OUT_FILE], stdout=DEVNULL, stderr=DEVNULL, input=input_string, encoding='utf-8')
                            Cov.generate_gcov(args.PROGRAM_PATH, args.COVERAGE)
                            Cov.clean_gcov(OUT_FILE)
                                
                            seed_coverage = set()
                            seed_coverage = BlockCov.get_block_coverage(args.PROGRAM_PATH)                   
                                 
                            if(result.returncode != 0 and result.returncode != -1):
                                print('writing to disk')
                                seeds = add_seed(seeds, input_string)
                                fo.write("Input String causing crash:   %s\n  Return code is:     %d\n\n" %(input_string, result.returncode))

                            elif(result.returncode == -1):
                                continue
                
                            elif max_candidate == "" or (len(seed_coverage) > len(max_candidate_coverage)):
                                print('got max')
                                max_candidate = input_string
                                max_candidate_coverage = seed_coverage.copy()

                            else:
                                coverage_diff = seed_coverage - max_candidate_coverage
                                print('candidate')
                                print(max_candidate_coverage)
                                print('seed')
                                print(seed_coverage)
                                print('difference')
                                print(coverage_diff) 
                                if len(coverage_diff):
                                    print('got new')
                                    new_block_seeds = 1
                                    seeds = add_seed(seeds, input_string)

                        
                            if args.ITERATIONS == 1:
                                if current_candidate != max_candidate or new_block_seeds !=0:
                                    current_candidate = max_candidate
                                    args.ITERATIONS = iterations
                                    print('got new block')
                                    continue
                                
                                else:
                                    print('no new block')
                                    update_seed = ByteArithmetic.add_character(random_seed)
                                    seeds = remove_seed(seeds, random_seed)
                                    seeds = add_seed(seeds, update_seed)
                                    break
                            
                            args.ITERATIONS -= 1

                print(BlockCov.aggregate_block_coverage)        
                        
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
