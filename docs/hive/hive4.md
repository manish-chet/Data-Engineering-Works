
### **Primary key in Hive**

Apache Hive does not enforce primary key constraints natively like traditional RDBMS systems do. Hive is designed to operate on large datasets using a distributed computing approach, which is fundamentally different from how relational databases manage data.
However, from Hive 2.1.0 onwards, there is support for defining primary keys during table creation for informational purposes, but they are not enforced by Hive itself.


### **Map Side Join (Broadcast Join) in Hive**

A Map Side Join (also known as Map Join) is an optimized version of the join operation in Hive, where one table is small enough to fit into memory. This smaller table (also known as the dimension table) is loaded into memory, and the larger table (also known as the fact table) is read line by line. Because the join operation occurs at the map phase and doesn't need a reduce phase, it's much faster than a traditional join operation.

To use a Map Join, the following properties need to be set:

 1. hive.auto.convert.join: This property should be set to true. It allows Hive to automatically convert a common join into a Map Join based on the sizes of the tables.
 2. hive.mapjoin.smalltable.filesize: This property sets the maximum size for the small table that can be loaded into memory. If the size of the table exceeds the value set by this property, Hive won't perform a Map Join. The default value is 25000000 bytes (approximately 25MB).
    SET hive.auto.convert.join=true;
    SET hive.mapjoin.smalltable.filesize=50000000;  // setting limit to 50MB

Also, keep in mind that if your join operation includes more than two tables, the table in the last position of the FROM clause is considered the large table (fact table), and the other tables are considered small tables 
(dimension tables). This matters because Hive attempts to perform the Map Join operation using the last table as the fact table.

### **Bucket Map Join in Hive**
A Bucket Map Join is an optimization of a Map Join in Hive where both tables are bucketed on the join columns. Instead of loading the entire small table into memory as done in a standard Map Join, the Bucket Map Join only needs to load the relevant bucket from the small table into memory, reducing memory usage and potentially allowing larger tables to be used in a Map Join.

To perform a Bucket Map Join, the following conditions need to be satisfied:

Both tables should be bucketed on the join column.The number of buckets in the large table should be a multiple of the number of buckets in the small table.

To enable Bucket Map Joins, the following properties need to be set:

 1. hive.auto.convert.join: This property should be set to true. It allows Hive to automatically convert a common join into a Map Join based on the sizes of the tables.
 2. hive.optimize.bucketmapjoin: This property should be set to true to allow Hive to convert common joins into Bucket Map Joins when possible.
    SET hive.auto.convert.join=true;
    SET hive.optimize.bucketmapjoin=true;

### **Sorted Merge Bucket Join in Hive**

A Sorted Merge Bucket (SMB) Join in Hive is an optimization for bucketed tables where not only are the tables bucketed on the join column, but also sorted on the join column. This is similar to the bucket map join, but SMB join does not require one table to fit into memory, making it more scalable.

For a Sorted Merge Bucket Join, the following conditions need to be satisfied:

1. Both tables should be bucketed and sorted on the join column.
2. Both tables should have the same number of buckets.


When these conditions are satisfied, each mapper can read a bucket from each table at a time and perform the join, significantly reducing the disk I/O operations.

To enable SMB Joins, the following properties need to be set:

 1. hive.auto.convert.sortmerge.join: This property should be set to true. It allows Hive to automatically convert common joins into Sorted Merge Bucket Joins when possible.
 2. hive.optimize.bucketmapjoin.sortedmerge: This property should be set to true to allow Hive to perform a SMB Join.


### **Skew Join in Hive**

A Skew Join in Hive is an optimization technique for handling skewed data, where some values appear very frequently compared to others in the dataset. In a typical MapReduce job, skewed data can lead to a few reducers taking much longer to complete than others because they process a majority of the data. This can negatively impact the overall performance of the join.

A Skew Join in Hive tries to handle this problem by performing the join in two stages:

1. In the first stage, Hive identifies the skewed keys and processes all the non-skewed keys.
2. In the second stage, Hive processes the skewed keys. The skewed keys are partitioned into different reducers based on a hash function, thus reducing the burden on a single reducer.

To perform a Skew Join, the following conditions need to be satisfied:

1. The join should be a two-table join. Currently, Hive does not support multi-table skew joins.
2. There should be skew in key distribution. If the key distribution is uniform, a skew join may not provide any advantage and can be less efficient than a regular join.


To enable Skew Joins, the following properties need to be set:

 1. hive.optimize.skewjoin: This property should be set to true. It enables the skew join optimization.
 2. hive.skewjoin.key: This property sets the minimum number of rows for a key to be considered skewed. The default value is 10000.