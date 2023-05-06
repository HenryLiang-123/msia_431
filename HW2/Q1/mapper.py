import sys

# Mapper
substrings = ['nu', 'chi', 'haw']
for line in sys.stdin:
    # Remove leading and trailing whitespace and split the words
    fields = line.strip().split()
    
    if len(fields) < 4:
        continue
    elif len(fields) == 4: # 1-gram
        word = fields[0].lower()
        try:
            year = int(fields[1])
        except:
            continue
        occurence = int(fields[2])
        volumes = int(fields[3])
    elif len(fields) == 5: # 2-grams
        word = fields[0].lower()
        second_word = fields[1].lower()
        try:
            year = int(fields[2])
        except:
            continue
        occurence = int(fields[3])
        volumes = int(fields[4])
    # print(fields)
    for substring in substrings:
        if len(fields) == 4:
            count = int(substring in word)
            if count > 0:
                print(f'{year},{substring},{count * volumes}')
        elif len(fields) == 5:
            count = int(substring in word) + int(substring in second_word)
            if count > 0:
                print(f'{year},{substring},{count * volumes}')