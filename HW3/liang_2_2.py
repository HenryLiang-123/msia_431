from pyspark import SparkConf, SparkContext
import numpy as np


def check_year(x):
    try:
        year = x[17]
        return year in ['2020', '2019', '2018', '2017', '2016']
    except :
        print(f"ValueError for record {x}")
        return False

def get_corr(path):
    conf = SparkConf().setAppName("CrimeAnalysis")
    sc = SparkContext(conf=conf)
    data = sc.textFile(path)
    header = data.first()
    data = data.filter(lambda line: line != header).map(lambda line: line.split(","))
    df_filtered = data.filter(check_year)

    beat_year = df_filtered.map(lambda row: ((row[10], row[17]), 1))\
                            .reduceByKey(lambda a, b: a + b)\
                            .map(lambda x: (x[0][0], (x[0][1], x[1])))
    beat_grouped = beat_year.groupByKey().mapValues(list)
    beat_counts = beat_grouped.mapValues(lambda x: [count for year, count in x])
    beat_dict = beat_counts.collectAsMap()

    corr_dict = {}
    beat_keys = list(beat_dict.keys())
    corr_mat = np.corrcoef(list(beat_dict.values()))

    for i in range(len(beat_keys)):
        for j in range(i+1, len(beat_keys)):
            beat1 = beat_keys[i]
            beat2 = beat_keys[j]
            corr = corr_mat[i, j]
            corr_dict[(beat1, beat2)] = corr
    sorted_corr_dict = dict(sorted(corr_dict.items(), key=lambda item: np.abs(item[1]), reverse=True))

    with open("HW3/liang_2_2.txt", "w") as file:
        file.write("Beat 1, Beat 2, Correlation\n")
        for k, v in sorted_corr_dict.items():
            file.write(f"{k[0]}, {k[1]}, {v}\n")


if __name__ == "__main__":
    get_corr("HW3/Crimes_-_2001_to_present.csv")
