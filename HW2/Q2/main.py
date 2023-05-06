import sys
import multiprocessing as mp
from mapper import mapper
from shuffle import shuffle
from reducer import reducer

def split_file(input_file, num_splits):
    with open(input_file, 'r') as file:
        lines = file.readlines()
        chunk_size = len(lines) // num_splits
        for i in range(num_splits):
            with open(f'split_{i}.csv', 'w') as split_file:
                start = i * chunk_size
                end = (i + 1) * chunk_size if i != num_splits - 1 else len(lines)
                split_file.writelines(lines[start:end])

if __name__ == '__main__':
    path = sys.argv[1]
    num_maps = int(sys.argv[2])
    num_reduces = int(sys.argv[3])

    split_file(path, num_maps)

    
    with mp.Pool(processes=num_maps) as map_pool:
        map_results = map_pool.map(mapper, [f'split_{i}.csv' for i in range(num_maps)])
        # print(len(map_results[0]), len(map_results[1]))
        # Shuffle data
        shuffled_data = shuffle(map_results)
        # Run reducers in parallel
        with mp.Pool(processes=num_reduces) as reduce_pool:
            reduced_data = reduce_pool.map(reducer, [dict(shuffled_data.items())])
        
        # Combine results from all reducers
        final_result = {}
        for result in reduced_data:
            final_result.update(result)
        
        # Write to file
        f = open("output.txt", "a")
        print(final_result, file=f)
        f.close()
