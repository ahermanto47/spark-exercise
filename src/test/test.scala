def randomStringGen(length: Int) = scala.util.Random.alphanumeric.take(length).mkString

val df = spark.sparkContext.parallelize(Seq.fill(4000){(randomStringGen(4), randomStringGen(4), randomStringGen(6))}, 10).toDF("col_1", "col_2", "col_3")

df.show