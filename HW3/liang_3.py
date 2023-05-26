from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import explode, posexplode, lit
from pyspark.sql.functions import expr, date_add
from pyspark.sql.functions import lag
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator


def get_pred(path):
    spark = SparkSession.builder.getOrCreate()
    df = spark.read.options(header = 'True', inferSchema='True').csv(path)

    # Define the UCR codes that represent violent crimes
    violent_crime_codes = ["0110", "0130", "0261", "0262", "0263", "0264", "0265", "0266", "0281", "0291", "1753", "1754"]

    # Filter out only the violent crimes
    violent_crimes_df = df.filter(df.IUCR.isin(violent_crime_codes))

    # Change the Date to a DateType
    violent_crimes_df = violent_crimes_df.withColumn("Date", F.to_date(F.col("Date"), 'MM/dd/yyyy hh:mm:ss a'))
    violent_crimes_df = violent_crimes_df.withColumn("week_of_yr", F.weekofyear(violent_crimes_df.Date))
    violent_crimes_df = violent_crimes_df.withColumn("yr", F.year(violent_crimes_df.Date))

    # Aggregate on a weekly basis
    weekly_violent_crimes_df = violent_crimes_df.groupBy('week_of_yr', 'yr', "Beat").count()

    df = df.withColumn("Date", F.to_date(F.col("Date"), 'MM/dd/yyyy hh:mm:ss a'))

    # Get the min and max date from the original DataFrame
    min_date, max_date = df.select(F.min("Date"), F.max("Date")).first()

    # Generate the range of dates with 1-week increments
    date_range = spark.range(0, (max_date - min_date).days // 7).select(date_add(lit(min_date), (7 * F.col("id")).cast('integer')).alias("week"))
   
   # Get all the unique beats
    beats = df.select("Beat").distinct()

    # Create a DataFrame with all combinations of Date and Beat
    complete_df = beats.crossJoin(date_range)

    # Show the DataFrame
    complete_df = complete_df.withColumn("week_of_yr", F.weekofyear("week"))
    complete_df = complete_df.withColumn("yr", F.year("week"))
    complete_df = complete_df.drop('week')

    filled_df = complete_df.join(weekly_violent_crimes_df, ["week_of_yr", "yr", "Beat"], "left_outer")

    # Fill the null counts with 0
    filled_df = filled_df.na.fill({"count": 0})
    filled_df = filled_df.orderBy(['Beat', 'yr', "week_of_yr"])

    # Window
    window = Window.partitionBy("Beat").orderBy("yr", "week_of_yr")

    # Creating lagged feature for 1 week
    filled_df = filled_df.withColumn("lag_week_1", lag(filled_df["count"]).over(window))
    # Creating lagged feature for 1 month (approx. 4 weeks)
    filled_df = filled_df.withColumn("lag_month_1", lag(filled_df["count"], 4).over(window)).na.drop()

    indexer = StringIndexer(inputCol="Beat", outputCol="beat_idx")
    indexer_model = indexer.fit(filled_df)
    indexed = indexer_model.transform(filled_df)
    indexed = indexed.withColumn("beat_idx", indexed.beat_idx.cast("int"))

    # Define the input columns for the VectorAssembler
    inputCols = ["lag_week_1", "lag_month_1", "beat_idx", "week_of_yr", "yr"]

    # Initialize the VectorAssembler
    vectorAssembler = VectorAssembler(inputCols=inputCols, outputCol="features")

    # Initialize the RandomForestRegressor
    rf = RandomForestRegressor(featuresCol="features", labelCol="count")

    # Initialize the pipeline
    pipeline = Pipeline(stages=[vectorAssembler, rf])

    # Split the data into train and test sets
    train_df, test_df = indexed.randomSplit([0.7, 0.3])

    # Train the model
    model = pipeline.fit(train_df)

    # Make predictions
    predictions = model.transform(test_df)

    # Evaluate the model
    evaluator = RegressionEvaluator(labelCol="count", predictionCol="prediction")
    mae = evaluator.setMetricName("mae").evaluate(predictions)
    r2 = evaluator.setMetricName("r2").evaluate(predictions)

    with open("HW3/liang_3.txt", "w") as file:
        file.write("Metric, Value\n")
        file.write(f"mae, {mae}\n")
        file.write(f"r squared, {r2}\n")

if __name__ == "__main__":
    get_pred("HW3/Crimes_-_2001_to_present.csv")


   

