# spark-exercise on standalone spark and hadoop on your local machine

> This is probably the simplest setup if you have limited resources (like plain vanilla laptop or desktop). Basically, you run one spark instance on a single node hadoop cluster.

4. commands to run working local node
    1. su - hadoop
    2. start hadoop and yarn
        1. ~/hadoop-3.3.4/sbin/start-dfs.sh
        2. ~/hadoop-3.3.4/sbin/start-yarn.sh
    3. commands to interact with hdfs
        1. hadoop-3.3.4/bin/hdfs namenode -format
        1. hadoop-3.3.4/bin/hdfs dfs -ls /user/hadoop
        2. hadoop-3.3.4/bin/hdfs dfs -put rossmann-store-sales/train.csv
    4. commands related with ms sql server instance
        1. kubectl exec -it mssql-0 -- bash
        2. /opt/mssql-tools18/bin/sqlcmd -No -U sa
    5. jdbc driver error is solved by using mssql-jdbc-12.8.1.jre8.jar place it in $SPARK_HOME/jars folder. Note the jre8 part because we are using openjdk 8
    6. commands to start spark
        1. spark-3.5.3-bin-hadoop3/bin/spark-shell --master yarn --name interactive
        2. spark-3.5.3-bin-hadoop3/bin/pyspark --master yarn --name interactive
        3. spark-3.5.3-bin-hadoop3/bin/spark-submit --master yarn --name interactive test-mssql.py
        4. spark-3.5.3-bin-hadoop3/bin/spark-submit --class MSSQLStoredProcedureCall --master yarn ~/scala_work_dir/mssql_sp_demo/target/scala-2.12/mssql-store-procedure_2.12-1.0.jar
    7. scala commands
        1. after testing scala in spark-shell, build dir structure like scala_work_dir, then run 'sbt package'
    8. store procedure call with pyspark and scala:
        1. pyspark
            a. issue retrieving out parameter
        2. scala
            b. use java native sql classes
    9. execute unit test
        1. cd ms-sql/unit-testing
        2. /opt/mssql-tools/bin/sqlcmd -No -S "192.168.39.110,32611" -U sa -C -P password123 -i test1.sql
