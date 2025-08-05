#!/usr/bin/env python
# coding: utf-8

# # Import all the functions

# In[1]:


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


# In[2]:


# --------------------------------------------------------------------------------------------------------------------------
# Setting Up the Configurations for pySpark
# --------------------------------------------------------------------------------------------------------------------------
conf = (pyspark.SparkConf().set('spark.driver.memory', '10G')        .set('spark.executor.memory', '10G')        .set('spark.driver.maxResultSize', '10G')        .set('spark.dynamicAllocation.enabled', 'false')        .set('spark.dynamicAllocaton.maxExecutors', '4')        .set('spark.master','local[4]')        .set('spark.driver.extraClassPath', '/data2/pythonuser/ngdbc-2.3.48.jar'))

# --------------------------------------------------------------------------------------------------------------------------
# Fetching or Creating a Session for this Activity
# --------------------------------------------------------------------------------------------------------------------------
spark = SparkSession.builder.config(conf = conf).appName("pyspark2").enableHiveSupport().getOrCreate()

spark


# # spark read modes
# When reading data (e.g., from CSV, JSON, etc.) in Apache Spark using DataFrameReader, you can specify how Spark should handle malformed or corrupted records using the mode option. Below are the available modes:
# 
# | Mode           | Description                                                                 |
# |----------------|-----------------------------------------------------------------------------|
# | failFast   | Terminates the query immediately if any malformed record is encountered. This is useful when data integrity is critical. |
# | dropMalformed | Drops all rows containing malformed records. This can be useful when you prefer to skip bad data instead of failing the entire job. |
# | permissive (default) | Tries to parse all records. If a record is corrupted or missing fields, Spark sets `null` values for corrupted fields and puts malformed data into a special column named `_corrupt_record`. |

# In[3]:


#Read dataframe with header false
flight_df = spark.read.format("csv")                 .option("header", "false")                 .option("inferschema","false")                .option("mode","FAILFAST")                .load("/sandbox/DataEngineering/manish/pyspark/flightdata.csv") 

flight_df.show()


# In[4]:


#Read dataframe with header true
flight_df2 = spark.read.format("csv")                 .option("header", "true")                 .option("inferschema","false")                .option("mode","FAILFAST")                .load("/sandbox/DataEngineering/manish/pyspark/flightdata.csv") 

flight_df2.show()


# In[5]:


flight_df2.printSchema()


# In[6]:


#Read dataframe with inferschema true
flight_df3 = spark.read.format("csv")                 .option("header", "true")                 .option("inferschema","true")                .option("mode","FAILFAST")                .load("/sandbox/DataEngineering/manish/pyspark/flightdata.csv") 

flight_df3.printSchema()


# # schema in spark
# There are two primary methods: using **StructType** and **StructField** classes, and using a DDL (Data Definition Language) string.
# 
# These are classes in Spark used to define the schema structure.
# 
# **StructField** represents a single column within a DataFrame. It holds information such as the column's name, its data type (e.g., String, Integer, Timestamp), and whether it can contain null values (nullable: True/False). If nullable is set to False, the column cannot contain NULL values, and an error will be thrown if it does.
# 
# **StructType** defines the overall structure of a DataFrame. It is essentially a list or collection of StructField objects. When you combine ID, Name, and Age fields, for example, they define the structure of a record, and a collection of such records forms a DataFrame.
# 
# What happens if you set header=False when your data actually has a header? If you disable the header option (header=False) but your CSV file contains a header row, Spark will treat that header row as regular data. If this header row's values do not match the data types defined in your manual schema (e.g., a string "Count" being read into an Integer column), it can lead to null values in that column if the read mode is set to permissive, or an error if the mode is failfast

# In[7]:


# Define the schema using StructType and StructField
my_schema = StructType([
    StructField("DEST_COUNTRY_NAME", StringType(), True),  
    StructField("ORIGIN_COUNTRY_NAME", StringType(), True),  
    StructField("count", IntegerType(), True)  
])
my_schema


# In[8]:


#Read dataframe with inferschema true
flight_df4 = spark.read.format("csv")                 .option("header", "true")                 .option("inferschema","false")                .option("skipRows",1)                .schema(my_schema)                .option("mode","PERMISSIVE")                .load("/sandbox/DataEngineering/manish/pyspark/flightdata.csv") 

flight_df4.printSchema()


# # handling corrupted records
# When reading data, Spark offers different modes to handle corrupted records, which influence how the DataFrame is populated.
# 
# In **permissive mode**, all records are allowed to enter the DataFrame. If a record is corrupted, Spark sets the malformed values to null and does not throw an error. For the example data with five total records (two corrupted), permissive mode will result in five records in the DataFrame, with nulls where data is bad.
# 
# In **dropMalformed mode**, Spark discards any record it identifies as corrupted. Given the example data has two corrupted records out of five, this mode will produce a DataFrame with three records
# 
# In **failfast mode**, Spark immediately throws an error and stops the job as soon as it encounters the first corrupted record. This mode will result in zero records in the DataFrame because the job will fail.

