# spark-exercise on standalone spark and hadoop on your local machine

> This is probably the simplest setup if you have limited resources (like plain vanilla laptop or desktop). Basically, you run one spark instance on a single node hadoop cluster. Here are the steps to setup your local environment

1. login as hadoop

```
su - hadoop
```

2. start hadoop and yarn

```
~/hadoop-3.3.4/sbin/start-dfs.sh

~/hadoop-3.3.4/sbin/start-yarn.sh
```

3. initialize hdfs

```
hadoop-3.3.4/bin/hdfs namenode -format

hadoop-3.3.4/bin/hdfs dfs -ls /user/hadoop

hadoop-3.3.4/bin/hdfs dfs -put rossmann-store-sales/train.csv
```

4. commands related with ms sql server instance integration

```
kubectl exec -it mssql-0 -- bash

/opt/mssql-tools18/bin/sqlcmd -No -U sa
```

5. jdbc driver error is solved by using mssql-jdbc-12.8.1.jre8.jar place it in $SPARK_HOME/jars folder. Note the jre8 part because we are using openjdk 8
    
6. commands to start spark

```
spark-3.5.3-bin-hadoop3/bin/spark-shell --master yarn --name interactive
        
spark-3.5.3-bin-hadoop3/bin/pyspark --master yarn --name interactive
        
spark-3.5.3-bin-hadoop3/bin/spark-submit --master yarn --name interactive test-mssql.py

spark-3.5.3-bin-hadoop3/bin/spark-submit --class MSSQLStoredProcedureCall --master yarn ~/scala_work_dir/mssql_sp_demo/target/scala-2.12/mssql-store-procedure_2.12-1.0.jar
```

7. scala commands after testing scala in spark-shell, build dir structure like scala_work_dir, then run 

```
sbt package
```

8. execute unit test

```
cd ms-sql/unit-testing

/opt/mssql-tools/bin/sqlcmd -No -S "192.168.39.110,32611" -U sa -C -P password123 -i test1.sql
```

## known issues on store procedure call with pyspark

1. issue retrieving out parameter

## known issues on store procedure call with scala

1. use java native sql classes

