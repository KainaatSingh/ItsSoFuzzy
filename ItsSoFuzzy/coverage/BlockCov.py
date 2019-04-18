import re

aggregate_block_coverage = [] 
total_coverage = set()

def get_aggregate_block_coverage(coverage):

    global aggregate_block_coverage
    global total_coverage
    total_coverage |= coverage
    aggregate_block_coverage.append(len(total_coverage))
    return 


def get_block_coverage(input_file):
    filename = input_file + ".gcov"
    coverage = set()
    block_covered = 0
    total_blocks = 0
   
    with open(filename) as fd:
        for line in fd.readlines():
            elements = re.split('[:,-]', line)
            covered = elements[0].strip()
            
            if elements[2].startswith('block'):
            
                if covered.startswith('-') or covered.startswith('#') or covered.startswith('$'):
                    continue
                
                block_covered += 1
                coverage.add(block_covered)
    
    get_aggregate_block_coverage(coverage)
    return coverage
