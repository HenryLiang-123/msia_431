from collections import defaultdict

def shuffle(mapper_outputs):
    shuffle_data = defaultdict(list)
    
    # Group data by artist name
    for mapper_output in mapper_outputs:
        for artist, duration in mapper_output:
            shuffle_data[artist].append(duration)
    
    # Sort the data by artist name
    sorted_data = dict(sorted(shuffle_data.items(), key=lambda x: x[0]))
    
    return sorted_data