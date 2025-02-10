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

# Read data from a Glue catalog table
# datasource = glueContext.create_dynamic_frame.from_catalog(database = "your_database", table_name = "your_table")

# Convert to DataFrame
# df = datasource.toDF()

glueContext.create_dynamic_frame()

data = [("Java", "20000"), ("Python", "100000"), ("Scala", "3000")]
df = spark.createDataFrame(data)
df.show()

# Write DataFrame to HDFS
df.write.format("parquet").save("hdfs://localhost:19000/test-parquet")

df2 = spark.read.format("parquet").load("hdfs://localhost:19000/test-parquet")
df2.show()
# job.commit()

jdbcDF = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://192.168.56.103:5432/postgres") \
    .option("dbtable", "movies.ratings") \
    .option("user", "postgres") \
    .option("password", "tesT123?") \
    .load()

moviesDF = spark.read.format('csv').option("header","true").load("hdfs://localhost:19000/movies-input/movies.csv")
linksDF = spark.read.format('csv').option("header","true").load("hdfs://localhost:19000/movies-input/links.csv")
ratingsDF = spark.read.format('csv').option("header","true").load("hdfs://localhost:19000/movies-input/ratings.csv")
tagsDF = spark.read.format('csv').option("header","true").load("hdfs://localhost:19000/movies-input/tags.csv")

# dfs = [moviesDF, linksDF, ratingsDF, tagsDF]

# moviesRatingsDF = reduce(lambda df1, df2: df1.join(df2, on="id", how="inner"), dfs)

# moviesRatingsDF = moviesDF.join(linksDF, on="movieId", how="full") \
#     .join(ratingsDF, on="movieId", how="full").withColumnRenamed('timestamp', 'rating_timestamp') \
#     .join(tagsDF, on=["movieId","userId"], how="full").withColumnRenamed('timestamp', 'tag_timestamp')  

moviesRatingsDF = moviesDF.join(linksDF, on="movieId", how="full") \
    .join(ratingsDF, on="movieId", how="full") \
    .join(tagsDF, on=["movieId","userId","timestamp"], how="full")  

# where there is null data on join columns, sometime youll get oom error
moviesRatingsDF = moviesRatingsDF.fillna("Unknown")

moviesRatingsDF.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://192.168.56.103:5432/postgres") \
    .option("dbtable", "movies.movies_ratings") \
    .option("user", "postgres") \
    .option("password", "tesT123?") \
    .save()

ratingsTagsDF = ratingsDF.join(tagsDF, on="movieId", how="full") 


ratingsTagsDF = Join.apply(tagsDF, ratingsDF["movieId"] == tagsDF["movieId"], "movieId", "movieId") 

ratingsDYF = DynamicFrame.fromDF(ratingsDF, glueContext, "test")

tagsDYF = DynamicFrame.fromDF(tagsDF, glueContext, "test2")

ratingsTagsDYF = Join.apply(tagsDYF, ratingsDYF["movieId"] == tagsDYF["movieId"], "movieId", "movieId") 

ratingsCountDF = ratingsDF.groupby('rating').count()

ratingsDF.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://192.168.56.103:5432/postgres") \
    .option("dbtable", "movies.ratings") \
    .option("user", "postgres") \
    .option("password", "tesT123?") \
    .save()

ratingsDF.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://192.168.56.103:5432/postgres") \
    .option("dbtable", "movies.ratings") \
    .option("user", "postgres") \
    .option("password", "tesT123?") \
    .option("batchSize",10000) \
    .save()

ratingsDF.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://192.168.56.103:5432/postgres") \
    .option("dbtable", "movies.ratings") \
    .option("user", "postgres") \
    .option("password", "tesT123?") \
    .option("partitionColumn", "rating") \
    .option("lowerBound", 0.5) \
    .option("upperBound", 5.0) \
    .option("numPartitions", 10) \
    .option("batchSize",100000) \
    .save()

