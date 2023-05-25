from pyspark import SparkConf, SparkContext

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
    data = sc.textFile("Crimes_-_2001_to_present.csv")
    header = data.first()
    data = data.filter(lambda line: line != header).map(lambda line: line.split(","))

    
# Filter the DataFrame for the last five years
df_filtered = data.filter(lambda x: x[17] in ['2020', '2019', '2018', '2017', '2016'])