# In[9]:


employee = spark.read.format("csv")                 .option("header", "true")                 .option("inferschema","true")                .option("mode","PERMISSIVE")                .load("/sandbox/DataEngineering/manish/pyspark/employee.csv") 

employee.show()


# In[10]:


employee1 = spark.read.format("csv")                 .option("header", "true")                 .option("inferschema","true")                .option("mode","dropmalformed")                .load("/sandbox/DataEngineering/manish/pyspark/employee.csv") 

employee1.show()


# In[ ]:





# # print bad records
# To specifically identify and view the corrupted records, you need to define a manual schema that includes a special column named _corrupt_record. This column will capture the raw content of the corrupted record.
# 
# Where to store bad record For scenarios with a large volume of corrupted records (e.g., thousands), printing them is not practical. Spark provides the badRecordsPath option to store all corrupted records in a specified location. These records are saved in JSON format at the designated path
# 
# 

# In[11]:


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


# In[12]:


employee3 = spark.read.format("csv")                 .option("header", "true")                 .option("inferschema","true")                .option("mode","PERMISSIVE")                .schema(empschema)                .load("/sandbox/DataEngineering/manish/pyspark/employee.csv") 

employee3.show()
employee3.show(truncate=False)


# In[13]:


employee3 = spark.read.format("csv")                 .option("header", "true")                 .option("inferschema","true")                .option("mode","PERMISSIVE")                .schema(empschema)                .option("badRecordsPath","/sandbox/DataEngineering/manish/pyspark/badrecords")                .load("/sandbox/DataEngineering/manish/pyspark/employee.csv") 

employee3.show()
employee3.show(truncate=False)


# # read json in spark

# In[14]:


json = spark.read.format("json")                 .option("inferschema","true")                .option("mode","PERMISSIVE")                .load("/sandbox/DataEngineering/manish/pyspark/line_delimeted.json").show()


# In[15]:


json2 = spark.read.format("json")                 .option("inferschema","true")                .option("mode","PERMISSIVE")                .load("/sandbox/DataEngineering/manish/pyspark/single_file.json").show()


# In[16]:


json3 = spark.read.format("json")                 .option("inferschema","true")                .option("mode","PERMISSIVE")                .option("multiline","True")                .load("/sandbox/DataEngineering/manish/pyspark/multiline.json").show()

json4 = spark.read.format("json")                 .option("inferschema","true")                .option("mode","PERMISSIVE")                .option("multiline","True")                .load("/sandbox/DataEngineering/manish/pyspark/corrupted_json").show()


# # write dataframe
# When working with Spark, after you have read data into a DataFrame and performed transformations, it is crucial to write the processed data back to disk to ensure its persistence. Currently, all the transformations and data processing occur in memory, so writing to disk makes the data permanent.
# Here's a detailed explanation with code examples and notes based on the provided sources:
# 
# !!! Code
# 
#         # Assuming 'df' is your DataFrame
#         # Define your base location where you want to save the output
#         base_location = "/user/hive/warehouse/your_database/output/"
# 
#         # Construct the full path for the CSV output folder
#         output_path = base_location + "csv_write/"
# 
#         # Write the DataFrame to disk
#         df.write \
#             .format("csv") \
#             .option("header", "true") \
#             .mode("overwrite") \
#             .save(output_path)
# 
# **General Structure for Writing a DataFrame to Disk**
# 
# The general structure for writing a DataFrame using the Spark DataFrame Writer API is as follows:
# 
# DataFrame.write: This is the starting point, indicating that you intend to write a DataFrame.
# 
#    .format(): Specifies the file format in which you want to save the data. Common formats include CSV or Parquet. If no format is explicitly passed, Spark will default to Parquet.
#    
#    .option(): Allows you to pass multiple options. For example, you can specify whether to include a header for CSV files (e.g., header as True). You can also specify the output path using path option, though save() method usually handles the path directly.
# 
#    .mode(): Defines how Spark should behave if files or directories already exist at the target location. This is a very important aspect of writing data.
#    
#    .partitionBy(): (To be covered in a dedicated video mentioned in the source) This method allows you to partition the output data based on one or more columns, creating separate folders for each partition.
# 
#    .bucketBy(): (To be covered in a dedicated video mentioned in the source) Similar to partitionBy, but it organizes data into a fixed number of buckets within partitions.
# 
#    .save(): This is the final action that triggers the write operation and specifies the output path where the DataFrame will be written.
# 
# A typical flow looks like: **df.write.format(...).option(...).mode(...).save(path)**.
# 
# **Modes in DataFrame Writer API**
# 
# The mode() method in the DataFrame Writer API is crucial as it dictates how Spark handles existing data at the target location. There are four primary modes:
# 
# **append**
#  
#  Functionality: If files already exist at the specified location, the new data from the DataFrame will be added to the existing files.
# 
#  Example: If there were three files previously, and a new output DataFrame comes, it will simply append its data to that list of files.
# 
# **overwrite**
# 
#  Functionality: This mode deletes any existing files at the target location before writing the new DataFrame.
# 
#  Example: If a previous file had records, overwrite will delete all old files and only the new file with its records (e.g., five new records) will be visible.
# 
# **errorIfExists**
# 
#  Functionality: Spark will check if a file or location already exists at the target path. If it does, the write operation will fail and throw an error.
# 
#  Use Case: Useful when you want to ensure that you do not accidentally overwrite or append to existing data.
# 
# **ignore**
# 
#  Functionality: If a file or location already exists at the target path, Spark will skip the write operation entirely without throwing an error. The new file will not be written.
# 
#  Use Case: This mode is suitable if you want to prevent new data from being written if data is already present, perhaps to avoid overwriting changes or to ensure data integrity
# 
# 
# 

