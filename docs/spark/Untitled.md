# Import all the functions


```python
#Importing all Required Packages
from pyspark.sql.functions import to_date, col, sum as _sum, when
import pyspark.sql.functions as f
from pyspark.sql.functions import date_format, current_date, udf
import pandas as pd
import numpy as np
import random
import datetime
import re
from pyspark.sql.types import StringType, MapType
from pyspark.sql.types import *
import warnings
import pyspark
from pyspark.sql.functions import current_timestamp
from pyspark.sql import SparkSession
from datetime import datetime, timedelta
from pyspark.sql.functions import lit, date_add
from pyspark.sql import Window
from pyspark.sql.functions import row_number
import sys
from pyspark.sql.types import StructType, StructField, StringType, IntegerType #
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import col
```


```python
# --------------------------------------------------------------------------------------------------------------------------
# Setting Up the Configurations for pySpark
# --------------------------------------------------------------------------------------------------------------------------
conf = (pyspark.SparkConf().set('spark.driver.memory', '10G')\
        .set('spark.executor.memory', '10G')\
        .set('spark.driver.maxResultSize', '10G')\
        .set('spark.dynamicAllocation.enabled', 'false')\
        .set('spark.dynamicAllocaton.maxExecutors', '4')\
        .set('spark.master','local[4]')\
        .set('spark.driver.extraClassPath', '/data2/pythonuser/ngdbc-2.3.48.jar'))

# --------------------------------------------------------------------------------------------------------------------------
# Fetching or Creating a Session for this Activity
# --------------------------------------------------------------------------------------------------------------------------
spark = SparkSession.builder.config(conf = conf).appName("pyspark2").enableHiveSupport().getOrCreate()

spark
```

    Setting default log level to "WARN".
    To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).






    <div>
        <p><b>SparkSession - hive</b></p>

<div>
    <p><b>SparkContext</b></p>

    <p><a href="http://10.129.130.96:4040">Spark UI</a></p>

    <dl>
      <dt>Version</dt>
        <dd><code>v3.5.3</code></dd>
      <dt>Master</dt>
        <dd><code>local[4]</code></dd>
      <dt>AppName</dt>
        <dd><code>pyspark2</code></dd>
    </dl>
</div>

    </div>




# spark read modes
When reading data (e.g., from CSV, JSON, etc.) in Apache Spark using DataFrameReader, you can specify how Spark should handle malformed or corrupted records using the mode option. Below are the available modes:

| Mode           | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| failFast   | Terminates the query immediately if any malformed record is encountered. This is useful when data integrity is critical. |
| dropMalformed | Drops all rows containing malformed records. This can be useful when you prefer to skip bad data instead of failing the entire job. |
| permissive (default) | Tries to parse all records. If a record is corrupted or missing fields, Spark sets `null` values for corrupted fields and puts malformed data into a special column named `_corrupt_record`. |


```python
#Read dataframe with header false
flight_df = spark.read.format("csv") \
                .option("header", "false") \
                .option("inferschema","false")\
                .option("mode","FAILFAST")\
                .load("/sandbox/DataEngineering/manish/pyspark/flightdata.csv") 

flight_df.show()
```

    25/08/05 15:55:46 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
    25/08/05 15:55:46 WARN DomainSocketFactory: The short-circuit local reads feature cannot be used because libhadoop cannot be loaded.


    +--------------------+-------------------+-----+
    |                 _c0|                _c1|  _c2|
    +--------------------+-------------------+-----+
    |   DEST_COUNTRY_NAME|ORIGIN_COUNTRY_NAME|count|
    |       United States|            Romania|    1|
    |       United States|            Ireland|  264|
    |       United States|              India|   69|
    |               Egypt|      United States|   24|
    |   Equatorial Guinea|      United States|    1|
    |       United States|          Singapore|   25|
    |       United States|            Grenada|   54|
    |          Costa Rica|      United States|  477|
    |             Senegal|      United States|   29|
    |       United States|   Marshall Islands|   44|
    |              Guyana|      United States|   17|
    |       United States|       Sint Maarten|   53|
    |               Malta|      United States|    1|
    |             Bolivia|      United States|   46|
    |            Anguilla|      United States|   21|
    |Turks and Caicos ...|      United States|  136|
    |       United States|        Afghanistan|    2|
    |Saint Vincent and...|      United States|    1|
    |               Italy|      United States|  390|
    +--------------------+-------------------+-----+
    only showing top 20 rows
    



```python
#Read dataframe with header true
flight_df2 = spark.read.format("csv") \
                .option("header", "true") \
                .option("inferschema","false")\
                .option("mode","FAILFAST")\
                .load("/sandbox/DataEngineering/manish/pyspark/flightdata.csv") 

flight_df2.show()
```

    +--------------------+-------------------+-----+
    |   DEST_COUNTRY_NAME|ORIGIN_COUNTRY_NAME|count|
    +--------------------+-------------------+-----+
    |       United States|            Romania|    1|
    |       United States|            Ireland|  264|
    |       United States|              India|   69|
    |               Egypt|      United States|   24|
    |   Equatorial Guinea|      United States|    1|
    |       United States|          Singapore|   25|
    |       United States|            Grenada|   54|
    |          Costa Rica|      United States|  477|
    |             Senegal|      United States|   29|
    |       United States|   Marshall Islands|   44|
    |              Guyana|      United States|   17|
    |       United States|       Sint Maarten|   53|
    |               Malta|      United States|    1|
    |             Bolivia|      United States|   46|
    |            Anguilla|      United States|   21|
    |Turks and Caicos ...|      United States|  136|
    |       United States|        Afghanistan|    2|
    |Saint Vincent and...|      United States|    1|
    |               Italy|      United States|  390|
    |       United States|             Russia|  156|
    +--------------------+-------------------+-----+
    only showing top 20 rows
    



```python
flight_df2.printSchema()
```

    root
     |-- DEST_COUNTRY_NAME: string (nullable = true)
     |-- ORIGIN_COUNTRY_NAME: string (nullable = true)
     |-- count: string (nullable = true)
    



```python
#Read dataframe with inferschema true
flight_df3 = spark.read.format("csv") \
                .option("header", "true") \
                .option("inferschema","true")\
                .option("mode","FAILFAST")\
                .load("/sandbox/DataEngineering/manish/pyspark/flightdata.csv") 

flight_df3.printSchema()
```

    root
     |-- DEST_COUNTRY_NAME: string (nullable = true)
     |-- ORIGIN_COUNTRY_NAME: string (nullable = true)
     |-- count: integer (nullable = true)
    


# schema in spark
There are two primary methods: using **StructType** and **StructField** classes, and using a DDL (Data Definition Language) string.

These are classes in Spark used to define the schema structure.

**StructField** represents a single column within a DataFrame. It holds information such as the column's name, its data type (e.g., String, Integer, Timestamp), and whether it can contain null values (nullable: True/False). If nullable is set to False, the column cannot contain NULL values, and an error will be thrown if it does.

**StructType** defines the overall structure of a DataFrame. It is essentially a list or collection of StructField objects. When you combine ID, Name, and Age fields, for example, they define the structure of a record, and a collection of such records forms a DataFrame.

What happens if you set header=False when your data actually has a header? If you disable the header option (header=False) but your CSV file contains a header row, Spark will treat that header row as regular data. If this header row's values do not match the data types defined in your manual schema (e.g., a string "Count" being read into an Integer column), it can lead to null values in that column if the read mode is set to permissive, or an error if the mode is failfast


```python
# Define the schema using StructType and StructField
my_schema = StructType([
    StructField("DEST_COUNTRY_NAME", StringType(), True),  
    StructField("ORIGIN_COUNTRY_NAME", StringType(), True),  
    StructField("count", IntegerType(), True)  
])
my_schema
```




    StructType([StructField('DEST_COUNTRY_NAME', StringType(), True), StructField('ORIGIN_COUNTRY_NAME', StringType(), True), StructField('count', IntegerType(), True)])




```python
#Read dataframe with inferschema true
flight_df4 = spark.read.format("csv") \
                .option("header", "true") \
                .option("inferschema","false")\
                .option("skipRows",1)\
                .schema(my_schema)\
                .option("mode","PERMISSIVE")\
                .load("/sandbox/DataEngineering/manish/pyspark/flightdata.csv") 

flight_df4.printSchema()
```

    root
     |-- DEST_COUNTRY_NAME: string (nullable = true)
     |-- ORIGIN_COUNTRY_NAME: string (nullable = true)
     |-- count: integer (nullable = true)
    


