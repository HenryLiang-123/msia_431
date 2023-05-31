from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql import Window
from pyspark.sql.functions import avg, lag, col
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
import datetime
import numpy as np

def get_mape(path):
    spark = SparkSession.builder.appName('hw4').getOrCreate()
    df = spark.read.csv(path, header=True, inferSchema=True)

    df = df.withColumn('bar_range', F.floor((df.bar_num - 1) / 10)) # starts from 1
    df = df.withColumn('bar_range', df.bar_range.cast("int"))


    # Calculate average profit per bar_range and trade_id
    df_range_avg = df.groupBy("trade_id", "bar_range").agg(avg("profit").alias("avg_profit"))

    # Define a window partitioned by trade_id and ordered by bar_range
    window = Window.partitionBy('trade_id').orderBy('bar_range')

    # Create profit_lag column, which is the lagged cumulative average of avg_profit
    df_range_avg = df_range_avg.withColumn('cumulative_avg_profit', avg('avg_profit').over(window))
    df_range_avg = df_range_avg.withColumn('profit_lag', lag('cumulative_avg_profit').over(window))

    df_new = df.join(df_range_avg, ['trade_id', 'bar_range'], 'left').fillna(0)

    mape_list = []
    results_string = ""

    # Define your feature columns
    feature_columns = ['bar_range', 'direction', 'var12', 'var13', 'var14', 'var15', 'var16', 
                    'var17', 'var18', 'var23', 'var24', 'var25', 'var26', 'var27', 'var28', 'var34', 'var35', 'var36',
                    'var37', 'var38', 'var45', 'var46', 'var47', 'var48', 'var56', 'var57', 'var58', 'var67',
                    'var68', 'var78', 'profit_lag']

    # Initialize the VectorAssembler with the input and output column names
    assembler = VectorAssembler(inputCols=feature_columns, outputCol='features')

    # Read the dataset
    df = df_new

    # Sort the dataframe by time_stamp
    df = df.orderBy('time_stamp')

    # Create a month_year column to group data
    df = df.withColumn('month_year', F.date_format('time_stamp', 'yyyy-MM'))

    # Assemble the features
    df = assembler.transform(df)

    # Cache the dataframe
    df.cache()

    # Set up the initial training period
    start_date = df.agg({"time_stamp": "min"}).collect()[0]["min(time_stamp)"]
    end_date = start_date + datetime.timedelta(6*365/12)

        # Set up the rolling window
    while end_date <= datetime.datetime(2015, 8, 3, 11, 15):
        # Define the training data
        train_df = df.filter((df['time_stamp'] >= start_date) & (df['time_stamp'] < end_date))

        # Fit the model
        lr = LinearRegression(featuresCol='features', labelCol='profit')
        model = lr.fit(train_df)

        # Define the test data (one month after the training period)
        test_date = end_date + datetime.timedelta(365/12)
        test_df = df.filter((df['time_stamp'] >= end_date) & (df['time_stamp'] < test_date))

        # Make predictions
        predictions = model.transform(test_df)

        # Evaluate the model
        mape = predictions.select(F.abs((F.col('profit') - F.col('prediction')) / F.col('profit')).alias('mape')).agg(F.mean('mape')).first()[0]
        mape_list.append(mape)

        results_string += f"Current training period is {start_date.strftime('%Y-%m')} and {end_date.strftime('%Y-%m')}\n"
        results_string += f"MAPE for prediction period {end_date.strftime('%Y-%m')} to {test_date.strftime('%Y-%m')}: {mape}\n"
        
        # Shift the training window
        start_date = test_date
        end_date = start_date + datetime.timedelta(6*365/12)

    results_string += f"Max MAPE: {max(mape_list)}\n"
    results_string += f"Min MAPE: {min(mape_list)}\n"
    results_string += f"Average MAPE: {np.mean(mape_list)}\n"
    new_df = spark.createDataFrame([(results_string, )], ["Results"])
    new_df.coalesce(1).write.text("s3://hwl6390-hw4/Exercise3.txt")

if __name__ == "__main__":
    get_mape('s3://msia-432-hw4-data/full_data.csv')
