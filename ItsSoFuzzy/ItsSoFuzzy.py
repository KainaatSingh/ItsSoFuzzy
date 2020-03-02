#!/usr/bin/env python3

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
from time import time, ctime
path.append('coverage/')
import Cov
import LineCov
import BlockCov
import matplotlib.pyplot as plt
import pickle
import unicodedata


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

def check_iterations(iterations):

    if iterations < 10:
        print("Minimum number of iterations should be 100000")
        exit(0)
    else:
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

def check_file(name):
    file_check = ["c", "cpp", "argument", "standard"]
    
    if name in file_check:
       return
    else:
       print("ERROR:   Invalid file format or type provided!!")
       exit(0)

def check_coverage(name):
    coverage_method = ["line", "block"]
    
    if name in coverage_method:
       return
    else:
       print("ERROR:   Invalid Code Coverage Method!!")
       exit(0)


    if iterations < 10:
        print("Minimum number of iterations should be 100000")
        exit(0)
    else:
        return


def write_result(crashes, runs, total_inputs, filename1, filename2, mutation, coverage):
        os.chdir('output/') 
        
        with open(filename1, "a") as fo:
            fo.truncate(0)
            fo.write("Mutation is   %s  Coverage is     %s" % (mutation, coverage))
            fo.write("/nTotal number of crashes found:   %d" % crashes)
            if runs>1:
                runs /= 2
            fo.write("/nTotal number of runs:   %d" % runs)
            fo.write("/nTotal number of inputs:   %d" % total_inputs)
        
        print('Program fuzzed successfully!!! :)')
        if coverage == 'line':
                 
            with open(filename2, "wb") as fi:
                pickle.dump(LineCov.aggregate_line_coverage, fi)
                os.chdir('../')
            
            plt.plot(LineCov.aggregate_line_coverage)
            plt.title(mutation)
            plt.xlabel('# of inputs')
            plt.ylabel('lines covered')
            filename = filename1[:-4] 
            plt.savefig(filename, dpi=300)
            plt.show()
        else:
            
            with open(filename2, "wb") as fi:
                pickle.dump(LineCov.aggregate_line_coverage, fi)
                os.chdir('../')
            
            plt.plot(BlockCov.aggregate_block_coverage)
            plt.title(mutation)
            plt.xlabel('# of inputs')
            plt.ylabel('blocks covered')
            filename = filename1[:-4] 
            plt.savefig(filename, dpi=300)
            plt.show()
            


