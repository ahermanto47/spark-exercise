import sys
from awsglue.transforms import *
from awsglue.context import GlueContext
from functools import reduce
from awsglue.transforms import Join
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import col, from_unixtime, row_number, lit
from pyspark.sql import Window

# Initialize Glue context
# sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# download the data from https://grouplens.org/datasets/movielens/
moviesDF = spark.read.format('csv').option("inferschema", "true").option("quote", "\"").option("header","true").load("hdfs://localhost:19000/movies-input/movies.csv")
linksDF = spark.read.format('csv').option("inferschema", "true").option("quote", "\"").option("header","true").load("hdfs://localhost:19000/movies-input/links.csv")
ratingsDF = spark.read.format('csv').option("inferschema", "true").option("quote", "\"").option("header","true").load("hdfs://localhost:19000/movies-input/ratings.csv")
tagsDF = spark.read.format('csv').option("inferschema", "true").option("quote", "\"").option("header","true").load("hdfs://localhost:19000/movies-input/tags.csv")

# using inner join, to get only matching data (no null values), smaller data size
# moviesRatingsDF = moviesDF.join(linksDF, on="movieId", how="inner") \
#     .join(ratingsDF, on="movieId", how="inner").withColumnRenamed('timestamp', 'rating_timestamp') \
#     .join(tagsDF, on=["movieId","userId","timestamp"], how="inner").withColumnRenamed('timestamp', 'tag_timestamp')  

# using full join, larger size, but there is null records
moviesRatingsDF = moviesDF.join(linksDF, on="movieId", how="full") \
    .join(ratingsDF, on="movieId", how="full") \
    .join(tagsDF, on=["movieId","userId","timestamp"], how="full")  

# where there is null data on join columns, sometime youll get oom error
moviesRatingsDF = moviesRatingsDF.fillna({
    "movieId":0,
    "userId":0,
    "timestamp":0,
    "title":"",
    "genres":"",
    "imdbId":0,
    "tmdbId":0,
    "rating":0,
    "tag":"",
}) 

# # add date column from timestamp
# moviesRatingsDF = moviesRatingsDF.withColumn("date", from_unixtime(col("timestamp")).cast("date"))

# Applying partitionBy() and orderBy()
# window_spec = Window.partitionBy("movieId").orderBy("timestamp")
window_spec = Window.orderBy(lit(1))

# Add a new column "id" using row_number() over the specified window
moviesRatingsDF = moviesRatingsDF.withColumn("row_number", row_number().over(window_spec))

# write it to postgres
moviesRatingsDF.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://192.168.56.103:5432/postgres") \
    .option("dbtable", "movies.movies_ratings") \
    .option("user", "postgres") \
    .option("password", "tesT123?") \
    .save()

# show the schema
moviesRatingsDF.printSchema()

# show the count
moviesRatingsDF.count()

# show the summary
moviesRatingsDF.summary()

# group by rating
ratingsCountDF = ratingsDF.groupby('rating').count()
ratingsCountDF.show()

