#!/usr/bin/env python3


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
    return coverage
