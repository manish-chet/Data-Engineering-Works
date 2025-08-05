### **Spark Data Read Modes**

When reading data (e.g., from CSV, JSON, etc.) in Apache Spark using `DataFrameReader`, you can specify how Spark should handle malformed or corrupted records using the `mode` option. Below are the available modes:

| Mode           | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| failFast   | Terminates the query immediately if any malformed record is encountered. This is useful when data integrity is critical. |
| dropMalformed | Drops all rows containing malformed records. This can be useful when you prefer to skip bad data instead of failing the entire job. |
| permissive (default) | Tries to parse all records. If a record is corrupted or missing fields, Spark sets `null` values for corrupted fields and puts malformed data into a special column named `_corrupt_record`. |


### **Schema in spark**

There are two primary methods: using `StructType` and `StructField` classes, and using a DDL (Data Definition Language) string.


These are classes in Spark used to define the schema structure.

`StructField` represents a single column within a DataFrame. It holds information such as the column's name, its data type (e.g., String, Integer, Timestamp), and whether it can contain null values (nullable: True/False). If `nullable` is set to `False`, the column cannot contain `NULL` values, and an error will be thrown if it does.
    
`StructType` defines the overall structure of a DataFrame. It is essentially a list or collection of `StructField` objects. When you combine `ID`, `Name`, and `Age` fields, for example, they define the structure of a record, and a collection of such records forms a DataFrame.

What happens if you set `header=False` when your data actually has a header? 
 If you disable the header option (`header=False`) but your CSV file contains a header row, Spark will treat that header row as regular data. If this header row's values do not match the data types defined in your manual schema (e.g., a string "Count" being read into an `Integer` column), it can lead to `null` values in that column if the read `mode` is set to `permissive`, or an error if the `mode` is `failfast`.

**Method 1: Creating Schema using `StructType` and `StructField`**

This method involves importing specific classes from `pyspark.sql.types` to programmatically define the schema.

Required Imports:
To use `StructType` and `StructField`, along with specific data types like `StringType` and `IntegerType`, you must import them:

!!! Code

        from pyspark.sql.types import StructType, StructField, StringType, IntegerType #


Conceptual Data (for explanation):

| ID | Name | Age |
|----|------|-----|
| 1  | Manish | 30  |
| 2  | John | 25  |

Code Example for `ID`, `Name`, `Age` Schema:
!!! Code

        # Define the schema using StructType and StructField
        my_schema = StructType([
            StructField("ID", IntegerType(), True),  # ID column, Integer type, nullable is True
            StructField("Name", StringType(), True),  # Name column, String type, nullable is True
            StructField("Age", IntegerType(), True)   # Age column, Integer type, nullable is True
        ])

 Each `StructField` defines a column: its name (string), its data type (e.g., `IntegerType()`), and whether it's nullable (Boolean `True` or `False`). Setting `nullable` to `False` means the column cannot be null, otherwise an error will be thrown.
 
 The `StructType` constructor takes a list of `StructField` objects.

**Method 2: Creating Schema using DDL String**

This method is simpler and involves passing a string that defines the column names and their data types, similar to SQL's Data Definition Language.

Code Example for `ID`, `Name`, `Age` Schema (DDL String):
!!! Code

        # Define the schema using a DDL string
        ddl_my_schema = "ID INT, Name STRING, Age INT" #

   The string specifies column names and their corresponding Spark SQL data types (e.g., `INT` for Integer, `STRING` for String) separated by commas.

**Applying the Schema to Read Data**


Actual Data Example (from a CSV file):
The example uses a CSV file containing flight data with columns `Destination Country`, `Origin Country`, and `Count`.

