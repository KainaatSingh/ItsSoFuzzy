#!/usr/bin/env python3


aggregate_line_coverage = []
total_line_coverage = set()

def get_aggregate_line_coverage(coverage):

    global aggregate_line_coverage
    global total_line_coverage
    total_line_coverage |= coverage
    aggregate_line_coverage.append(len(total_line_coverage))
    return

def get_line_coverage(input_file):
    filename = input_file + ".gcov"
    coverage = set()
    
    with open(filename) as fd:
    
        for line in fd.readlines():
            elements = line.split(':')
            covered = elements[0].strip()
            line_no = int(elements[1].strip())
        
            if covered.startswith('-') or covered.startswith('#'):
                continue
            
            coverage.add(line_no)
    
    get_aggregate_line_coverage(coverage)
    return coverage
