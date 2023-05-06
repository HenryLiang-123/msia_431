## Question 1

### Chat GPT Prompts

#### Prompt 1

Description: The data for this problem comes from Google’s project for counting word frequencies in its
entire Google Books collection. You are given two files: one file reports 1 grams (single words) and
another file reports 2 grams (pairs of words; one following each other in text). The data represents the
number of occurrences of a particular word (or pairs of words) in a given year across all books available
by Google Books. The number of volumes/books containing a word (or pairs of words) is also reported.
Write a MapReduce program in python that reports the average number of volumes per year for words
containing
the following three substrings: ‘nu,’ ‘chi,’ ‘haw’.
Example:
The 1 gram file format --the regex “\\s+” will match any kind of whitespace (space, tab etc):
word \\s+ year \\s+ number of occurrences \\s+ number of volumes \\s+ ...
The 2 gram file format:
word \\s+ word \\s+ year \\s+ number of occurrences \\s+ number of volumes \\s+...
The final output should show the year, substring, and average number of volumes where the substring
appears in that year. For example:
2000,nu,345
2010,nu,200
1998,chi,31
If each word in the bi-gram includes the string, it should be counted twice in the average. For example,
for the bi-gram “nugi hinunu” with volume of 10, when calculating the average, its contribution to the
numerator should be 2 times 10 and in the denominator it should be 2. A unigram counts only once
regardless of the number of occurrences of “nu” in the word.

Here's what i have as a test file
N'Dogo	1911	4	2
N'Dogo	1936	1	1
N'Dogo	1971	3	3
N'Dogo	1972	3	3
N'Dogo	1973	2	2
chi nu	1965	1	4
chi chichi	1965	1	10

------------------------------------------
Here's what the mapper.py script looks like
#!/usr/bin/env python3
import sys

/# Read each line from stdin
for line in sys.stdin:
    # Remove leading and trailing whitespace and split the words
    words = line.strip().split()

    # Write each word with its count (1) to stdout
    for word in words:
        print(f'{word}\t1')

----------------------------------
Heres what the reducer.py looks like

#!/usr/bin/env python3
import sys

current_word = None
current_count = 0

/# Read each line from stdin
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

/# Print the last word and its count
if current_word:
    print(f'{current_word}\t{current_count}')

The mapper.py and reducer.py may not be correct to solve the problem at hand. 

--------------------------
The correct output should be
1965,chi 4
1965,nu 4
1965,chi 10
1965,chi 10

#### Prompt 2

why is the sorter part important?

#### Prompt 3

can you provide me a solution of the reducer where the incoming data needs to be sorted

#### Prompt 4

im running the mapper and reducer scripts in a hadoop cluster. Do i still need to sort?


## Question 2

### Pseudocode

#### Split file

function split_file(input_file, num_splits):
    open input_file as file
    read all lines from file and store them in lines
    set chunk_size = floor(length of lines / num_splits)
    for i in range(num_splits):
        open a new file named 'split_i.csv' as split_file
        set start = i * chunk_size
        set end = (i + 1) * chunk_size if i != num_splits - 1 else length of lines
        write lines from start to end into split_file
    close all files

#### Mapper

FUNCTION mapper(file_path)
    1. Create an empty list called "results"
    2. Open the file at "file_path" in read mode as "csvfile"
    3. Create a CSV reader object for "csvfile" called "reader"
    4. For each row in "reader":
        a. Get the value in the third column and store it in a variable called "artist"
        b. Get the value in the fourth column and store it in a variable called "duration"
        c. Convert "duration" to a float
        d. Append a tuple containing "artist" and the converted "duration" to the "results" list
    5. Return the "results" list
END FUNCTION

#### Shuffle

FUNCTION shuffle(mapper_outputs)
    1. Create a new defaultdict called "shuffle_data" with lists as default values
    2. For each "mapper_output" in "mapper_outputs":
        a. For each tuple (artist, duration) in "mapper_output":
            i. Append "duration" to the list corresponding to the "artist" key in "shuffle_data"
    3. Sort the items in "shuffle_data" by the artist name (key) and store them in a new dictionary called "sorted_data"
    4. Return the "sorted_data" dictionary
END FUNCTION

#### Reducer

FUNCTION reducer(shuffled_data)
    1. Create an empty dictionary called "max_durations"
    2. For each key-value pair (artist, durations) in "shuffled_data":
        a. Find the maximum duration in the "durations" list
        b. Store the maximum duration in "max_durations" with "artist" as the key
    3. Return the "max_durations" dictionary
END FUNCTION


