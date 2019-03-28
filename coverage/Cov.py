#!/usr/bin/env python3


import os
import subprocess
from sys import path
path.append('../input')


def compile_program(input_file, out_file):
    
    os.chdir('input/')
    output = subprocess.run(['gcc ' + ' --coverage ' + ' -ftest-coverage ' + ' -fprofile-arcs ' + input_file + ' -o ' + out_file], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, encoding ='utf-8')

    if output.returncode == 0:
        os.chdir('../')
        return
    else:
        print("Compiling Error...............:\n", output.stderr)
        exit(0)


def generate_gcov(input_file):

    #print(os.getcwd())
    os.chdir('input/')
    output = subprocess.run(['gcov ' + input_file], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, encoding ='utf-8')

    if output.returncode == 0:
        os.chdir('../')
        return
    else:
        print("Error Generating Gcov...............:\n", output.stderr)
        exit(0)


def clean_gcov(out_file):
    #print(os.getcwd())
    os.chdir('input/')
    output1 = subprocess.run(['rm ' + '*.gcda'], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, encoding ='utf-8')
    output2 = subprocess.run(['rm ' + '*.gcno'], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, encoding ='utf-8')
    os.chdir('../')

'''
compile_program('/home/kainaat/malware_analysis/masterlabkainaatsingh/input/sample_program.c', '/home/kainaat/malware_analysis/masterlabkainaatsingh/input/sample_program')
print('compiled')
generate_gcov('/home/kainaat/malware_analysis/masterlabkainaatsingh/input/sample_program.c')
print('generated')
clean_gcov('/home/kainaat/malware_analysis/masterlabkainaatsingh/input/sample_program')
print('cleaned')
'''
