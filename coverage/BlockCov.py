import re

def get_block_coverage(input_file):
    filename = input_file + ".gcov"
    coverage = set()
    blocks_covered = 0
    total_blocks = 0
    with open(filename) as fd:
        for line in fd.readlines():
            elements = re.split('[:,-]', line)
            #print(elems[2].strip())
            covered = elements[0].strip()
            #print(covered)
            #line_number = int(elems[1].strip())
            #print(line_number)
            if elements[2].startswith('block'):
                total_blocks +=1
                if covered.startswith('-') or covered.startswith('#') or covered.startswith('$'):
                    continue
                blocks_covered +=1
    coverage.add((blocks_covered, total_blocks))
    return coverage