'''
    * Main function
    * 
    * Run the input program with input string
'''
if __name__ == "__main__":
    
    parser = ArgumentParser()
    parser.add_argument("PROGRAM_PATH", help="Enter the absolute program path", type=str)
    parser.add_argument("TEST_CASES", help="Enter absolute path of file containing testcases", type=str)
    parser.add_argument("FILE_FORMAT", help="Enter the file format: c or cpp", type=str)
    parser.add_argument("FILE_TYPE", help="Enter the file type: argument or standard", type=str)
    parser.add_argument("-o", action="store", dest="OUTPUT_FILE", default='output.txt', help="Enter output file name", type=str)  
    parser.add_argument("-r1", action="store", dest="RESULT_FILE", default='result.txt', help="Enter result file name", type=str)  
    parser.add_argument("-r2", action="store", dest="COVERAGE_FILE", default='coverage.txt', help="Enter coverage file name", type=str)  
    parser.add_argument("-m", action="store", dest="MUTATION_OPTION", default='random', help="Enter mutation method. See Documentation for meaning:\nrandom\nflip_one\nflip_all\nflip_two\nbyte_arithmetic\nbyte_swap", type=str)  
    parser.add_argument("-s", action="store", dest="SEED_OPTION", default="random_printable", help="Enter seed generation method. See Documentation for meaning:\nrandom_printable\nrandom\nexhaustive", type=str) 
    parser.add_argument("-c", action="store", dest="COVERAGE", default='line', help="Enter coverage type:\nline\nblock", type=str)
    parser.add_argument("-i", action="store", dest="ITERATIONS", default=10000, help="Enter the number of iterations for each run", type=int)
    parser.add_argument("-t", action="store", dest="TIME", default=90, help="Enter the time for fuzzer timeout", type=int)


    args = parser.parse_args()

    
    try:
        check_inputfile(args.PROGRAM_PATH)
        check_inputfile(args.TEST_CASES)
        check_file(args.FILE_FORMAT)
        check_file(args.FILE_TYPE)
        check_outputfile(args.OUTPUT_FILE)
        check_mutation(args.MUTATION_OPTION)
        check_seed(args.SEED_OPTION)
        check_coverage(args.COVERAGE)
        check_iterations(args.ITERATIONS)


       
        if(args.PROGRAM_PATH.endswith("p")):
                OUT_FILE = args.PROGRAM_PATH.replace(".cpp", "")
        elif(args.PROGRAM_PATH.endswith("c")):
                OUT_FILE = args.PROGRAM_PATH.replace(".c", "")
        
        cases = set(line.rstrip('\n') for line in open(args.TEST_CASES))

        crashes = 0
        seed_values = []
        runs = 0
        total_inputs = 0
        iterations_new_path = []
        os.chdir('output/')
        with open(args.OUTPUT_FILE, "w") as fo:
            os.chdir('../')
            
            '''
                *path coverage algorithm
                *only for mutation methods
            '''
            end_time = time() + 60 * args.TIME

            if args.COVERAGE == "line":
                paths_seen = set()
                iterations = args.ITERATIONS 
                if args.MUTATION_OPTION != "":
                    if len(cases) != 0:
                        seeds = cases.copy()
                        length = 1
                 
                print(ctime())
                while True: 
                    runs += 1 
                    seed_values.append(len(seeds))

                    if time() > end_time:
                        write_result(crashes, runs, total_inputs, args.RESULT_FILE, args.COVERAGE_FILE, args.MUTATION_OPTION, args.COVERAGE)
                        exit(0)
                    
              
                    current_paths = paths_seen.copy()
                    random_seed = pick_seed(seeds)
                    args.ITERATIONS = iterations
                    
                    while(args.ITERATIONS>0):
                        if args.ITERATIONS==iterations:
                            runs+=1
                        if time() > end_time:
                            write_result(crashes, runs, total_inputs, args.RESULT_FILE, args.COVERAGE_FILE, args.MUTATION_OPTION, args.COVERAGE)
                            exit(0)

                        input_strings = []

                        if args.MUTATION_OPTION == "random":
                            args.SEED_OPTION = "none"
                            input_strings.append(random_mutation(length, args.MUTATION_OPTION, args.SEED_OPTION, random_seed))
                        
                        elif args.MUTATION_OPTION != '' and args.MUTATION_OPTION != "random":
                            args.SEED_OPTION = "none"
                            input_strings.append(get_Input(length, args.MUTATION_OPTION, args.SEED_OPTION, random_seed))


                        total_inputs += 1
                        for i in range(0, len(input_strings)):
                            temp_string = input_strings[i]
                            temp_string=temp_string.encode() 
                            temp_string=str(temp_string, 'utf-8')
                            temp_string="".join(ch for ch in temp_string if unicodedata.category(ch)[0]!="C")
                            
                            Cov.compile_program(args.PROGRAM_PATH, OUT_FILE, args.FILE_FORMAT)
                            if args.FILE_TYPE=="standard":
                                result = run([OUT_FILE], input=temp_string, encoding='utf-8')
                            else:
                                result = run([OUT_FILE,temp_string], stdout=DEVNULL, stderr=DEVNULL, encoding='utf-8')
                            Cov.generate_gcov(args.PROGRAM_PATH, args.COVERAGE)                 
                            Cov.clean_gcov(OUT_FILE)

                            coverage = frozenset(LineCov.get_line_coverage(args.PROGRAM_PATH))
                        
                            if(result.returncode != 0 and result.returncode != -1):
                                crashes += 1
                                fo.write("Input String causing crash:   %s\n  Return code is:     %d\n\n" %(temp_string, result.returncode))
                                seeds = add_seed(seeds, temp_string)

                            elif(result.returncode == -1):
                                continue
                    
                            elif coverage not in paths_seen:
                                iterations_new_path.append(iterations-args.ITERATIONS)
                                paths_seen.add(coverage)
                                seeds = add_seed(seeds, temp_string)

                        args.ITERATIONS -= 1
                    if current_paths != paths_seen:
                        continue
                    else:
                        update_seed = ByteArithmetic.add_character(random_seed)
                        seeds = remove_seed(seeds, random_seed)
                        seeds = add_seed(seeds, update_seed)
                       
        #block coverage
        #only for random mutations

            elif args.COVERAGE == 'block':
                iterations = args.ITERATIONS
                if args.MUTATION_OPTION != "":
                    if len(cases) != 0:
                        seeds = cases.copy()
                        length = 1
 
                print(ctime())
                while True:
                        runs += 1
                        if time() > end_time:
                            write_result(crashes, runs, total_inputs, args.RESULT_FILE, args.COVERAGE_FILE, args.MUTATION_OPTION, args.COVERAGE)
                            exit(0)
                            
                        args.ITERATIONS = iterations
                        input_string = ""
                        max_candidate = ""
                        current_candidate =""
                        max_candidate_coverage = set()
                        random_seed = pick_seed(seeds)
                        new_block_seeds = 0

                        while args.ITERATIONS > 0:
                            if args.ITERATIONS==iterations:
                                runs+=1
                            

                            if time() > end_time:
                                write_result(crashes, runs, total_inputs, args.RESULT_FILE, args.COVERAGE_FILE, args.MUTATION_OPTION, args.COVERAGE)
                                exit(0)

                            
                            length = 1
                            if args.MUTATION_OPTION == "random":
                                args.SEED_OPTION = "none"
                                input_string = random_mutation(length, args.MUTATION_OPTION, args.SEED_OPTION, random_seed)

                            elif args.MUTATION_OPTION != '' and args.MUTATION_OPTION != "random":
                                args.SEED_OPTION = "none"
                                input_string = get_Input(length, args.MUTATION_OPTION, args.SEED_OPTION, random_seed)
         
                            total_inputs += 1
                            
                            input_string=input_string.encode() 
                            input_string=str(input_string, 'utf-8')
                            input_string="".join(ch for ch in input_string if unicodedata.category(ch)[0]!="C")
                            
                            Cov.compile_program(args.PROGRAM_PATH, OUT_FILE, args.FILE_FORMAT)
                            if args.FILE_TYPE=="standard":
                                result = run([OUT_FILE], stdout=DEVNULL, stderr=DEVNULL, input=input_string, encoding='utf-8')
                            else:
                                result = run([OUT_FILE,input_string], stdout=DEVNULL, stderr=DEVNULL, encoding='utf-8')
                            Cov.generate_gcov(args.PROGRAM_PATH, args.COVERAGE)
                            Cov.clean_gcov(OUT_FILE)
                                
                            seed_coverage = set()
                            seed_coverage = BlockCov.get_block_coverage(args.PROGRAM_PATH)                   
                                 
                            if(result.returncode != 0 and result.returncode != -1):
                                crashes += 1
                                seeds = add_seed(seeds, input_string)
                                fo.write("Input String causing crash:   %s\n  Return code is:     %d\n\n" %(input_string, result.returncode))

                            elif(result.returncode == -1):
                                continue
                
                            elif max_candidate == "" or (len(seed_coverage) > len(max_candidate_coverage)):
                                max_candidate = input_string
                                max_candidate_coverage = seed_coverage.copy()

                            else:
                                coverage_diff = seed_coverage - max_candidate_coverage
                                if len(coverage_diff):
                                    new_block_seeds = 1
                                    seeds = add_seed(seeds, input_string)

                        
                            if args.ITERATIONS == 1:
                                if current_candidate != max_candidate or new_block_seeds !=0:
                                    current_candidate = max_candidate
                                    args.ITERATIONS = iterations
                                    continue
                                
                                else:
                                    update_seed = ByteArithmetic.add_character(random_seed)
                                    seeds = remove_seed(seeds, random_seed)
                                    seeds = add_seed(seeds, update_seed)
                                    break
                            
                            args.ITERATIONS -= 1

                        
    except KeyboardInterrupt:
           print("\nyou pressed ctrl+c to quit")
