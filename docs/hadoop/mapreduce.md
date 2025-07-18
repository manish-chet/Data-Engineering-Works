### **MapReduce**
MapReduce is a programming framework that allows us to perform distributed and parallel processing on large data sets in a distributed environment.

MapReduce consists of two distinct tasks — Map and Reduce.

As the name MapReduce suggests, reducer phase takes place after the mapper phase has been completed.

So, the first is the map job, where a block of data is read and processed to produce key-value pairs as intermediate outputs.

The output of a Mapper or map job (key-value pairs) is input to the Reducer.

The reducer receives the key-value pair from multiple map jobs.

Then, the reducer aggregates those intermediate data tuples (intermediate key-value pair) into a smaller set of tuples or key-value pairs which is the final output.

### **Advantages of MapReduce**
- Parallel Processing: In MapReduce, we are dividing the job among multiple nodes and each node works with a part of the job simultaneously. So, MapReduce is based on Divide and Conquer paradigm which helps us to process the data using different machines very quickly.

- Data Locality: Instead of moving data to the processing unit, we are moving the processing unit to the data in the MapReduce Framework.  In the traditional system, we used to bring data to the processing unit and process it. But, as the data grew and became very huge, bringing this huge amount of data to the processing unit posed the following issues:

Moving huge data to processing is costly and deteriorates the network performance.
Processing takes time as the data is processed by a single unit which becomes the bottleneck.
The master node can get over-burdened and may fail.

Now, MapReduce allows us to overcome the above issues by bringing the processing unit to the data. This allows us to have the following advantages:

 1. It is very cost-effective to move processing unit to the data.

 2. The processing time is reduced as all the nodes are working with their part of the data in parallel.

 3. Every node gets a part of the data to process and therefore, there is no chance of a node getting overburdened.

### **MapReduce Data Flow**

![Steps](mapreduce.svg)

- Input Files: The data for a MapReduce task is stored in input files, and input files typically lives in HDFS.

- InputFormat: Now, InputFormat defines how these input files are split and read. It selects the files or other objects that are used for input.

- InputSplits: It is created by InputFormat, logically represent the data which will be processed by an individual Mapper. One map task is created for each split; thus the number of map tasks will be equal to the number of InputSplits.

- RecordReader: It communicates with the InputSplit in Hadoop MapReduce and converts the data into key-value pairs suitable for reading by the mapper.

- Mapper: It processes each input record (from RecordReader) and generates new key-value pair, and this key-value pair generated by Mapper is completely different from the input pair. The output of Mapper is also known as intermediate output which is written to the local disk. The output of the Mapper is not stored on HDFS as this is temporary data and writing on HDFS will create unnecessary copies.

- Combiner: The combiner is also known as ‘Mini-reducer’. Hadoop MapReduce Combiner performs local aggregation on the mappers’ output, which helps to minimize the data transfer between mapper and reducer.

- Partitioner: Hadoop MapReduce, Partitioner comes into the picture if we are working on more than one reducer (for one reducer partitioner is not used). Partitioner takes the output from combiners and performs partitioning. Partitioning of output takes place on the basis of the key and then sorted. By hash function, key (or a subset of the key) is used to derive the partition. According to the key value in MapReduce, each combiner output is partitioned, and a record having the same key value goes into the same partition, and then each partition is sent to a reducer.

- Shuffling and Sorting: Now, the output is Shuffled to the reduce node (which is a normal slave node but reduce phase will run here hence called as reducer node). The shuffling is the physical movement of the data which is done over the network. Once all the mappers are finished and their output is shuffled on the reducer nodes, then this intermediate output is merged and sorted, which is then provided as input to reduce phase.

- Reducer: It takes the set of intermediate key-value pairs produced by the mappers as the input and then runs a reducer function on each of them to generate the output. The output of the reducer is the final output, which is stored in HDFS.

- RecordWriter: It writes these output key-value pair from the Reducer phase to the output files.

- OutputFormat: The way these output key-value pairs are written in output files by RecordWriter is determined by the OutputFormat.