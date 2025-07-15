### Broadcast Variables
In Spark, broadcast variables are read-only shared variables that are cached on each worker node rather than sent over the network with tasks. They're used to give every node a copy of a large input dataset in an efficient manner. Spark's actions are executed through a set of stages, separated by distributed "shuffle" operations. Spark automatically broadcasts the common data needed by tasks within each stage.

    from pyspark.sql import SparkSession
    # initialize SparkSession 
    spark = SparkSession.builder.getOrCreate()
    # broadcast a large read-only lookup table
    large_lookup_table = {"apple": "fruit", "broccoli": "vegetable", "chicken": "meat"}
    broadcasted_table = spark.sparkContext.broadcast(large_lookup_table)
    def classify(word):
        # access the value of the broadcast variable  
        lookup_table = broadcasted_table.value     
        return lookup_table.get(word, "unknown")
    data = ["apple", "banana", "chicken", "potato", "broccoli"] 
    rdd = spark.sparkContext.parallelize(data)
    classification = rdd.map(classify) 
    print(classification.collect())


### Accumulators
Accumulators are variables that are only "added" to through associative and commutative operations and are used to implement counters and sums efficiently. They can be used to implement counters (as in MapReduce) or sums. Spark natively supports accumulators of numeric types, and programmers can add support for new types.

A simple use of accumulators is:
    
    from pyspark.sql import SparkSession
    # initialize SparkSession 
    spark = SparkSession.builder.getOrCreate()
    # create an Accumulator[Int] initialized to 0
    accum = spark.sparkContext.accumulator(0)
    rdd = spark.sparkContext.parallelize([1, 2, 3, 4]) 
    def add_to_accum(x):
        global accum
        accum += x rdd.foreach(add_to_accum)
    # get the current value of the accumulator 
    print(accum.value)
        