Code Example for Reading Data with Manual Schema:
!!! Code

        # Assuming 'spark' session is available and the CSV file is at 'path/to/flight_data.csv'

        # Define the schema for the flight data using StructType and StructField
        flight_schema = StructType([
            StructField("Destination Country", StringType(), True), #
            StructField("Origin Country", StringType(), True),      #
            StructField("Count", IntegerType(), True)              #
        ])

        # Read the CSV file applying the defined schema
        # Note: The video uses 'flight_df' as the DataFrame name
        flight_df = spark.read.format("csv") \
                        .option("header", "false") \ # Initially set to false to demonstrate header issues
                        .schema(flight_schema) \    # Apply the custom schema
                        .load("dbfs:/FileStore/tables/flight_data.csv") # Example path

        # To display the schema of the loaded DataFrame
        # flight_df.printSchema()


**Handling Headers and Skipping Rows**

Problem Scenario: If `header=False` is set and the data includes a header row (e.g., "Count" as the first value in the `Count` column), Spark will attempt to parse "Count" as an `Integer`. This will result in `null` values for that row/column if the reading `mode` is `permissive`, or an error if the `mode` is `failfast`.

Solution 1: Using `mode("permissive")`:
The `mode("permissive")` option allows Spark to continue reading the data even if there are type mismatches, converting problematic values to `null` instead of failing the job.

!!! Code

        flight_df = spark.read.format("csv") \
                        .option("header", "false") \
                        .schema(flight_schema) \
                        .option("mode", "permissive") \ # Allows nulls for type mismatches
                        .load("dbfs:/FileStore/tables/flight_data.csv")
        # After this, the first row's 'Count' column would likely be null because 'Count' (string) cannot be an Integer.


Solution 2: Skipping Rows with `option("skipRows", "N")`:
A more direct way to handle unwanted header rows (or any initial rows) is to use the `skipRows` option. This option allows you to skip a specified number of rows from the beginning of the file.

!!! Code

        # To skip the first row (e.g., a header row)
        flight_df_skipped_header = spark.read.format("csv") \
                                    .option("header", "false") \ # Header detection is off
                                    .option("skipRows", "1") \   # Skips the first row (the actual header)
                                    .schema(flight_schema) \
                                    .load("dbfs:/FileStore/tables/flight_data.csv")

        # To skip multiple initial rows (e.g., the first three rows)
        flight_df_skipped_multiple = spark.read.format("csv") \
                                        .option("header", "false") \
                                        .option("skipRows", "3") \ # Skips the first three rows
                                        .schema(flight_schema) \
                                        .load("dbfs:/FileStore/tables/flight_data.csv")

This is a robust way to ensure that the schema aligns with the actual data, excluding any rows that are not part of the data records.

### **Handling corrupted record**
When reading data, Spark offers different modes to handle corrupted records, which influence how the DataFrame is populated.

In permissive mode, all records are allowed to enter the DataFrame. If a record is corrupted, Spark sets the malformed values to null and does not throw an error. For the example data with five total records (two corrupted), permissive mode will result in five records in the DataFrame, with nulls where data is bad.

In dropMalformed mode, Spark discards any record it identifies as corrupted. Given the example data has two corrupted records out of five, this mode will produce a DataFrame with three records

In failfast mode, Spark immediately throws an error and stops the job as soon as it encounters the first corrupted record. This mode will result in zero records in the DataFrame because the job will fail.

### **How to Print Bad Records**

To specifically identify and view the corrupted records, you need to define a manual schema that includes a special column named _corrupt_record. This column will capture the raw content of the corrupted record.

**Where to store bad record**
For scenarios with a large volume of corrupted records (e.g., thousands), printing them is not practical. Spark provides the badRecordsPath option to store all corrupted records in a specified location. These records are saved in JSON format at the designated path

### **Read Json in Spark**

Reading JSON files in PySpark is straightforward. The general method involves using spark.read.format("json").load().
Basic Read Operation: 

The simplest way to read a JSON file is as follows:
!!! Code

        df = spark.read.format("json").load("path/to/your/json_file.json")
        df.show()
        

### **Datafram Write**
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