# handling corrupted records
When reading data, Spark offers different modes to handle corrupted records, which influence how the DataFrame is populated.

In **permissive mode**, all records are allowed to enter the DataFrame. If a record is corrupted, Spark sets the malformed values to null and does not throw an error. For the example data with five total records (two corrupted), permissive mode will result in five records in the DataFrame, with nulls where data is bad.

In **dropMalformed mode**, Spark discards any record it identifies as corrupted. Given the example data has two corrupted records out of five, this mode will produce a DataFrame with three records

In **failfast mode**, Spark immediately throws an error and stops the job as soon as it encounters the first corrupted record. This mode will result in zero records in the DataFrame because the job will fail.


```python
employee = spark.read.format("csv") \
                .option("header", "true") \
                .option("inferschema","true")\
                .option("mode","PERMISSIVE")\
                .load("/sandbox/DataEngineering/manish/pyspark/employee.csv") 

employee.show()
```

    +---+--------+---+------+------------+--------+
    | id|    name|age|salary|     address| nominee|
    +---+--------+---+------+------------+--------+
    |  1|  Manish| 26| 75000|       bihar|nominee1|
    |  2|  Nikita| 23|100000|uttarpradesh|nominee2|
    |  3|  Pritam| 22|150000|   Bangalore|   India|
    |  4|Prantosh| 17|200000|     Kolkata|   India|
    |  5|  Vikash| 31|300000|        NULL|nominee5|
    +---+--------+---+------+------------+--------+
    



```python
employee1 = spark.read.format("csv") \
                .option("header", "true") \
                .option("inferschema","true")\
                .option("mode","dropmalformed")\
                .load("/sandbox/DataEngineering/manish/pyspark/employee.csv") 

employee1.show()
```

    +---+------+---+------+------------+--------+
    | id|  name|age|salary|     address| nominee|
    +---+------+---+------+------------+--------+
    |  1|Manish| 26| 75000|       bihar|nominee1|
    |  2|Nikita| 23|100000|uttarpradesh|nominee2|
    |  5|Vikash| 31|300000|        NULL|nominee5|
    +---+------+---+------+------------+--------+
    



```python

```

# print bad records
To specifically identify and view the corrupted records, you need to define a manual schema that includes a special column named _corrupt_record. This column will capture the raw content of the corrupted record.

Where to store bad record For scenarios with a large volume of corrupted records (e.g., thousands), printing them is not practical. Spark provides the badRecordsPath option to store all corrupted records in a specified location. These records are saved in JSON format at the designated path




```python
empschema = StructType([
    StructField("id", IntegerType(), True),  
    StructField("name", StringType(), True),  
    StructField("age", IntegerType(), True),
    StructField("salary", IntegerType(), True), 
    StructField("address", StringType(), True), 
    StructField("nominee", StringType(), True),
    StructField("_corrupt_record", StringType(), True),
])
empschema
```




    StructType([StructField('id', IntegerType(), True), StructField('name', StringType(), True), StructField('age', IntegerType(), True), StructField('salary', IntegerType(), True), StructField('address', StringType(), True), StructField('nominee', StringType(), True), StructField('_corrupt_record', StringType(), True)])




```python
employee3 = spark.read.format("csv") \
                .option("header", "true") \
                .option("inferschema","true")\
                .option("mode","PERMISSIVE")\
                .schema(empschema)\
                .load("/sandbox/DataEngineering/manish/pyspark/employee.csv") 

employee3.show()
employee3.show(truncate=False)
```

    +---+--------+---+------+------------+--------+--------------------+
    | id|    name|age|salary|     address| nominee|     _corrupt_record|
    +---+--------+---+------+------------+--------+--------------------+
    |  1|  Manish| 26| 75000|       bihar|nominee1|                NULL|
    |  2|  Nikita| 23|100000|uttarpradesh|nominee2|                NULL|
    |  3|  Pritam| 22|150000|   Bangalore|   India|3,Pritam,22,15000...|
    |  4|Prantosh| 17|200000|     Kolkata|   India|4,Prantosh,17,200...|
    |  5|  Vikash| 31|300000|        NULL|nominee5|                NULL|
    +---+--------+---+------+------------+--------+--------------------+
    
    +---+--------+---+------+------------+--------+-------------------------------------------+
    |id |name    |age|salary|address     |nominee |_corrupt_record                            |
    +---+--------+---+------+------------+--------+-------------------------------------------+
    |1  |Manish  |26 |75000 |bihar       |nominee1|NULL                                       |
    |2  |Nikita  |23 |100000|uttarpradesh|nominee2|NULL                                       |
    |3  |Pritam  |22 |150000|Bangalore   |India   |3,Pritam,22,150000,Bangalore,India,nominee3|
    |4  |Prantosh|17 |200000|Kolkata     |India   |4,Prantosh,17,200000,Kolkata,India,nominee4|
    |5  |Vikash  |31 |300000|NULL        |nominee5|NULL                                       |
    +---+--------+---+------+------------+--------+-------------------------------------------+
    



```python
employee3 = spark.read.format("csv") \
                .option("header", "true") \
                .option("inferschema","true")\
                .option("mode","PERMISSIVE")\
                .schema(empschema)\
                .option("badRecordsPath","/sandbox/DataEngineering/manish/pyspark/badrecords")\
                .load("/sandbox/DataEngineering/manish/pyspark/employee.csv") 

employee3.show()
employee3.show(truncate=False)
```

    +---+--------+---+------+------------+--------+--------------------+
    | id|    name|age|salary|     address| nominee|     _corrupt_record|
    +---+--------+---+------+------------+--------+--------------------+
    |  1|  Manish| 26| 75000|       bihar|nominee1|                NULL|
    |  2|  Nikita| 23|100000|uttarpradesh|nominee2|                NULL|
    |  3|  Pritam| 22|150000|   Bangalore|   India|3,Pritam,22,15000...|
    |  4|Prantosh| 17|200000|     Kolkata|   India|4,Prantosh,17,200...|
    |  5|  Vikash| 31|300000|        NULL|nominee5|                NULL|
    +---+--------+---+------+------------+--------+--------------------+
    
    +---+--------+---+------+------------+--------+-------------------------------------------+
    |id |name    |age|salary|address     |nominee |_corrupt_record                            |
    +---+--------+---+------+------------+--------+-------------------------------------------+
    |1  |Manish  |26 |75000 |bihar       |nominee1|NULL                                       |
    |2  |Nikita  |23 |100000|uttarpradesh|nominee2|NULL                                       |
    |3  |Pritam  |22 |150000|Bangalore   |India   |3,Pritam,22,150000,Bangalore,India,nominee3|
    |4  |Prantosh|17 |200000|Kolkata     |India   |4,Prantosh,17,200000,Kolkata,India,nominee4|
    |5  |Vikash  |31 |300000|NULL        |nominee5|NULL                                       |
    +---+--------+---+------+------------+--------+-------------------------------------------+
    


# read json in spark


```python
json = spark.read.format("json") \
                .option("inferschema","true")\
                .option("mode","PERMISSIVE")\
                .load("/sandbox/DataEngineering/manish/pyspark/line_delimeted.json").show()
```

    [Stage 16:>                                                         (0 + 1) / 1]

    +---+--------+------+
    |age|    name|salary|
    +---+--------+------+
    | 20|  Manish| 20000|
    | 25|  Nikita| 21000|
    | 16|  Pritam| 22000|
    | 35|Prantosh| 25000|
    | 67|  Vikash| 40000|
    +---+--------+------+
    


                                                                                    


```python
json2 = spark.read.format("json") \
                .option("inferschema","true")\
                .option("mode","PERMISSIVE")\
                .load("/sandbox/DataEngineering/manish/pyspark/single_file.json").show()
```

    +---+------+--------+------+
    |age|gender|    name|salary|
    +---+------+--------+------+
    | 20|  NULL|  Manish| 20000|
    | 25|  NULL|  Nikita| 21000|
    | 16|  NULL|  Pritam| 22000|
    | 35|  NULL|Prantosh| 25000|
    | 67|     M|  Vikash| 40000|
    +---+------+--------+------+
    



