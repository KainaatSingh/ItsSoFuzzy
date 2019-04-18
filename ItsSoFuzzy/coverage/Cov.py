#!/usr/bin/env python3


import os
import subprocess
from sys import path
path.append('../input/')


def compile_program(input_file, out_file, filetype):
    
    work_directory = os.path.dirname(input_file)
    os.chdir(work_directory)
    
    if filetype=="c":
        output = subprocess.run(['gcc ' + '-fsanitize=address ' + ' --coverage ' + ' -ftest-coverage ' + ' -fprofile-arcs ' + input_file + ' -o ' + out_file], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, encoding ='utf-8')
    else:
        output = subprocess.run(['g++ ' + '-fsanitize=address ' + ' --coverage ' + ' -ftest-coverage ' + ' -fprofile-arcs ' + input_file + ' -o ' + out_file], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, encoding ='utf-8')

    if output.returncode == 0:
        os.chdir('../')
        return
    else:
        print("Compiling Error...............:\n", output.stderr)
        exit(0)


def generate_gcov(input_file, coverage):

    work_directory = os.path.dirname(input_file)
    os.chdir(work_directory)
    
    if coverage == 'line':
        output = subprocess.run(['gcov ' + input_file], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, encoding ='utf-8')
    elif coverage == 'block':
        output = subprocess.run(['gcov ' + ' -a ' + input_file], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, encoding ='utf-8')
    
    if output.returncode == 0:
        os.chdir('../')
        return
    else:
        print("Error Generating Gcov...............:\n", output.stderr)
        exit(0)


def clean_gcov(out_file):
    
    work_directory = os.path.dirname(out_file)
    os.chdir(work_directory)
    
    output1 = subprocess.run(['rm ' + '*.gcda'], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, encoding ='utf-8')
    output2 = subprocess.run(['rm ' + '*.gcno'], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, encoding ='utf-8')
    os.chdir('../')