# df.write \
#     .format("csv") \
#     .option("header", "true") \
#     .option("mode", "overwrite") \
#     .option("path", "/sandbox/DataEngineering/manish/pyspark") \
#     .save()

# # paritition in spark

# 

# In[17]:


df = spark.read.format("csv")                 .option("header", "true")                 .option("inferschema","true")                .option("mode","PERMISSIVE")                .load("/sandbox/DataEngineering/manish/pyspark/part.csv") 

df.show()


# df.write \
#     .format("csv") \
#     .option("header", "true") \
#     .option("mode", "overwrite") \
#     .option("path", "/sandbox/DataEngineering/manish/pyspark/partbyid/") \
#     .partitionBy("address")\
#     .save()

# df.write \
#     .format("csv") \
#     .option("header", "true") \
#     .option("mode", "overwrite") \
#     .option("path", "/sandbox/DataEngineering/manish/pyspark/partition/") \
#     .partitionBy("address","gender")\
#     .save()

# # bucketing in pyspark
# save doesnt work, need to use saveAsTable

# df.write \
#     .format("csv") \
#     .option("header", "true") \
#     .option("mode", "overwrite") \
#     .option("path", "/sandbox/DataEngineering/manish/pyspark/bucket/") \
#     .bucketBy(3,"id")\
#     .saveAsTable("bucketbyid")

# # column selection and expression 

# In[18]:


empdf = spark.read.format("csv")                 .option("header", "true")                 .option("inferschema","true")                .option("mode","PERMISSIVE")                .load("/sandbox/DataEngineering/manish/pyspark/part.csv") 

empdf.show()
empdf.printSchema()
empdf.columns


# In[19]:


empdf.select('age').show()


# In[20]:


empdf.select(col("name")).show()


# In[21]:


empdf.select(col("id")+5).show()


# In[22]:


empdf.select("id","name","age").show()


# In[23]:


empdf.select(col("id"),col("name")).show()


# In[24]:


empdf.select("id",col("name"),empdf['salary'],empdf.address).show()


# In[25]:


empdf.select(expr("id +5")).show()


# In[26]:


empdf.select(expr("id as emp_id"),expr("name as emp_name"), expr("concat(emp_id, ' ', emp_name)")).show()


# # spark SQL

# In[27]:


empdf.createOrReplaceTempView('employeetable')


# In[28]:


sqldf = spark.sql(""" select * from employeetable """)
sqldf.show()


# In[29]:


sqldf.select('*').show()


# In[30]:


empdf.select(col("id").alias("empid"),"name","age").show()


# In[31]:


empdf.filter(col("salary")>150000).show()
empdf.where(col("salary")>150000).show()


# In[32]:


empdf.filter((col("salary")>150000) & (col("age") < 18)).show()


# # literal with aliasing

# In[33]:


empdf.select("*",lit("kumar").alias("lastname")).show()


# # withcolumn

# In[34]:


empdf.withColumn("surname",lit("chetpalli")).show()


# In[35]:


empdf.withColumnRenamed("id","empid").show()


# In[36]:


empdf.withColumn("id",col("id").cast("string"))     .withColumn("salary",col("salary").cast("long")).printSchema()


# In[37]:


dropdf = empdf.drop("id",col("name"))
dropdf.show()


# In[38]:


sqldf2 = spark.sql("""
    select * from employeetable where age>18 and salary >150000
""")
sqldf2.show()