```python
json3 = spark.read.format("json") \
                .option("inferschema","true")\
                .option("mode","PERMISSIVE")\
                .option("multiline","True")\
                .load("/sandbox/DataEngineering/manish/pyspark/multiline.json").show()

json4 = spark.read.format("json") \
                .option("inferschema","true")\
                .option("mode","PERMISSIVE")\
                .option("multiline","True")\
                .load("/sandbox/DataEngineering/manish/pyspark/corrupted_json").show()
```

                                                                                    

    +---+--------+------+
    |age|    name|salary|
    +---+--------+------+
    | 20|  Manish| 20000|
    | 25|  Nikita| 21000|
    | 16|  Pritam| 22000|
    | 35|Prantosh| 25000|
    | 67|  Vikash| 40000|
    +---+--------+------+
    
    +---+------+------+
    |age|  name|salary|
    +---+------+------+
    | 20|Manish| 20000|
    +---+------+------+
    


# write dataframe
When working with Spark, after you have read data into a DataFrame and performed transformations, it is crucial to write the processed data back to disk to ensure its persistence. Currently, all the transformations and data processing occur in memory, so writing to disk makes the data permanent.
Here's a detailed explanation with code examples and notes based on the provided sources:

!!! Code

        # Assuming 'df' is your DataFrame
        # Define your base location where you want to save the output
        base_location = "/user/hive/warehouse/your_database/output/"

        # Construct the full path for the CSV output folder
        output_path = base_location + "csv_write/"

        # Write the DataFrame to disk
        df.write \
            .format("csv") \
            .option("header", "true") \
            .mode("overwrite") \
            .save(output_path)

**General Structure for Writing a DataFrame to Disk**

The general structure for writing a DataFrame using the Spark DataFrame Writer API is as follows:

DataFrame.write: This is the starting point, indicating that you intend to write a DataFrame.

   .format(): Specifies the file format in which you want to save the data. Common formats include CSV or Parquet. If no format is explicitly passed, Spark will default to Parquet.
   
   .option(): Allows you to pass multiple options. For example, you can specify whether to include a header for CSV files (e.g., header as True). You can also specify the output path using path option, though save() method usually handles the path directly.

   .mode(): Defines how Spark should behave if files or directories already exist at the target location. This is a very important aspect of writing data.
   
   .partitionBy(): (To be covered in a dedicated video mentioned in the source) This method allows you to partition the output data based on one or more columns, creating separate folders for each partition.

   .bucketBy(): (To be covered in a dedicated video mentioned in the source) Similar to partitionBy, but it organizes data into a fixed number of buckets within partitions.

   .save(): This is the final action that triggers the write operation and specifies the output path where the DataFrame will be written.

A typical flow looks like: **df.write.format(...).option(...).mode(...).save(path)**.

**Modes in DataFrame Writer API**

The mode() method in the DataFrame Writer API is crucial as it dictates how Spark handles existing data at the target location. There are four primary modes:

**append**
 
 Functionality: If files already exist at the specified location, the new data from the DataFrame will be added to the existing files.

 Example: If there were three files previously, and a new output DataFrame comes, it will simply append its data to that list of files.

**overwrite**

 Functionality: This mode deletes any existing files at the target location before writing the new DataFrame.

 Example: If a previous file had records, overwrite will delete all old files and only the new file with its records (e.g., five new records) will be visible.

**errorIfExists**

 Functionality: Spark will check if a file or location already exists at the target path. If it does, the write operation will fail and throw an error.

 Use Case: Useful when you want to ensure that you do not accidentally overwrite or append to existing data.

**ignore**

 Functionality: If a file or location already exists at the target path, Spark will skip the write operation entirely without throwing an error. The new file will not be written.

 Use Case: This mode is suitable if you want to prevent new data from being written if data is already present, perhaps to avoid overwriting changes or to ensure data integrity




df.write \
    .format("csv") \
    .option("header", "true") \
    .option("mode", "overwrite") \
    .option("path", "/sandbox/DataEngineering/manish/pyspark") \
    .save()

# paritition in spark




```python
df = spark.read.format("csv") \
                .option("header", "true") \
                .option("inferschema","true")\
                .option("mode","PERMISSIVE")\
                .load("/sandbox/DataEngineering/manish/pyspark/part.csv") 

df.show()
```

    +---+--------+---+------+-------+------+
    | id|    name|age|salary|address|gender|
    +---+--------+---+------+-------+------+
    |  1|  Manish| 26| 75000|  INDIA|     m|
    |  2|  Nikita| 23|100000|    USA|     f|
    |  3|  Pritam| 22|150000|  INDIA|     m|
    |  4|Prantosh| 17|200000|  JAPAN|     m|
    |  5|  Vikash| 31|300000|    USA|     m|
    |  6|   Rahul| 55|300000|  INDIA|     m|
    |  7|    Raju| 67|540000|    USA|     m|
    |  8| Praveen| 28| 70000|  JAPAN|     m|
    |  9|     Dev| 32|150000|  JAPAN|     m|
    | 10|  Sherin| 16| 25000| RUSSIA|     f|
    | 11|    Ragu| 12| 35000|  INDIA|     f|
    | 12|   Sweta| 43|200000|  INDIA|     f|
    | 13| Raushan| 48|650000|    USA|     m|
    | 14|  Mukesh| 36| 95000| RUSSIA|     m|
    | 15| Prakash| 52|750000|  INDIA|     m|
    +---+--------+---+------+-------+------+
    


df.write \
    .format("csv") \
    .option("header", "true") \
    .option("mode", "overwrite") \
    .option("path", "/sandbox/DataEngineering/manish/pyspark/partbyid/") \
    .partitionBy("address")\
    .save()

df.write \
    .format("csv") \
    .option("header", "true") \
    .option("mode", "overwrite") \
    .option("path", "/sandbox/DataEngineering/manish/pyspark/partition/") \
    .partitionBy("address","gender")\
    .save()

# bucketing in pyspark
save doesnt work, need to use saveAsTable

df.write \
    .format("csv") \
    .option("header", "true") \
    .option("mode", "overwrite") \
    .option("path", "/sandbox/DataEngineering/manish/pyspark/bucket/") \
    .bucketBy(3,"id")\
    .saveAsTable("bucketbyid")

# column selection and expression 


```python
empdf = spark.read.format("csv") \
                .option("header", "true") \
                .option("inferschema","true")\
                .option("mode","PERMISSIVE")\
                .load("/sandbox/DataEngineering/manish/pyspark/part.csv") 

empdf.show()
empdf.printSchema()
empdf.columns
```

    +---+--------+---+------+-------+------+
    | id|    name|age|salary|address|gender|
    +---+--------+---+------+-------+------+
    |  1|  Manish| 26| 75000|  INDIA|     m|
    |  2|  Nikita| 23|100000|    USA|     f|
    |  3|  Pritam| 22|150000|  INDIA|     m|
    |  4|Prantosh| 17|200000|  JAPAN|     m|
    |  5|  Vikash| 31|300000|    USA|     m|
    |  6|   Rahul| 55|300000|  INDIA|     m|
    |  7|    Raju| 67|540000|    USA|     m|
    |  8| Praveen| 28| 70000|  JAPAN|     m|
    |  9|     Dev| 32|150000|  JAPAN|     m|
    | 10|  Sherin| 16| 25000| RUSSIA|     f|
    | 11|    Ragu| 12| 35000|  INDIA|     f|
    | 12|   Sweta| 43|200000|  INDIA|     f|
    | 13| Raushan| 48|650000|    USA|     m|
    | 14|  Mukesh| 36| 95000| RUSSIA|     m|
    | 15| Prakash| 52|750000|  INDIA|     m|
    +---+--------+---+------+-------+------+
    
    root
     |-- id: integer (nullable = true)
     |-- name: string (nullable = true)
     |-- age: integer (nullable = true)
     |-- salary: integer (nullable = true)
     |-- address: string (nullable = true)
     |-- gender: string (nullable = true)
    





    ['id', 'name', 'age', 'salary', 'address', 'gender']




```python
empdf.select('age').show()
```

    +---+
    |age|
    +---+
    | 26|
    | 23|
    | 22|
    | 17|
    | 31|
    | 55|
    | 67|
    | 28|
    | 32|
    | 16|
    | 12|
    | 43|
    | 48|
    | 36|
    | 52|
    +---+
    



