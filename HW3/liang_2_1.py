from pyspark import SparkConf, SparkContext
import time

def check_year(x):
    try:
        year = int(x[17])
        return year in [2020,2021,2022]
    except :
        print(f"ValueError for record {x}")
        return False


def get_high_crime_block(path):

    conf = SparkConf().setAppName("CrimeAnalysis")
    sc = SparkContext(conf=conf)
    # Read the data
    data = sc.textFile(path)
    header = data.first()
    data = data.filter(lambda line: line != header).map(lambda line: line.split(","))

    data_year = data.map(lambda x: ())
    # Filter to get data from last 3 years
    data_last_3_years = data.filter(check_year)

    # Get the block and its count
    block_counts = data_last_3_years.map(lambda x: (x[3][:5], 1)).reduceByKey(lambda a, b: a + b)

    # Get top 10 blocks
    top_10_blocks = block_counts.sortBy(lambda x: x[1], ascending=False).take(10)

    with open("liang_2_1.txt", "w") as file:
        file.write("Block, Count\n")
        for block, count in top_10_blocks:
            file.write(f"{block}, {count}\n")

if __name__ == "__main__":
    get_high_crime_block(path = 'Crimes_-_2001_to_present.csv')