# # union vs unionall
# 
# The primary distinction between UNION and UNION ALL depends heavily on the context in which they are used: Spark DataFrames (PySpark) versus Spark SQL. This is a very common interview question.
# a. In Spark DataFrames (PySpark)
# 
# • Behavior: When working with Spark DataFrames (e.g., using df.union() or df.unionAll()), UNION and UNION ALL 
# behave identically. Both operations combine the records from two DataFrames without removing any duplicate rows
# 
# The operations will simply append all records from the second DataFrame below the first one, irrespective of whether those records are duplicates of existing records in the first DataFrame or duplicates within the second DataFrame
# 
# 
# In Spark SQL (or Hive/SQL Context)
# 
# • Behavior: This is where the crucial difference between UNION and UNION ALL manifests.
#     ◦ UNION: In Spark SQL, the UNION operator removes duplicate records. It first checks if a record already exists in the combined result set. If it finds an exact duplicate, it drops it, ensuring that only distinct records are returned.
#     ◦ UNION ALL: In contrast, UNION ALL in Spark SQL retains all records, including duplicates. It does not perform any duplicate checking or removal.
# 
# • Explanation: This distinction is vital in SQL contexts because duplicate handling is a common requirement.

# In[39]:



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


# In[40]:


managerdf = spark.createDataFrame(data=data,schema=schema)
managerdf.show()
managerdf.count()


# In[41]:


managerdfnew = spark.createDataFrame(data=data1,schema=schema)
managerdfnew.show()
managerdfnew.count()
managerdfnew.createOrReplaceTempView("managerdfnew")


# In[42]:


managerdf.union(managerdfnew).show()
managerdf.union(managerdfnew).count()


# In[43]:


managerdf.unionAll(managerdfnew).show()
managerdf.unionAll(managerdfnew).count()


# In[44]:


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


# In[45]:


duplicatedf.union(managerdf).show()
duplicatedf.count()


# In[46]:


duplicatedf.unionAll(managerdf).show()
duplicatedf.count()


# In[47]:


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


# In[48]:


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


# In[49]:


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


# In[50]:


managerdf.union(wrong1).show()
managerdf.union(wrong1).count()


# In[51]:


managerdf.unionByName(wrong1).show()
managerdf.unionByName(wrong1).count()


# In[52]:


wrong2.select('id','salary','managerid','name').union(managerdf).show()


# # Repartition

# In[53]:


#Read dataframe with header false
flight_df = spark.read.format("csv")                 .option("header", "true")                 .option("inferschema","true")                .load("/sandbox/DataEngineering/manish/pyspark/flightdata.csv") 

flight_df.show()


# In[54]:


flight_df.count()


# In[55]:


flight_df.rdd.getNumPartitions()


# In[56]:


patitionflightdf = flight_df.repartition(4)


# In[57]:


patitionflightdf.withColumn("partitionId",spark_partition_id()).groupBy("partitionId").count().show()


# In[58]:


paritiononcolumn =  flight_df.repartition(300,"ORIGIN_COUNTRY_NAME")


# In[59]:


paritiononcolumn.rdd.getNumPartitions()


# In[60]:


paritiononcolumn.withColumn("partitionId",spark_partition_id()).groupBy("partitionId").count().show()


# In[61]:


paritiononcolumn.show()


# # Coalesce

# In[62]:


coalescedf = flight_df.repartition(8)


# In[63]:


threecoalescedf = coalescedf.coalesce(3)


# In[64]:


threecoalescedf.withColumn("partitionId",spark_partition_id()).groupBy("partitionId").count().show()


# In[65]:


coalescedf2 = flight_df.repartition(3)


# In[66]:


coalescedf2.withColumn("partitionId",spark_partition_id()).groupBy("partitionId").count().show()


# In[67]:


coalescedf.coalesce(10).rdd.getNumPartitions()


# # case when & when otherwise

# In[68]:


empdf = spark.read.format("csv")                 .option("header", "true")                 .option("inferschema","true")                .load("/sandbox/DataEngineering/manish/pyspark/part.csv") 

empdf.show()
empdf.printSchema()
empdf.columns


# In[69]:


empdf.withColumn("adult", when(col("age") < 18,"no")                          .when(col("age") > 18,"yes")                         .otherwise("novalue")).show()


# In[70]:


empdf2 = empdf.withColumn("age", when(col("age").isNull(),lit(19))
              .otherwise(col("age")))\
              .withColumn("adult", when(col("age") > 18,"yes")\
              .otherwise("no")).show()


# In[71]:


empdf3 = empdf.withColumn("agewise",when((col("age")>0) & (col("age")<18),"minor")                                    .when((col("age")>18) & (col("age")<30),"mid")                                    .otherwise("major")).show()


# In[72]:


spark.sql("""
select *,
       case when age < 18 then 'Minor'
            when age > 18 then 'Mid'
            else 'Major'
        end as Adult
from 
    employeetable
""").show()


# In[ ]:




