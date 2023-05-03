#!/usr/bin/env python3
import sys

# Read each line from stdin
for line in sys.stdin:
    # Remove leading and trailing whitespace and split the words
    words = line.strip().split()

    # Write each word with its count (1) to stdout
    for word in words:
        print(f'{word}\t1')