```python
empdf.select(col("name")).show()
```

    +--------+
    |    name|
    +--------+
    |  Manish|
    |  Nikita|
    |  Pritam|
    |Prantosh|
    |  Vikash|
    |   Rahul|
    |    Raju|
    | Praveen|
    |     Dev|
    |  Sherin|
    |    Ragu|
    |   Sweta|
    | Raushan|
    |  Mukesh|
    | Prakash|
    +--------+
    



```python
empdf.select(col("id")+5).show()
```

    +--------+
    |(id + 5)|
    +--------+
    |       6|
    |       7|
    |       8|
    |       9|
    |      10|
    |      11|
    |      12|
    |      13|
    |      14|
    |      15|
    |      16|
    |      17|
    |      18|
    |      19|
    |      20|
    +--------+
    



```python
empdf.select("id","name","age").show()
```

    +---+--------+---+
    | id|    name|age|
    +---+--------+---+
    |  1|  Manish| 26|
    |  2|  Nikita| 23|
    |  3|  Pritam| 22|
    |  4|Prantosh| 17|
    |  5|  Vikash| 31|
    |  6|   Rahul| 55|
    |  7|    Raju| 67|
    |  8| Praveen| 28|
    |  9|     Dev| 32|
    | 10|  Sherin| 16|
    | 11|    Ragu| 12|
    | 12|   Sweta| 43|
    | 13| Raushan| 48|
    | 14|  Mukesh| 36|
    | 15| Prakash| 52|
    +---+--------+---+
    



```python
empdf.select(col("id"),col("name")).show()
```

    +---+--------+
    | id|    name|
    +---+--------+
    |  1|  Manish|
    |  2|  Nikita|
    |  3|  Pritam|
    |  4|Prantosh|
    |  5|  Vikash|
    |  6|   Rahul|
    |  7|    Raju|
    |  8| Praveen|
    |  9|     Dev|
    | 10|  Sherin|
    | 11|    Ragu|
    | 12|   Sweta|
    | 13| Raushan|
    | 14|  Mukesh|
    | 15| Prakash|
    +---+--------+
    



```python
empdf.select("id",col("name"),empdf['salary'],empdf.address).show()
```

    +---+--------+------+-------+
    | id|    name|salary|address|
    +---+--------+------+-------+
    |  1|  Manish| 75000|  INDIA|
    |  2|  Nikita|100000|    USA|
    |  3|  Pritam|150000|  INDIA|
    |  4|Prantosh|200000|  JAPAN|
    |  5|  Vikash|300000|    USA|
    |  6|   Rahul|300000|  INDIA|
    |  7|    Raju|540000|    USA|
    |  8| Praveen| 70000|  JAPAN|
    |  9|     Dev|150000|  JAPAN|
    | 10|  Sherin| 25000| RUSSIA|
    | 11|    Ragu| 35000|  INDIA|
    | 12|   Sweta|200000|  INDIA|
    | 13| Raushan|650000|    USA|
    | 14|  Mukesh| 95000| RUSSIA|
    | 15| Prakash|750000|  INDIA|
    +---+--------+------+-------+
    



```python
empdf.select(expr("id +5")).show()
```

    +--------+
    |(id + 5)|
    +--------+
    |       6|
    |       7|
    |       8|
    |       9|
    |      10|
    |      11|
    |      12|
    |      13|
    |      14|
    |      15|
    |      16|
    |      17|
    |      18|
    |      19|
    |      20|
    +--------+
    



```python
empdf.select(expr("id as emp_id"),expr("name as emp_name"), expr("concat(emp_id, ' ', emp_name)")).show()
```

    +------+--------+-------------------------------------------------------------------------+
    |emp_id|emp_name|concat(lateralAliasReference(emp_id),  , lateralAliasReference(emp_name))|
    +------+--------+-------------------------------------------------------------------------+
    |     1|  Manish|                                                                 1 Manish|
    |     2|  Nikita|                                                                 2 Nikita|
    |     3|  Pritam|                                                                 3 Pritam|
    |     4|Prantosh|                                                               4 Prantosh|
    |     5|  Vikash|                                                                 5 Vikash|
    |     6|   Rahul|                                                                  6 Rahul|
    |     7|    Raju|                                                                   7 Raju|
    |     8| Praveen|                                                                8 Praveen|
    |     9|     Dev|                                                                    9 Dev|
    |    10|  Sherin|                                                                10 Sherin|
    |    11|    Ragu|                                                                  11 Ragu|
    |    12|   Sweta|                                                                 12 Sweta|
    |    13| Raushan|                                                               13 Raushan|
    |    14|  Mukesh|                                                                14 Mukesh|
    |    15| Prakash|                                                               15 Prakash|
    +------+--------+-------------------------------------------------------------------------+
    


# spark SQL


```python
empdf.createOrReplaceTempView('employeetable')
```


```python
sqldf = spark.sql(""" select * from employeetable """)
sqldf.show()
```

    +---+--------+---+------+-------+------+
    | id|    name|age|salary|address|gender|
    +---+--------+---+------+-------+------+
    |  1|  Manish| 26| 75000|  INDIA|     m|
    |  2|  Nikita| 23|100000|    USA|     f|
    |  3|  Pritam| 22|150000|  INDIA|     m|
    |  4|Prantosh| 17|200000|  JAPAN|     m|
    |  5|  Vikash| 31|300000|    USA|     m|
    |  6|   Rahul| 55|300000|  INDIA|     m|
    |  7|    Raju| 67|540000|    USA|     m|
    |  8| Praveen| 28| 70000|  JAPAN|     m|
    |  9|     Dev| 32|150000|  JAPAN|     m|
    | 10|  Sherin| 16| 25000| RUSSIA|     f|
    | 11|    Ragu| 12| 35000|  INDIA|     f|
    | 12|   Sweta| 43|200000|  INDIA|     f|
    | 13| Raushan| 48|650000|    USA|     m|
    | 14|  Mukesh| 36| 95000| RUSSIA|     m|
    | 15| Prakash| 52|750000|  INDIA|     m|
    +---+--------+---+------+-------+------+
    



```python
sqldf.select('*').show()
```

    +---+--------+---+------+-------+------+
    | id|    name|age|salary|address|gender|
    +---+--------+---+------+-------+------+
    |  1|  Manish| 26| 75000|  INDIA|     m|
    |  2|  Nikita| 23|100000|    USA|     f|
    |  3|  Pritam| 22|150000|  INDIA|     m|
    |  4|Prantosh| 17|200000|  JAPAN|     m|
    |  5|  Vikash| 31|300000|    USA|     m|
    |  6|   Rahul| 55|300000|  INDIA|     m|
    |  7|    Raju| 67|540000|    USA|     m|
    |  8| Praveen| 28| 70000|  JAPAN|     m|
    |  9|     Dev| 32|150000|  JAPAN|     m|
    | 10|  Sherin| 16| 25000| RUSSIA|     f|
    | 11|    Ragu| 12| 35000|  INDIA|     f|
    | 12|   Sweta| 43|200000|  INDIA|     f|
    | 13| Raushan| 48|650000|    USA|     m|
    | 14|  Mukesh| 36| 95000| RUSSIA|     m|
    | 15| Prakash| 52|750000|  INDIA|     m|
    +---+--------+---+------+-------+------+
    



```python
empdf.select(col("id").alias("empid"),"name","age").show()
```

    +-----+--------+---+
    |empid|    name|age|
    +-----+--------+---+
    |    1|  Manish| 26|
    |    2|  Nikita| 23|
    |    3|  Pritam| 22|
    |    4|Prantosh| 17|
    |    5|  Vikash| 31|
    |    6|   Rahul| 55|
    |    7|    Raju| 67|
    |    8| Praveen| 28|
    |    9|     Dev| 32|
    |   10|  Sherin| 16|
    |   11|    Ragu| 12|
    |   12|   Sweta| 43|
    |   13| Raushan| 48|
    |   14|  Mukesh| 36|
    |   15| Prakash| 52|
    +-----+--------+---+
    



```python
empdf.filter(col("salary")>150000).show()
empdf.where(col("salary")>150000).show()
```

    +---+--------+---+------+-------+------+
    | id|    name|age|salary|address|gender|
    +---+--------+---+------+-------+------+
    |  4|Prantosh| 17|200000|  JAPAN|     m|
    |  5|  Vikash| 31|300000|    USA|     m|
    |  6|   Rahul| 55|300000|  INDIA|     m|
    |  7|    Raju| 67|540000|    USA|     m|
    | 12|   Sweta| 43|200000|  INDIA|     f|
    | 13| Raushan| 48|650000|    USA|     m|
    | 15| Prakash| 52|750000|  INDIA|     m|
    +---+--------+---+------+-------+------+
    
    +---+--------+---+------+-------+------+
    | id|    name|age|salary|address|gender|
    +---+--------+---+------+-------+------+
    |  4|Prantosh| 17|200000|  JAPAN|     m|
    |  5|  Vikash| 31|300000|    USA|     m|
    |  6|   Rahul| 55|300000|  INDIA|     m|
    |  7|    Raju| 67|540000|    USA|     m|
    | 12|   Sweta| 43|200000|  INDIA|     f|
    | 13| Raushan| 48|650000|    USA|     m|
    | 15| Prakash| 52|750000|  INDIA|     m|
    +---+--------+---+------+-------+------+
    



```python
empdf.filter((col("salary")>150000) & (col("age") < 18)).show()
```

    +---+--------+---+------+-------+------+
    | id|    name|age|salary|address|gender|
    +---+--------+---+------+-------+------+
    |  4|Prantosh| 17|200000|  JAPAN|     m|
    +---+--------+---+------+-------+------+
    


# literal with aliasing


```python
empdf.select("*",lit("kumar").alias("lastname")).show()
```

    +---+--------+---+------+-------+------+--------+
    | id|    name|age|salary|address|gender|lastname|
    +---+--------+---+------+-------+------+--------+
    |  1|  Manish| 26| 75000|  INDIA|     m|   kumar|
    |  2|  Nikita| 23|100000|    USA|     f|   kumar|
    |  3|  Pritam| 22|150000|  INDIA|     m|   kumar|
    |  4|Prantosh| 17|200000|  JAPAN|     m|   kumar|
    |  5|  Vikash| 31|300000|    USA|     m|   kumar|
    |  6|   Rahul| 55|300000|  INDIA|     m|   kumar|
    |  7|    Raju| 67|540000|    USA|     m|   kumar|
    |  8| Praveen| 28| 70000|  JAPAN|     m|   kumar|
    |  9|     Dev| 32|150000|  JAPAN|     m|   kumar|
    | 10|  Sherin| 16| 25000| RUSSIA|     f|   kumar|
    | 11|    Ragu| 12| 35000|  INDIA|     f|   kumar|
    | 12|   Sweta| 43|200000|  INDIA|     f|   kumar|
    | 13| Raushan| 48|650000|    USA|     m|   kumar|
    | 14|  Mukesh| 36| 95000| RUSSIA|     m|   kumar|
    | 15| Prakash| 52|750000|  INDIA|     m|   kumar|
    +---+--------+---+------+-------+------+--------+
    


# withcolumn


```python
empdf.withColumn("surname",lit("chetpalli")).show()
```

    +---+--------+---+------+-------+------+---------+
    | id|    name|age|salary|address|gender|  surname|
    +---+--------+---+------+-------+------+---------+
    |  1|  Manish| 26| 75000|  INDIA|     m|chetpalli|
    |  2|  Nikita| 23|100000|    USA|     f|chetpalli|
    |  3|  Pritam| 22|150000|  INDIA|     m|chetpalli|
    |  4|Prantosh| 17|200000|  JAPAN|     m|chetpalli|
    |  5|  Vikash| 31|300000|    USA|     m|chetpalli|
    |  6|   Rahul| 55|300000|  INDIA|     m|chetpalli|
    |  7|    Raju| 67|540000|    USA|     m|chetpalli|
    |  8| Praveen| 28| 70000|  JAPAN|     m|chetpalli|
    |  9|     Dev| 32|150000|  JAPAN|     m|chetpalli|
    | 10|  Sherin| 16| 25000| RUSSIA|     f|chetpalli|
    | 11|    Ragu| 12| 35000|  INDIA|     f|chetpalli|
    | 12|   Sweta| 43|200000|  INDIA|     f|chetpalli|
    | 13| Raushan| 48|650000|    USA|     m|chetpalli|
    | 14|  Mukesh| 36| 95000| RUSSIA|     m|chetpalli|
    | 15| Prakash| 52|750000|  INDIA|     m|chetpalli|
    +---+--------+---+------+-------+------+---------+
    



```python
empdf.withColumnRenamed("id","empid").show()
```

    +-----+--------+---+------+-------+------+
    |empid|    name|age|salary|address|gender|
    +-----+--------+---+------+-------+------+
    |    1|  Manish| 26| 75000|  INDIA|     m|
    |    2|  Nikita| 23|100000|    USA|     f|
    |    3|  Pritam| 22|150000|  INDIA|     m|
    |    4|Prantosh| 17|200000|  JAPAN|     m|
    |    5|  Vikash| 31|300000|    USA|     m|
    |    6|   Rahul| 55|300000|  INDIA|     m|
    |    7|    Raju| 67|540000|    USA|     m|
    |    8| Praveen| 28| 70000|  JAPAN|     m|
    |    9|     Dev| 32|150000|  JAPAN|     m|
    |   10|  Sherin| 16| 25000| RUSSIA|     f|
    |   11|    Ragu| 12| 35000|  INDIA|     f|
    |   12|   Sweta| 43|200000|  INDIA|     f|
    |   13| Raushan| 48|650000|    USA|     m|
    |   14|  Mukesh| 36| 95000| RUSSIA|     m|
    |   15| Prakash| 52|750000|  INDIA|     m|
    +-----+--------+---+------+-------+------+
    



```python
empdf.withColumn("id",col("id").cast("string"))\
     .withColumn("salary",col("salary").cast("long"))\
.printSchema()
```

    root
     |-- id: string (nullable = true)
     |-- name: string (nullable = true)
     |-- age: integer (nullable = true)
     |-- salary: long (nullable = true)
     |-- address: string (nullable = true)
     |-- gender: string (nullable = true)
    



```python
dropdf = empdf.drop("id",col("name"))
dropdf.show()
```

    +---+------+-------+------+
    |age|salary|address|gender|
    +---+------+-------+------+
    | 26| 75000|  INDIA|     m|
    | 23|100000|    USA|     f|
    | 22|150000|  INDIA|     m|
    | 17|200000|  JAPAN|     m|
    | 31|300000|    USA|     m|
    | 55|300000|  INDIA|     m|
    | 67|540000|    USA|     m|
    | 28| 70000|  JAPAN|     m|
    | 32|150000|  JAPAN|     m|
    | 16| 25000| RUSSIA|     f|
    | 12| 35000|  INDIA|     f|
    | 43|200000|  INDIA|     f|
    | 48|650000|    USA|     m|
    | 36| 95000| RUSSIA|     m|
    | 52|750000|  INDIA|     m|
    +---+------+-------+------+
    



```python
sqldf2 = spark.sql("""
    select * from employeetable where age>18 and salary >150000
""")
sqldf2.show()
```

    +---+-------+---+------+-------+------+
    | id|   name|age|salary|address|gender|
    +---+-------+---+------+-------+------+
    |  5| Vikash| 31|300000|    USA|     m|
    |  6|  Rahul| 55|300000|  INDIA|     m|
    |  7|   Raju| 67|540000|    USA|     m|
    | 12|  Sweta| 43|200000|  INDIA|     f|
    | 13|Raushan| 48|650000|    USA|     m|
    | 15|Prakash| 52|750000|  INDIA|     m|
    +---+-------+---+------+-------+------+
    


# union vs unionall

The primary distinction between UNION and UNION ALL depends heavily on the context in which they are used: Spark DataFrames (PySpark) versus Spark SQL. This is a very common interview question.
a. In Spark DataFrames (PySpark)

• Behavior: When working with Spark DataFrames (e.g., using df.union() or df.unionAll()), UNION and UNION ALL 
behave identically. Both operations combine the records from two DataFrames without removing any duplicate rows

The operations will simply append all records from the second DataFrame below the first one, irrespective of whether those records are duplicates of existing records in the first DataFrame or duplicates within the second DataFrame


In Spark SQL (or Hive/SQL Context)

• Behavior: This is where the crucial difference between UNION and UNION ALL manifests.
    ◦ UNION: In Spark SQL, the UNION operator removes duplicate records. It first checks if a record already exists in the combined result set. If it finds an exact duplicate, it drops it, ensuring that only distinct records are returned.
    ◦ UNION ALL: In contrast, UNION ALL in Spark SQL retains all records, including duplicates. It does not perform any duplicate checking or removal.

• Explanation: This distinction is vital in SQL contexts because duplicate handling is a common requirement.


```python

data=[(10 ,'Anil',50000, 18),
(11 ,'Vikas',75000,  16),
(12 ,'Nisha',40000,  18),
(13 ,'Nidhi',60000,  17),
(14 ,'Priya',80000,  18),
(15 ,'Mohit',45000,  18),
(16 ,'Rajesh',90000, 10),
(17 ,'Raman',55000, 16),
(18 ,'Sam',65000,   17)]

schema=['id','name','salary','managerid']

data1=[(19 ,'Sohan',50000, 18),
(20 ,'Sima',75000,  17)]
```


```python
managerdf = spark.createDataFrame(data=data,schema=schema)
managerdf.show()
managerdf.count()
```

                                                                                    

    +---+------+------+---------+
    | id|  name|salary|managerid|
    +---+------+------+---------+
    | 10|  Anil| 50000|       18|
    | 11| Vikas| 75000|       16|
    | 12| Nisha| 40000|       18|
    | 13| Nidhi| 60000|       17|
    | 14| Priya| 80000|       18|
    | 15| Mohit| 45000|       18|
    | 16|Rajesh| 90000|       10|
    | 17| Raman| 55000|       16|
    | 18|   Sam| 65000|       17|
    +---+------+------+---------+
    





    9




```python
managerdfnew = spark.createDataFrame(data=data1,schema=schema)
managerdfnew.show()
managerdfnew.count()
managerdfnew.createOrReplaceTempView("managerdfnew")
```

    +---+-----+------+---------+
    | id| name|salary|managerid|
    +---+-----+------+---------+
    | 19|Sohan| 50000|       18|
    | 20| Sima| 75000|       17|
    +---+-----+------+---------+
    



```python
managerdf.union(managerdfnew).show()
managerdf.union(managerdfnew).count()
```

    +---+------+------+---------+
    | id|  name|salary|managerid|
    +---+------+------+---------+
    | 10|  Anil| 50000|       18|
    | 11| Vikas| 75000|       16|
    | 12| Nisha| 40000|       18|
    | 13| Nidhi| 60000|       17|
    | 14| Priya| 80000|       18|
    | 15| Mohit| 45000|       18|
    | 16|Rajesh| 90000|       10|
    | 17| Raman| 55000|       16|
    | 18|   Sam| 65000|       17|
    | 19| Sohan| 50000|       18|
    | 20|  Sima| 75000|       17|
    +---+------+------+---------+
    





    11




```python
managerdf.unionAll(managerdfnew).show()
managerdf.unionAll(managerdfnew).count()
```

    +---+------+------+---------+
    | id|  name|salary|managerid|
    +---+------+------+---------+
    | 10|  Anil| 50000|       18|
    | 11| Vikas| 75000|       16|
    | 12| Nisha| 40000|       18|
    | 13| Nidhi| 60000|       17|
    | 14| Priya| 80000|       18|
    | 15| Mohit| 45000|       18|
    | 16|Rajesh| 90000|       10|
    | 17| Raman| 55000|       16|
    | 18|   Sam| 65000|       17|
    | 19| Sohan| 50000|       18|
    | 20|  Sima| 75000|       17|
    +---+------+------+---------+
    





    11




```python
duplicate=[(10 ,'Anil',50000, 18),
(11 ,'Vikas',75000,  16),
(12 ,'Nisha',40000,  18),
(13 ,'Nidhi',60000,  17),
(14 ,'Priya',80000,  18),
(15 ,'Mohit',45000,  18),
(16 ,'Rajesh',90000, 10),
(17 ,'Raman',55000, 16),
(18 ,'Sam',65000,   17),
(18 ,'Sam',65000,   17)]
duplicatedf = spark.createDataFrame(data=duplicate,schema=schema)
duplicatedf.show()
duplicatedf.createOrReplaceTempView("duplicatetable")
```

    +---+------+------+---------+
    | id|  name|salary|managerid|
    +---+------+------+---------+
    | 10|  Anil| 50000|       18|
    | 11| Vikas| 75000|       16|
    | 12| Nisha| 40000|       18|
    | 13| Nidhi| 60000|       17|
    | 14| Priya| 80000|       18|
    | 15| Mohit| 45000|       18|
    | 16|Rajesh| 90000|       10|
    | 17| Raman| 55000|       16|
    | 18|   Sam| 65000|       17|
    | 18|   Sam| 65000|       17|
    +---+------+------+---------+
    



```python
duplicatedf.union(managerdf).show()
duplicatedf.count()
```

    +---+------+------+---------+
    | id|  name|salary|managerid|
    +---+------+------+---------+
    | 10|  Anil| 50000|       18|
    | 11| Vikas| 75000|       16|
    | 12| Nisha| 40000|       18|
    | 13| Nidhi| 60000|       17|
    | 14| Priya| 80000|       18|
    | 15| Mohit| 45000|       18|
    | 16|Rajesh| 90000|       10|
    | 17| Raman| 55000|       16|
    | 18|   Sam| 65000|       17|
    | 18|   Sam| 65000|       17|
    | 10|  Anil| 50000|       18|
    | 11| Vikas| 75000|       16|
    | 12| Nisha| 40000|       18|
    | 13| Nidhi| 60000|       17|
    | 14| Priya| 80000|       18|
    | 15| Mohit| 45000|       18|
    | 16|Rajesh| 90000|       10|
    | 17| Raman| 55000|       16|
    | 18|   Sam| 65000|       17|
    +---+------+------+---------+
    





    10




```python
duplicatedf.unionAll(managerdf).show()
duplicatedf.count()
```

    +---+------+------+---------+
    | id|  name|salary|managerid|
    +---+------+------+---------+
    | 10|  Anil| 50000|       18|
    | 11| Vikas| 75000|       16|
    | 12| Nisha| 40000|       18|
    | 13| Nidhi| 60000|       17|
    | 14| Priya| 80000|       18|
    | 15| Mohit| 45000|       18|
    | 16|Rajesh| 90000|       10|
    | 17| Raman| 55000|       16|
    | 18|   Sam| 65000|       17|
    | 18|   Sam| 65000|       17|
    | 10|  Anil| 50000|       18|
    | 11| Vikas| 75000|       16|
    | 12| Nisha| 40000|       18|
    | 13| Nidhi| 60000|       17|
    | 14| Priya| 80000|       18|
    | 15| Mohit| 45000|       18|
    | 16|Rajesh| 90000|       10|
    | 17| Raman| 55000|       16|
    | 18|   Sam| 65000|       17|
    +---+------+------+---------+
    





    10




```python
spark.sql("""
select * from managerdfnew 
union
select * from duplicatetable
""").show()
spark.sql("""
select * from managerdfnew 
union
select * from duplicatetable
""").count()
```

    +---+------+------+---------+
    | id|  name|salary|managerid|
    +---+------+------+---------+
    | 19| Sohan| 50000|       18|
    | 20|  Sima| 75000|       17|
    | 10|  Anil| 50000|       18|
    | 11| Vikas| 75000|       16|
    | 12| Nisha| 40000|       18|
    | 13| Nidhi| 60000|       17|
    | 15| Mohit| 45000|       18|
    | 14| Priya| 80000|       18|
    | 16|Rajesh| 90000|       10|
    | 18|   Sam| 65000|       17|
    | 17| Raman| 55000|       16|
    +---+------+------+---------+
    





    11




```python
spark.sql("""
select * from managerdfnew 
union all
select * from duplicatetable
""").show()

spark.sql("""
select * from managerdfnew 
union all
select * from duplicatetable
""").count()
```

    +---+------+------+---------+
    | id|  name|salary|managerid|
    +---+------+------+---------+
    | 19| Sohan| 50000|       18|
    | 20|  Sima| 75000|       17|
    | 10|  Anil| 50000|       18|
    | 11| Vikas| 75000|       16|
    | 12| Nisha| 40000|       18|
    | 13| Nidhi| 60000|       17|
    | 14| Priya| 80000|       18|
    | 15| Mohit| 45000|       18|
    | 16|Rajesh| 90000|       10|
    | 17| Raman| 55000|       16|
    | 18|   Sam| 65000|       17|
    | 18|   Sam| 65000|       17|
    +---+------+------+---------+
    





    12




