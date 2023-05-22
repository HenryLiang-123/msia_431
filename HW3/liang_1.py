import pandas as pd
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.functions import to_date, month, col
import matplotlib.pyplot as plt


def generate_hist(path):
    spark = SparkSession.builder.getOrCreate()
    df_spark = spark.read.options(header = 'True', inferSchema='True').csv(path)

    df_spark = df_spark.withColumn('Date', to_date(col("Date"), 'MM/dd/yyyy hh:mm:ss a'))
    df_spark = df_spark.withColumn("Month", month(col("Date")))

    # Register the DataFrame as a temporary table
    df_spark.createOrReplaceTempView("crimes")

    # Use SparkSQL to find the count of crime events by month
    result = spark.sql("""
        SELECT Month, COUNT(*) as crime_events
        FROM crimes
        GROUP BY Month
        ORDER BY Month
    """)

    # Collect the results to a Pandas DataFrame
    pd_result = result.toPandas()
    plt.figure(figsize=(10, 5))
    plt.bar(pd_result['Month'], pd_result['crime_events'])
    plt.xlabel('Month')
    plt.ylabel('Crime Events')
    plt.title('Crime Events by Month')
    plt.show()

if __name__ == "__main__":
    generate_hist('Crimes_-_2001_to_present.csv')