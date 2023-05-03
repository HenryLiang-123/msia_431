#!/usr/bin/env python3
import sys

current_word = None
current_count = 0

# Read each line from stdin
for line in sys.stdin:
    # Split the input line into word and count
    word, count = line.strip().split('\t')

    # Convert count to integer
    count = int(count)

    # If the current word is not None and is different from the word just read, 
    # print the word and its count
    if current_word and current_word != word:
        print(f'{current_word}\t{current_count}')
        current_count = 0

    # Update the current word and increment its count
    current_word = word
    current_count += count

# Print the last word and its count
if current_word:
    print(f'{current_word}\t{current_count}')
