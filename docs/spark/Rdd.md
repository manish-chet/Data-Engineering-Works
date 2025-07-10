RDDs are the building blocks of any Spark application. RDDs Stands for:

1. Resilient: Fault tolerant and is capable of rebuilding data on failure
2. Distributed: Distributed data among the multiple nodes in a cluster
3. Dataset: Collection of partitioned data with values
Resilient Distributed Datasets (RDD) are a core abstraction in Apache Spark. Here are some key points about RDDs and their properties:
4. Fundamental Data Structure: RDD is the fundamental data structure of Spark, which allows it to efficiently operate on large-scale data across a distributed environment.
5. Immutability: Once an RDD is created, it cannot be changed. Any transformation applied to an RDD creates a new RDD, leaving the original one untouched.
6. Resilience: RDDs are fault-tolerant, meaning they can recover from node failures. This resilience is provided through a feature known as 
lineage, a record of all the transformations applied to the base data.
7. Lazy Evaluation: RDDs follow a lazy evaluation approach, meaning transformations on RDDs are not executed immediately, but computed only when an action (like count, collect) is performed. This leads to optimized computation.
8. Partitioning: RDDs are partitioned across nodes in the cluster, allowing for parallel computation on separate portions of the dataset.
9. In-Memory Computation: RDDs can be stored in the memory of worker nodes, making them readily available for repeated access, and thereby speeding up computations.
10. Distributed Nature: RDDs can be processed in parallel across a Spark cluster, contributing to the overall speed and scalability of Spark.
11. Persistence: Users can manually persist an RDD in memory, allowing it to be reused across parallel operations. This is useful for iterative algorithms and fast interactive use.
12. Operations: Two types of operations can be performed on RDDs - transformations (which create a new RDD) and actions (which return a value to the driver program or write data to an external storage system).