```python
wrong_column_data1=[(19 ,50000, 18,'Sohan'),
(20 ,75000,  17,'Sima')]

wrongschema=['id','salary','managerid','name']
wrong_column_data2=[(19 ,50000, 18,'Sohan',10),
(20 ,75000,  17,'Sima',20)]
wrongschema2=['id','salary','managerid','name','bonus']
wrong1 = spark.createDataFrame(data=wrong_column_data1,schema=wrongschema)
wrong2 = spark.createDataFrame(data=wrong_column_data2,schema=wrongschema2)
wrong1.show()
wrong2.show()
```

    +---+------+---------+-----+
    | id|salary|managerid| name|
    +---+------+---------+-----+
    | 19| 50000|       18|Sohan|
    | 20| 75000|       17| Sima|
    +---+------+---------+-----+
    
    +---+------+---------+-----+-----+
    | id|salary|managerid| name|bonus|
    +---+------+---------+-----+-----+
    | 19| 50000|       18|Sohan|   10|
    | 20| 75000|       17| Sima|   20|
    +---+------+---------+-----+-----+
    



```python
managerdf.union(wrong1).show()
managerdf.union(wrong1).count()
```

    +---+------+------+---------+
    | id|  name|salary|managerid|
    +---+------+------+---------+
    | 10|  Anil| 50000|       18|
    | 11| Vikas| 75000|       16|
    | 12| Nisha| 40000|       18|
    | 13| Nidhi| 60000|       17|
    | 14| Priya| 80000|       18|
    | 15| Mohit| 45000|       18|
    | 16|Rajesh| 90000|       10|
    | 17| Raman| 55000|       16|
    | 18|   Sam| 65000|       17|
    | 19| 50000|    18|    Sohan|
    | 20| 75000|    17|     Sima|
    +---+------+------+---------+
    





    11




```python
managerdf.unionByName(wrong1).show()
managerdf.unionByName(wrong1).count()
```

    +---+------+------+---------+
    | id|  name|salary|managerid|
    +---+------+------+---------+
    | 10|  Anil| 50000|       18|
    | 11| Vikas| 75000|       16|
    | 12| Nisha| 40000|       18|
    | 13| Nidhi| 60000|       17|
    | 14| Priya| 80000|       18|
    | 15| Mohit| 45000|       18|
    | 16|Rajesh| 90000|       10|
    | 17| Raman| 55000|       16|
    | 18|   Sam| 65000|       17|
    | 19| Sohan| 50000|       18|
    | 20|  Sima| 75000|       17|
    +---+------+------+---------+
    





    11




```python
wrong2.select('id','salary','managerid','name').union(managerdf).show()
```

    +---+------+---------+-----+
    | id|salary|managerid| name|
    +---+------+---------+-----+
    | 19| 50000|       18|Sohan|
    | 20| 75000|       17| Sima|
    | 10|  Anil|    50000|   18|
    | 11| Vikas|    75000|   16|
    | 12| Nisha|    40000|   18|
    | 13| Nidhi|    60000|   17|
    | 14| Priya|    80000|   18|
    | 15| Mohit|    45000|   18|
    | 16|Rajesh|    90000|   10|
    | 17| Raman|    55000|   16|
    | 18|   Sam|    65000|   17|
    +---+------+---------+-----+
    


# Repartition


```python
#Read dataframe with header false
flight_df = spark.read.format("csv") \
                .option("header", "true") \
                .option("inferschema","true")\
                .load("/sandbox/DataEngineering/manish/pyspark/flightdata.csv") 

flight_df.show()
```

    +--------------------+-------------------+-----+
    |   DEST_COUNTRY_NAME|ORIGIN_COUNTRY_NAME|count|
    +--------------------+-------------------+-----+
    |       United States|            Romania|    1|
    |       United States|            Ireland|  264|
    |       United States|              India|   69|
    |               Egypt|      United States|   24|
    |   Equatorial Guinea|      United States|    1|
    |       United States|          Singapore|   25|
    |       United States|            Grenada|   54|
    |          Costa Rica|      United States|  477|
    |             Senegal|      United States|   29|
    |       United States|   Marshall Islands|   44|
    |              Guyana|      United States|   17|
    |       United States|       Sint Maarten|   53|
    |               Malta|      United States|    1|
    |             Bolivia|      United States|   46|
    |            Anguilla|      United States|   21|
    |Turks and Caicos ...|      United States|  136|
    |       United States|        Afghanistan|    2|
    |Saint Vincent and...|      United States|    1|
    |               Italy|      United States|  390|
    |       United States|             Russia|  156|
    +--------------------+-------------------+-----+
    only showing top 20 rows
    



```python
flight_df.count()
```




    255




```python
flight_df.rdd.getNumPartitions()
```




    1




```python
patitionflightdf = flight_df.repartition(4)
```


```python
patitionflightdf.withColumn("partitionId",spark_partition_id()).groupBy("partitionId").count().show()
```

    [Stage 125:>                                                        (0 + 1) / 1]

    +-----------+-----+
    |partitionId|count|
    +-----------+-----+
    |          0|   63|
    |          1|   64|
    |          2|   64|
    |          3|   64|
    +-----------+-----+
    


                                                                                    


```python
paritiononcolumn =  flight_df.repartition(300,"ORIGIN_COUNTRY_NAME")
```


```python
paritiononcolumn.rdd.getNumPartitions()
```




    300




```python
paritiononcolumn.withColumn("partitionId",spark_partition_id()).groupBy("partitionId").count().show()
```

    [Stage 134:=========================================>           (237 + 4) / 300]

    +-----------+-----+
    |partitionId|count|
    +-----------+-----+
    |          0|    1|
    |          2|    1|
    |          7|    1|
    |         10|    1|
    |         13|    1|
    |         15|    2|
    |         16|    2|
    |         19|    1|
    |         21|    1|
    |         22|    1|
    |         28|    1|
    |         31|    1|
    |         39|    1|
    |         42|    1|
    |         43|    1|
    |         44|    1|
    |         45|    2|
    |         48|    1|
    |         53|    1|
    |         54|    1|
    +-----------+-----+
    only showing top 20 rows
    


                                                                                    


```python
paritiononcolumn.show()
```

    +-----------------+--------------------+-----+
    |DEST_COUNTRY_NAME| ORIGIN_COUNTRY_NAME|count|
    +-----------------+--------------------+-----+
    |    United States|          Cape Verde|   18|
    |    United States|            Anguilla|   20|
    |    United States|Saint Kitts and N...|  127|
    |    United States|    French Polynesia|   38|
    |    United States|              Cyprus|    1|
    |    United States|           Singapore|   25|
    |    United States|Bonaire, Sint Eus...|   16|
    |    United States|              Mexico| 6220|
    |    United States|                Fiji|   51|
    |    United States|             Estonia|    1|
    |    United States|Saint Vincent and...|   16|
    |    United States|             Germany| 1406|
    |    United States|Federated States ...|   48|
    |    United States|            Honduras|  393|
    |    United States|         Switzerland|  334|
    |    United States|            Slovakia|    1|
    |    United States|             Jamaica|  757|
    |    United States|United Arab Emirates|  156|
    |    United States|              Angola|   18|
    |    United States|         Saint Lucia|  121|
    +-----------------+--------------------+-----+
    only showing top 20 rows
    


# Coalesce


```python
coalescedf = flight_df.repartition(8)
```


```python
threecoalescedf = coalescedf.coalesce(3)
```


```python
threecoalescedf.withColumn("partitionId",spark_partition_id()).groupBy("partitionId").count().show()
```

    +-----------+-----+
    |partitionId|count|
    +-----------+-----+
    |          0|   64|
    |          1|   95|
    |          2|   96|
    +-----------+-----+
    



```python
coalescedf2 = flight_df.repartition(3)
```


