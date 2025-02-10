set SPARK_HOME=C:\\Users\\dad\\dev\\spark
set JAVA_HOME=C:\\Users\\dad\\dev\\jdk8u442-b06
set HADOOP_HOME=C:\\Users\\dad\\dev\\hadoop-3.3.6

set ROOT_DIR=C:\\Users\\dad\\workspace\\aws-glue-libs
cd %ROOT_DIR%

set SPARK_CONF_DIR=%ROOT_DIR%\\conf
set GLUE_JARS_DIR=%ROOT_DIR%\\jarsv1

set PYTHONPATH=
set PYTHONPATH=%SPARK_HOME%\python;%PYTHONPATH%
set PYTHONPATH=%SPARK_HOME%\python\lib\py4j-0.10.9.5-src.zip;%PYTHONPATH%

if exist PyGlue.zip del PyGlue.zip
7z a PyGlue.zip awsglue
set PYTHONPATH=%ROOT_DIR%\PyGlue.zip;%PYTHONPATH%

@REM # Run mvn copy-dependencies target to get the Glue dependencies locally
@REM mvn -f $ROOT_DIR/pom.xml -DoutputDirectory=$ROOT_DIR/jarsv1 dependency:copy-dependencies

if exist %SPARK_CONF_DIR% rmdir /s /q %SPARK_CONF_DIR%
mkdir %SPARK_CONF_DIR%
echo spark.driver.extraClassPath %SPARK_HOME%\\jars\\*;%GLUE_JARS_DIR%\\* >> %ROOT_DIR%\conf\spark-defaults.conf
echo spark.executor.extraClassPath %SPARK_HOME%\\jars\\*;%GLUE_JARS_DIR%\\* >> %ROOT_DIR%\conf\spark-defaults.conf
echo spark.driver.memory 4g >> %ROOT_DIR%\conf\spark-defaults.conf
echo spark.driver.cores 2 >> %ROOT_DIR%\conf\spark-defaults.conf
echo spark.executor.memory 4g >> %ROOT_DIR%\conf\spark-defaults.conf
echo spark.executor.cores 2 >> %ROOT_DIR%\conf\spark-defaults.conf

set PYSPARK_PYTHON=python