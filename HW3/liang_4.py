from pyspark.sql.functions import to_timestamp, col
from pyspark.sql import SparkSession
from pyspark.sql.functions import hour, dayofweek, month
from pyspark.sql.functions import count
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans

def get_pattern(path):
    spark = SparkSession.builder.getOrCreate()
    df_spark = spark.read.options(header = 'True', inferSchema='True').csv(path)

    crimeDF = df_spark.withColumn("Date", to_timestamp(col("Date"), "MM/dd/yyyy hh:mm:ss a"))
    crimeDF = crimeDF.filter(crimeDF.Arrest == "true")


    crimeDF = (crimeDF
                .withColumn("Hour", hour(col("Date")))
                .withColumn("DayOfWeek", dayofweek(col("Date")))
                .withColumn("Month", month(col("Date"))))


    crimeDF_grouped = (crimeDF
                    .filter(crimeDF.Arrest == "true")
                    .groupBy("Hour", "DayOfWeek", "Month")
                    .agg(count("ID").alias("CrimeWithArrestCount")))

    crimeDF_sorted = crimeDF_grouped.sort(col("CrimeWithArrestCount").desc())


    assembler = VectorAssembler(inputCols=["Hour", "DayOfWeek", "Month"], outputCol="features")
    crimeDF = assembler.transform(crimeDF)


    kmeans = KMeans(k=5, seed=1)  # Initialization
    model = kmeans.fit(crimeDF.select('features'))  # Fitting the model

    transformed = model.transform(crimeDF)
    num_clusters = model.getK()

    centers = model.clusterCenters()
    with open("HW3/liang_4.txt", "w") as file:
        for center in centers:
            file.write(f"Cluster center (Hour, DayOfWeek, Month): {center}\n")

        for i in range(num_clusters):
            file.write(f"Showing instances from cluster: {i}\n")
            file.write(f"{transformed.filter(transformed.prediction == i).take(5)}\n")

        for i in range(num_clusters):
            file.write(f"Most common crimes in cluster: {i}\n")
            file.write(f"{transformed.filter(transformed.prediction == i).groupBy('Primary Type').count().sort('count', ascending=False).collect()}\n")


if __name__ == "__main__":
    get_pattern("HW3/Crimes_-_2001_to_present.csv")