```python
coalescedf2.withColumn("partitionId",spark_partition_id()).groupBy("partitionId").count().show()
```

    +-----------+-----+
    |partitionId|count|
    +-----------+-----+
    |          0|   85|
    |          1|   85|
    |          2|   85|
    +-----------+-----+
    



```python
coalescedf.coalesce(10).rdd.getNumPartitions()
```




    8



# case when & when otherwise


```python
empdf = spark.read.format("csv") \
                .option("header", "true") \
                .option("inferschema","true")\
                .load("/sandbox/DataEngineering/manish/pyspark/part.csv") 

empdf.show()
empdf.printSchema()
empdf.columns
```

    +---+--------+---+------+-------+------+
    | id|    name|age|salary|address|gender|
    +---+--------+---+------+-------+------+
    |  1|  Manish| 26| 75000|  INDIA|     m|
    |  2|  Nikita| 23|100000|    USA|     f|
    |  3|  Pritam| 22|150000|  INDIA|     m|
    |  4|Prantosh| 17|200000|  JAPAN|     m|
    |  5|  Vikash| 31|300000|    USA|     m|
    |  6|   Rahul| 55|300000|  INDIA|     m|
    |  7|    Raju| 67|540000|    USA|     m|
    |  8| Praveen| 28| 70000|  JAPAN|     m|
    |  9|     Dev| 32|150000|  JAPAN|     m|
    | 10|  Sherin| 16| 25000| RUSSIA|     f|
    | 11|    Ragu| 12| 35000|  INDIA|     f|
    | 12|   Sweta| 43|200000|  INDIA|     f|
    | 13| Raushan| 48|650000|    USA|     m|
    | 14|  Mukesh| 36| 95000| RUSSIA|     m|
    | 15| Prakash| 52|750000|  INDIA|     m|
    +---+--------+---+------+-------+------+
    
    root
     |-- id: integer (nullable = true)
     |-- name: string (nullable = true)
     |-- age: integer (nullable = true)
     |-- salary: integer (nullable = true)
     |-- address: string (nullable = true)
     |-- gender: string (nullable = true)
    





    ['id', 'name', 'age', 'salary', 'address', 'gender']




```python
empdf.withColumn("adult", when(col("age") < 18,"no")\
                          .when(col("age") > 18,"yes")\
                         .otherwise("novalue")).show()
```

    +---+--------+---+------+-------+------+-----+
    | id|    name|age|salary|address|gender|adult|
    +---+--------+---+------+-------+------+-----+
    |  1|  Manish| 26| 75000|  INDIA|     m|  yes|
    |  2|  Nikita| 23|100000|    USA|     f|  yes|
    |  3|  Pritam| 22|150000|  INDIA|     m|  yes|
    |  4|Prantosh| 17|200000|  JAPAN|     m|   no|
    |  5|  Vikash| 31|300000|    USA|     m|  yes|
    |  6|   Rahul| 55|300000|  INDIA|     m|  yes|
    |  7|    Raju| 67|540000|    USA|     m|  yes|
    |  8| Praveen| 28| 70000|  JAPAN|     m|  yes|
    |  9|     Dev| 32|150000|  JAPAN|     m|  yes|
    | 10|  Sherin| 16| 25000| RUSSIA|     f|   no|
    | 11|    Ragu| 12| 35000|  INDIA|     f|   no|
    | 12|   Sweta| 43|200000|  INDIA|     f|  yes|
    | 13| Raushan| 48|650000|    USA|     m|  yes|
    | 14|  Mukesh| 36| 95000| RUSSIA|     m|  yes|
    | 15| Prakash| 52|750000|  INDIA|     m|  yes|
    +---+--------+---+------+-------+------+-----+
    



```python
empdf2 = empdf.withColumn("age", when(col("age").isNull(),lit(19))
              .otherwise(col("age")))\
              .withColumn("adult", when(col("age") > 18,"yes")\
              .otherwise("no")).show()
```

    +---+--------+---+------+-------+------+-----+
    | id|    name|age|salary|address|gender|adult|
    +---+--------+---+------+-------+------+-----+
    |  1|  Manish| 26| 75000|  INDIA|     m|  yes|
    |  2|  Nikita| 23|100000|    USA|     f|  yes|
    |  3|  Pritam| 22|150000|  INDIA|     m|  yes|
    |  4|Prantosh| 17|200000|  JAPAN|     m|   no|
    |  5|  Vikash| 31|300000|    USA|     m|  yes|
    |  6|   Rahul| 55|300000|  INDIA|     m|  yes|
    |  7|    Raju| 67|540000|    USA|     m|  yes|
    |  8| Praveen| 28| 70000|  JAPAN|     m|  yes|
    |  9|     Dev| 32|150000|  JAPAN|     m|  yes|
    | 10|  Sherin| 16| 25000| RUSSIA|     f|   no|
    | 11|    Ragu| 12| 35000|  INDIA|     f|   no|
    | 12|   Sweta| 43|200000|  INDIA|     f|  yes|
    | 13| Raushan| 48|650000|    USA|     m|  yes|
    | 14|  Mukesh| 36| 95000| RUSSIA|     m|  yes|
    | 15| Prakash| 52|750000|  INDIA|     m|  yes|
    +---+--------+---+------+-------+------+-----+
    



```python
empdf3 = empdf.withColumn("agewise",when((col("age")>0) & (col("age")<18),"minor")\
                                    .when((col("age")>18) & (col("age")<30),"mid")\
                                    .otherwise("major")).show()
```

    +---+--------+---+------+-------+------+-------+
    | id|    name|age|salary|address|gender|agewise|
    +---+--------+---+------+-------+------+-------+
    |  1|  Manish| 26| 75000|  INDIA|     m|    mid|
    |  2|  Nikita| 23|100000|    USA|     f|    mid|
    |  3|  Pritam| 22|150000|  INDIA|     m|    mid|
    |  4|Prantosh| 17|200000|  JAPAN|     m|  minor|
    |  5|  Vikash| 31|300000|    USA|     m|  major|
    |  6|   Rahul| 55|300000|  INDIA|     m|  major|
    |  7|    Raju| 67|540000|    USA|     m|  major|
    |  8| Praveen| 28| 70000|  JAPAN|     m|    mid|
    |  9|     Dev| 32|150000|  JAPAN|     m|  major|
    | 10|  Sherin| 16| 25000| RUSSIA|     f|  minor|
    | 11|    Ragu| 12| 35000|  INDIA|     f|  minor|
    | 12|   Sweta| 43|200000|  INDIA|     f|  major|
    | 13| Raushan| 48|650000|    USA|     m|  major|
    | 14|  Mukesh| 36| 95000| RUSSIA|     m|  major|
    | 15| Prakash| 52|750000|  INDIA|     m|  major|
    +---+--------+---+------+-------+------+-------+
    



```python
spark.sql("""
select *,
       case when age < 18 then 'Minor'
            when age > 18 then 'Mid'
            else 'Major'
        end as Adult
from 
    employeetable
""").show()
```

    +---+--------+---+------+-------+------+-----+
    | id|    name|age|salary|address|gender|Adult|
    +---+--------+---+------+-------+------+-----+
    |  1|  Manish| 26| 75000|  INDIA|     m|  Mid|
    |  2|  Nikita| 23|100000|    USA|     f|  Mid|
    |  3|  Pritam| 22|150000|  INDIA|     m|  Mid|
    |  4|Prantosh| 17|200000|  JAPAN|     m|Minor|
    |  5|  Vikash| 31|300000|    USA|     m|  Mid|
    |  6|   Rahul| 55|300000|  INDIA|     m|  Mid|
    |  7|    Raju| 67|540000|    USA|     m|  Mid|
    |  8| Praveen| 28| 70000|  JAPAN|     m|  Mid|
    |  9|     Dev| 32|150000|  JAPAN|     m|  Mid|
    | 10|  Sherin| 16| 25000| RUSSIA|     f|Minor|
    | 11|    Ragu| 12| 35000|  INDIA|     f|Minor|
    | 12|   Sweta| 43|200000|  INDIA|     f|  Mid|
    | 13| Raushan| 48|650000|    USA|     m|  Mid|
    | 14|  Mukesh| 36| 95000| RUSSIA|     m|  Mid|
    | 15| Prakash| 52|750000|  INDIA|     m|  Mid|
    +---+--------+---+------+-------+------+-----+
    



```python

```
