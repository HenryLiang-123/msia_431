from pyspark import SparkConf, SparkContext
from scipy import stats

def check_year_e(x):
    emanuel_years = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
    try:
        year = x[17]
        return year in emanuel_years
    except :
        print(f"ValueError for record {x}")
        return False
    
def check_year_d(x):
    daley_years = ['1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011']
    try:
        year = x[17]
        return year in daley_years
    except :
        print(f"ValueError for record {x}")
        return False

def is_diff(path):
    conf = SparkConf().setAppName("CrimeAnalysis")
    sc = SparkContext(conf=conf)

    data = sc.textFile(path)
    header = data.first()
    data = data.filter(lambda line: line != header).map(lambda line: line.split(","))
        
    df_filtered_e = data.filter(check_year_e)
    beat_year_e = df_filtered_e.map(lambda row: ((row[10], row[17]), 1))\
                            .reduceByKey(lambda a, b: a + b)\
                            .map(lambda x: (x[0][0], (x[0][1], x[1])))
    beat_grouped_e = beat_year_e.groupByKey().mapValues(list)
    beat_counts_e = beat_grouped_e.mapValues(lambda x: [count for year, count in x])
    beat_dict_e = beat_counts_e.collectAsMap()

    df_filtered_d = data.filter(check_year_d)
    beat_year_d = df_filtered_d.map(lambda row: ((row[10], row[17]), 1))\
                            .reduceByKey(lambda a, b: a + b)\
                            .map(lambda x: (x[0][0], (x[0][1], x[1])))
    beat_grouped_d = beat_year_d.groupByKey().mapValues(list)
    beat_counts_d = beat_grouped_d.mapValues(lambda x: [count for year, count in x])
    beat_dict_d = beat_counts_d.collectAsMap()
    
    diff_dict = {}

    for k, v in beat_dict_e.items():
        if k in beat_dict_d:
            e_crime = v
            d_crime = beat_dict_d[k]
            t_statistic, p_value = stats.ttest_ind(e_crime, d_crime, equal_var=False)
            
            if p_value <= 0.05:
                diff_dict[k] = 'Yes'
            else:
                diff_dict[k] = 'No'

    with open("HW3/liang_2_3.txt", "w") as file:
        file.write("Beat, is_diff\n")
        for k, v in diff_dict.items():
            file.write(f"{k}, {v}\n")

if __name__=="__main__":
    is_diff("HW3/Crimes_-_2001_to_present.csv")