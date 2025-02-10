import sys
from awsglue.transforms import *
from awsglue.context import GlueContext
from functools import reduce
from awsglue.transforms import Join
from awsglue.dynamicframe import DynamicFrame

# Initialize Glue context
# sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# write it to postgres
moviesRatingsDF = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://192.168.56.103:5432/postgres") \
    .option("dbtable", "movies.movies_ratings") \
    .option("user", "postgres") \
    .option("password", "tesT123?") \
    .option("partitionColumn", "row_number") \
    .option("lowerBound", 1) \
    .option("upperBound", 34003312) \
    .option("numPartitions", 341) \
    .load()

moviesRatingsDF.write.format("parquet").save("hdfs://localhost:19000/movies-ratings-parquet")
