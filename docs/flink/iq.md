# FLINK_IQ

!!!- info "1. See you using Flink, briefly introduce Flink?"
    Apache Flink is an open-source stream processing and batch processing framework designed for big data processing and analytics. It provides fault tolerance, high throughput, and low-latency processing of large-scale data streams

!!!- info "2. What are the differences between Flink and Spark Streaming?"
    1. The design ideas are different. Flink considers batch to be a kind of streaming, and spark considers a streaming batch.
    2. The architecture model is different. Spark has Driver, Master, Worker, and Executor. Flink has the concepts of TaskManager, JobManager, Task, SubTask, and Slot
    3. Flink's streaming data processing is much stronger than spark, for example, time supports three kinds of time
    There are more windows than spark
    4. In the case of out-of-order data, Flink is stronger than spark, because flink has watermark. In fact, the calculation method when running is the time of the last data-if watermaker is greater than the end of the window, execute
    5. For fault tolerance, flink is also better than spark. For example, flink supports two-stage transactions to ensure that data after program crashes will not be re-consumed. Spark also has checkpoints, but it only ensures that data is not lost, and it cannot be repeated. consumption.


!!!- info "3. What are the roles of Flink cluster? What are the functions?"
    Flink programs mainly have three roles: TaskManager, JobManager, and Client when they are running.

    JobManager In the role of a manager in the cluster, it is the coordinator of the entire cluster. It is responsible for receiving the execution of Flink Job, coordinating checkpoints, recovering from failures, and managing Task Manager.

    TaskManager It is responsible for the resource information on the node where the manager is located, such as memory, disk, and network. It will report the resource to the JobManager when it is started.

    Client It is the client submitted by the Flink program. When a user submits a Flink program, a Client is first created. Then the program submitted by the user will be preprocessed and submitted to the cluster for processing.

!!!- info "4. What is TaskSlot?"
    In Flink's architecture, TaskManager is the working node that is actually used to execute our program. TaskManager is a JVM process. In fact, in order to achieve the concept of resource isolation and parallel execution, the concept of TaskSlot was proposed at this time, which is actually In order to control how many Tasks the TaskManager can receive, the TaskManager is controlled by taskslot, that is, if we have a source that specifies three parallelism, then he will use three slots, and the other one needs to be mainly parallel as an operator When the degree is the same, and there is no change in the degree of parallelism, or there is no shuffle, they will be together at this time. This is an optimized concept.

!!!- info "5. What are the commonly used operators in Flink?"
    Map operator

    Filter operator

    KeyBy operator

    Window window

!!!- info "6. What is the parallelism of Flink and What is the parallelism setting of Flink?"
    The parallelism of Flink is well understood. For example, kafkaSource, its parallelism is the number of partitions by default. The degree of parallelism is this operator, and how many taskslot are needed, we should know that is the advantage of parallel computing. Generally, the degree of parallelism is set according to the amount of data. It is best to keep the source and map operators without shuffle, because the pressure on the source and map operators is not very large, but when our data table is widened, It is better to set it larger.

!!!- info "7. What is the relationship between Flink's Slot and parallelism?"
    slot is a concept in TaskManager. Parallelism is a concept in the program, that is, the concept of execution level. In fact, slot specifies how many slots this TaskManager has and how much parallelism can be supported, but the parallelism developed by the program uses slots That is slot, that is, TaskManager is the provider and the program is the user

!!!- info "8. What if Flink encounters an abnormal restart of the program?"
    Flink has some restart strategies, and as long as the checkpoint is done, it can be done at least once. Of course, it may not be accurate once, but some components can be done. The restart strategy generally set is a fixed delay restart strategy. The restart does not delete the checkpoint. Generally, the number of restarts set by our company is 4 times. If it stops, we will send a nail warning and start from the checkpoint when it starts.

!!!- info "9. Flink's distributed cache"
    The distributed cache implemented by Flink is similar to Hadoop. The purpose is to read the file locally and put it in the taskmanager node to prevent the task from repeatedly pulling data and reduce performance.

!!!- info "10. Broadcast variables in Flink"
    We know that Flink is parallel, and the calculation process may not be performed in a Slot. Then there is a situation: when we need to access the same data. Then the broadcast variable in Flink is to solve this situation. We can understand the broadcast variable as a public shared variable. We can broadcast a dataset, and then different tasks can be obtained on the node. There will only be one copy of this data on each node.

!!!- info "11. Do you know what windows in Flink are?"
    Flink supports two ways to divide windows, according to time and count. session is also a kind of time

    Tumbing Count Window： Perform calculation when reaching a certain number, no folding

    Sliding Time Window： When a certain period of time is reached, roll over, there can be overlap, generally used to calculate the recent demand, such as nearly 5 minutes.

    Tubing time Window： When a certain period of time is reached, the slide is carried out, which can be thought of as the Nokia slide phone used before. This is actually a micro batch

    Sliding Count Window： Slide when it reaches a certain number

    Session Window: The window data has no fixed size, it is divided according to the parameters passed in by the user, and the window data does not overlap. It is similar to calculating the user's previous actions when the user logs out.

!!!- info "12. Flink's state storage?"
    Flink often needs to store intermediate states during calculations to avoid data loss and recover from abnormal states. Choosing a different state storage strategy will affect the state interaction between JobManager and Subtask, that is, JobManager will interact with State to store state.

    Flink provides three state storage:
    MemoryStateBackend

    FsSateBackend

    RocksDBStateBackend

!!!- info "13. What kind of time are there in Flink?"
    Event time: the time when the event actually occurred

    Intake time: time to enter flink

    Processing time: the time to enter the flink operator

!!!- info "14. What is Watermark in Flink?"
    Watermark is an operation used by Flink to deal with out-of-order time. In fact, in Flink, if we use event time and take kafka's source, then the window execution time at this time is the smallest among the partitions Partitions are used for triggering, and each partition must be triggered to perform calculations. Why is this? In fact, it is because the partitions of Kafka are disordered. Orderly in the zone. The execution time is the maximum time minus the watermark>window end time, and the calculation will be executed at this time.
    Watermarks are used in Apache Flink to track the progress of event time. They represent a threshold for event times and indicate that no events with timestamps earlier than the watermark should arrive any longer. They help define when window computations should be considered complete.

!!!- info "15. What is Unbounded streams in Apache Flink?"
    Any type of data is produced as a stream of events. Data can be processed as unbounded or bounded streams.
    Unbounded streams have a beginning but no end. They do not end and continue to provide data as it is produced. Unbounded streams should be processed continuously, i.e., events should be handled as soon as they are consumed. Since the input is unbounded and will not be complete at any point in time, it is not possible to wait for all of the data to arrive.
    Processing unbounded data sometimes requires that events are consuming in a specific order, such as the order in which events arrives, to be able to reason about result completeness.

!!!- info "16. What is Bounded streams in Apache Flink?"
    Bounded streams have a beginning and an end point. Bounded streams could be processed by consuming all data before doing any computations. Ordered ingestion is not needed to process bounded streams since a bounded data set could always be sorted. Processing of bounded streams is also called as batch processing.

!!!- info "17. What is Dataset API in Apache Flink?"
    The Apache Flink Dataset API is used to do batch operations on data over time. This API is available in Java, Scala, and Python. It may perform various transformations on datasets such as filtering, mapping, aggregating, joining, and grouping.

    DataSet API helps us in enabling the client to actualize activities like a guide, channel, gathering and so on.It is utilized for appropriated preparing, it is an uncommon instance of stream preparing where we have a limited information source.They are regular programs that implement transformation on data sets like filtering, mapping, etc.

    Data sets are created from sources like reading files, local collections, etc.All the results are returned through sinks, the execution can happen in a local JVM or on clusters of many machines.

    DataSet<Tuple2<String, Integer>> wordCounts = text
    .flatMap(new LineSplitter())
    .groupBy(0)
    .sum(1);

!!!- info "18. What is DataStream API in Apache Flink?"
    The Apache Flink DataStream API is used to handle data in a continuous stream. On the stream data, you can perform operations such as filtering, routing, windowing, and aggregation. On this data stream, there are different sources such as message queues, files, and socket streams, and the resulting data can be written to different sinks such as command line terminals. This API is supported by the Java and Scala programming languages.

    DataStream<Tuple2<String, Integer>> dataStream = env
    .socketTextStream("localhost", 9091)
    .flatMap(new Splitter())
    .keyBy(0)
    .timeWindow(Time.seconds(7))
    .sum(1);

!!!- info "19. What is Apache Flink Table API?"
    Table API is a relational API with an expression language similar to SQL. This API is capable of batch and stream processing. It is compatible with the Java and Scala Dataset and Datastream APIs. Tables can be generated from internal Datasets and Datastreams as well as from external data sources. You can use this relational API to perform operations such as join, select, aggregate, and filter. The semantics of the query are the same if the input is batch or stream.
    val tableEnvironment = TableEnvironment.getTableEnvironment(env)
    // register a Table
    tableEnvironment.registerTable("TestTable1", ...);
    // create a new Table from a Table API query
    val newTable2 = tableEnvironment.scan(TestTable1).select(...);

!!!- info "20. What is Apache Flink FlinkML?"
    FlinkML is the Flink Machine Learning (ML) library. It is a new initiative in the Flink community, with an expanding list of algorithms and contributors. FlinkML aims to include scalable ML algorithms, an easy-to-use API, and tools to help reduce glue code in end-to-end ML systems. Note: Flink Community has planned to delete/deprecate the legacy flink-libraries/flink-ml package in Flink1.9, and replace it with the new flink-ml interface proposed in FLIP39 and FLINK-12470.


!!!- info "21. Explain the Apache Flink Job Execution Architecture?"
    Program: It is a piece of code that is executed on the Flink Cluster.

    Client: It is in charge of taking code from the given programm and creating a job dataflow graph, which is then passed to JobManager. It also retrieves the Job data.

    JobManager: It is responsible for generating the execution graph after obtaining the Job Dataflow Graph from the Client. It assigns the job to TaskManagers in the cluster and monitors its execution.

    TaskManager:It is in charge of executing all of the tasks assigned to it by JobManager. Both TaskManagers execute the tasks in their respective slots in the specified parallelism. It is in charge of informing JobManager about the status of the tasks.

!!!- info "22. What are the features of Apache Flink?"
    One of the key features of Apache Flink is its ability to process data in real-time with low-latency and high throughput. It supports event time processing, which means it can handle out-of-order events and provide correct results based on event timestamps. Flink also provides extensive windowing operations for aggregating data within time intervals, such as tumbling windows, sliding windows, and session windows.

    Another important feature of Flink is its support for fault-tolerance. It achieves fault-tolerance through a mechanism called "exactly-once" processing, which guarantees that each event is processed exactly once, even in the presence of failures. This is crucial for applications where data correctness is paramount.

    Apache Flink can process all data in the form of streams at any point in time.
    Apache Flink does not give a burden on users' shoulders for tunning or managing the physical execution concepts.
    The memory management is done by the Apache Flink itself and not by the user.
    Apache Flink optimizer chooses the best plan to execute the user's program hence very little intervention is required in terms of tunning.
    Apache Flink can be deployed on various cluster frameworks.
    It is capable to support various types of the file system.
    Apache Flink can be integrated with Hadoop YARN in a very good way.


!!!- info "23. What are the Apache Flink domain-specific libraries?"
    The following is the list of Apache Flink domain-specific libraries.
    FlinkML: It is used for machine learning.
    Table: It is used to perform the relational operation.
    Gelly: It is used to perform the Graph operation.
    CEP: It is used for complex event processing.

!!!- info "24. What is the programing model of Apache Flink?"
    The Apache Flink Datastream and the Dataset work as a programming model of flink and its other layers of architecture. The Datastream programming model is useful in real-time stream processing whereas the Dataset programming model is useful in batch processing.


!!!- info "25. What are the use cases of Apache Flink?"
    Many real-world industries are using Apache Flink and their use cases are as mentioned below.

    Financial Services
    Financial industries are using Flink to perform fraud detection in real-time and send mobile notifications.

    Healthcare
    The hospitals are using Apache Flink to collect data from devices such as MRI, IVs for real-time issue detection and analysis.

    Ad Tech
    Ads companies are using Flink to find out the real-time customer preference.

    Oil Gas
    The Oil and Gas industries are using Flink for real-time monitoring of pumping and issue detection.

    Telecommunications
    The telecom companies are using Apache Flink to provide the best services to the users such as real-time view of billing and payment, the optimization of antenna per-user location, mobile offers, and so on.

!!!- info "26. What is bounded and unbounded data in Apache Flink?"
    Apache Flink processes data in the form of bounded and unbounded streams. The bounded data will have a start point and an endpoint and the computation starts once all data has arrived. It is also called batch processing. The unbounded data will have a start point but no endpoint because it is streaming of data. The processing of unbounded data is continous and doesn't wait for complete data. As soon the data is generated the processing will start.

!!!- info "27. How Apache Flink handles the fault-tolerance?"
    Apache Flink manages the fault-tolerance of stream applications by capturing the snapshot of the streaming dataflow state so in case of failure those snapshots will be used for recovery. For batch processing, Flink uses the program's sequence of transformations for recovery.

    To achieve fault tolerance, Apache Flink employs a combination of techniques such as data replication, checkpointing, and exactly-once processing semantics. The framework allows users to define fault-tolerant data streams, which are resilient to failures and can effectively recover from possible errors.

    1. Checkpointing: Apache Flink periodically captures the state of executing jobs by taking checkpoints. Checkpoints consist of the in-memory state of all operators and the metadata necessary for restoring the state, such as the offset of each stream source. Users can configure the frequency of checkpoints to strike a balance between reliability and performance

    2. State Backends: Apache Flink supports different state backends (e.g., in-memory, RocksDB) to persist checkpointed state. The chosen backend determines how and where the state is stored, allowing for fault tolerance and efficient recovery.

    3. Exactly-once Processing: Flink's checkpointing, along with its transactional processing capabilities, enables exactly-once processing semantics. It ensures that each record is processed exactly once, even in the presence of failures or system restarts. This guarantees consistency and correctness in data processing.

    4. Failure Handling: In case of failures, Flink automatically reverts the system to the latest successful checkpoint. It replays the data from that point onwards, resuming processing from a consistent state.


!!!- info "28. What is the responsibility of JobManager in Apache Flink Cluster?"
    The Job Manager is responsible for managing and coordinating with distributed processing of a program. It assigns the task to node managers, handles the failures for recovery, and performs the checkpointing. It has three components namely ResourceManager, Dispatcher, and JobMaster.

!!!- info "29. What is the responsibility of TaskManager in Apache Flink Cluster?"
    The Task Manager is responsible for executing the dataflow task and return the result to JobManager. It executes the task in the form of a slot hence the number of slots shows the number of process execution.


!!!- info "30. What is the difference between stream processing and batch processing?"
    In Batch processing, the data is a bounded set of the stream that has a start point and the endpoint, so once the entire data is ingested then only processing starts in batch processing mode. In-stream processing the nature of data is unbounded which means the processing will continue as the data will be received.

    Flink How to ensure accurate one-time consumption
    Flink There are two ways to ensure accurate one-time consumption Flink Mechanism
    1、Checkpoint Mechanism
    2、 Two stage submission mechanism

    Checkpoint Mechanism:Mainly when Flink Turn on Checkpoint When , Will turn out for the Source Insert a barrir, And then this barrir As the data flows all the time , When it comes to an operator , This operator starts to make checkpoint, It's made from barrir The state of the current operator when it comes to the previous time , Write the state to the state backend . And then barrir Flow down , When it flows to keyby perhaps shuffle Operator time , For example, when the data of an operator , Depending on multiple streams , There will be barrir alignment , That is, when all barrir All come to this operator to make checkpoint, Flow in turn , When it flows to sink Operator time , also sink The operator is also finished checkpoint Will send to jobmanager The report checkpoint n Production complete .

    Two stage submission mechanism: Flink Provides CheckpointedFunction And CheckpointListener These two interfaces ,CheckpointedFunction There is snapshotState Method , Every time checkpoint Trigger execution method , The cache data is usually put into the State , You can think of it as one hook, This method can be used to achieve pre submission ,CheckpointListyener There is notifyCheckpointComplete Method ,checkpoint Notification method after completion , There are some extra operations that can be done here . for example FLinkKafkaConumerBase Use this to do Kafka offset Submission of , In this method, you can implement the submit operation . stay 2PC If the corresponding process, such as a checkpoint Failure words , that checkpoint It will roll back , No impact on data consistency , So if you're informing checkpoint Success followed by failure , Then it will be in initalizeSate Method to complete the transaction commit , This ensures data consistency . It's mainly based on checkpoint The state file to judge .

    flink and spark difference: flink It's a similar spark Of " Open source technology stack ", Because it also provides batch processing , Flow computation , Figure calculation , Interactive query , Machine learning, etc .flink It's also memory computing , similar spark, But the difference is ,spark The calculation model of is based on RDD, Consider streaming as a special batch process , His DStream In fact, or RDD. and flink Consider batch processing as a special stream computing , But there are two engines in the layer of batch processing and streaming computing , Abstract the DataSet and DataStream.flink It's also very good in performance , Streaming delay ratio spark Less , Can do real flow computing , and spark It can only be a quasi flow calculation . And in batch processing , When the number of iterations gets more ,flink Faster than spark faster , So if flink Come out earlier , Maybe more than what we have now Spark More fire .


!!!- info "31. Flink watermark Transmission mechanism."
    Flink Medium watermark Mechanism is used to deal with disorder ,flink It has to be event time , A simple example is , If the window is 5 second ,watermark yes 2 second , that All in all 7 second , When will calculation be triggered at this time , Suppose the initial time of the data is 1000, Then wait until 6999 It will trigger 5999 The calculation of windows , So the next one is 13999 Is triggered when 10999 The window of
    In fact, this is watermark The mechanism of , In multi parallelism , For example, in kafka The window will not be triggered until all partitions are reached

!!!- info "32. Flink window join:"
    1、window join, That is, according to the specified fields and scrolling sliding window and session window inner join

    2、 yes coGoup In fact, that is left join and right join,

    3、interval join That is to say In the window join There are some problems , Because some of the data really came after the meeting , It's still a long time , Then there will be interval join But it has to be the time of the event , And also specify watermark And water level and getting event timestamps . And set it up Offset interval , because join I can't wait all the time .


!!!- info "33. keyedProcessFunction How it works"
    keyedProcessFunction There is one ontime Operation of the , If so event In time that The time to call is to look at ,event Of watermark Is it greater than trigger time Time for , If it is greater than, calculate it , No, just wait , If it is kafka Words , Then the default is to trigger the partition key in the shortest time .

!!!- info "34. How to deal with offline data such as the association with offline data?"
    1、async io
    2、broadcast
    3、async io + cache
    4、open Method , Then the thread is refreshed at a fixed time , Cache updates are deleted first , Then write another one, and then write to the cache

!!!- info "35. What if there is a data skew?"
    Flink How to view data skew ：
    stay flink Of web ui You can see the data skew in , It's every one subtask The amount of data processed varies greatly , For example, some have only one M yes , we have 100M This is a serious data skew .
    KafkaSource Data skew at the end
    For example, upstream kafka It was specified when it was sent key There are data hotspots , So just after the access , Do a load balancing （ The premise is not keyby）.
    Aggregation class operator data skew
    Pre aggregation plus global aggregation

!!!- info "36. FlinkTopN And offline TopN The difference between?"
    topn It is a common function in both offline and real-time computing , It's different from... In offline computing topn, Real time data is continuous , This will give topn It's very difficult to calculate , Because it's going to keep a... In memory topn Data structure of , When new data comes , Update this data structure

!!!- info "37. Sparkstreaming and flink in checkpoint?"
    sparkstreaming Of checkpoint It will lead to repeated consumption of data
    however flink Of checkpoint Sure Make sure it's accurate one time , At the same time, it can be incremental , fast checkpoint Of , There are three states ,memery、rocksdb、hdfs

!!!- info "38. A brief introduction cep State programming:"
    Complex Event Processing（CEP）：
    FLink Cep Is in FLink Complex time processing library implemented in ,CEP Allows event patterns to be detected in an endless stream of time , Give us a chance to grasp the important parts of the data , One or more time streams composed of simple events are matched by certain rules , Then output the data the user wants , That is, complex events that satisfy the rules .

    Flink Data aggregation in , How to aggregate without windows
    valueState Used to save a single value
    ListState Used to hold list Elements
    MapState Used to save a set of key value pairs
    ReducingState Provided with ListState Same method , Return to one ReducingFunction The aggregated value .
    AggregatingState and ReducingState similar , Return to one AggregatingState The value after internal aggregation

!!!- info "39. How to deal with abnormal data in Flink."
    Abnormal data in our scenario , It is generally divided into missing fields and outlier data .
    outliers ： For example, data on the age of the baby , For example, for the maternal and infant industry , The age of a baby is a crucial data , It's the most important , Because the baby is bigger than 3 At the age of 20, you hardly buy things from mothers and babies . There are days like ours 、 Unknown 、 And for a long time . This is an exception field , We will show the data to store managers and regional managers , Let them know how many ages are not allowed . If we have to deal with it , It can be corrected in real time according to the time of purchase , For example, maternity clothing 、 The rank of milk powder 、 The size of a diaper , As well as pacifiers, some can distinguish the age group to carry on the processing . We don't process the data in real time , We're going to have a low-level strategy task, night dimension, to run , Run once a week .
    Missing field ： For example, some fields are really missing , If you can fix it, you can fix it . Give up if you can't fix it , It's like the news recommendation filter in the last company .

!!!- info "40. Is there any possibility of data loss in Flink?"
    Flink There are three kinds of data consumption semantics ：
    At Most Once One consumption at most In case of failure, it may be lost
    At Least Once At least once If there is a fault, it may be repeated
    Exactly-Once Exactly once If something goes wrong , It can also ensure that the data will not be lost or repeated .
    flink The new version is no longer available At-Most-Once semantics .

    Flink interval join Can you write it simply
    DataStream<T> keyed1 = ds1.keyBy(o -> o.getString("key"))
    DataStream<T> keyed2 = ds2.keyBy(o -> o.getString("key"))
    // Time stamp on the right -5s<= Stream timestamp on the left <= Time stamp on the right -1s
    keyed1.intervalJoin(keyed2).between(Time.milliseconds(-5), Time.milliseconds(5))


!!!- info "41. How to maintain Checkpoint?"
    By default , If set Checkpoint Options ,Flink Only the most recently generated 1 individual Checkpoint. When Flink When the program fails , From the nearest one Checkpoint To recover . however , If we want to keep more than one Checkpoint, And can choose one of them to recover according to the actual needs , It's more flexible .Flink Support to keep multiple Checkpoint, Need to be in Flink Configuration file for conf/flink-conf.yaml in , Add the following configuration to specify that at most Checkpoint The number of .
    For small files, please refer to The death of Daedalus - Solutions to the problem of small files in the field of big data .

!!!- info "42. What's the difference at Spark and Flink Serialization?"
    Spark The default is Java Serialization mechanism , At the same time, there is an optimization mechanism , That is to say kryo
    Flink It's a self implemented serialization mechanism , That is to say TypeInformation

!!!- info "43. How to deal with late data?"
    In Flink, late data refers to events that arrive after the watermark has progressed past their event time. This typically happens due to network delays, out-of-order arrival, or slow event sources.

    To handle late data, Flink provides the following mechanisms:

    Allowed Lateness
    You can configure how long Flink should wait for late events using the allowedLateness() method.

    java
    Copy
    Edit
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .allowedLateness(Time.minutes(2))
    This keeps the window open for 2 extra minutes to accept late events.

    Late elements within this period will update the window and trigger re-evaluation.

    Side Output for Late Data
    Events that arrive after the allowed lateness can be redirected to a side output for separate handling.

    java
    Copy
    Edit
    OutputTag<Event> lateOutputTag = new OutputTag<Event>("late-data"){};
    windowedStream
        .sideOutputLateData(lateOutputTag);
    You can process or store this late data elsewhere for analysis or alerting.

    Watermarks Configuration

    Watermarks indicate the progress of event time. You can use bounded out-of-orderness watermarks to tolerate out-of-order events.

    java
    Copy
    Edit
    env.assignTimestampsAndWatermarks(
        WatermarkStrategy.<Event>forBoundedOutOfOrderness(Duration.ofMinutes(2))
    );

   
!!!- info "44. When to use aggregate perhaps process:"
    aggregate： Incremental aggregation
    process： Total polymerization
    When calculating the accumulation operation, you can use aggregate operation .
    When calculating the full amount of data in the window, use process, For example, sorting and other operations.

!!!- info "45. How does Flink handle stateful computations efficiently:"
    Flink is designed to handle stateful computations efficiently by using a distributed and fault-tolerant mechanism called StateBackend. It provides several options for managing state, including in-memory state and state that can be stored on disk or in an external system like Apache Hadoop or Amazon S3.

    Flink's StateBackend allows users to choose between three options: MemoryStateBackend, FsStateBackend, and RocksDBStateBackend. These options differ in terms of their trade-offs between performance and fault tolerance. For example, the MemoryStateBackend provides high performance and low latency but does not recover state after a failure, while the FsStateBackend provides fault tolerance by storing state on a distributed file system.

!!!- info "46. What are the important factors to consider when tuning the performance of Apache Flink applications:"
    When tuning the performance of Apache Flink applications, several important factors need to be considered. These factors range from resource allocation to algorithm design and configuration settings. Here are some key aspects to focus on:

    1. Resource Allocation: Efficiently allocating resources is crucial for optimal performance. This includes tuning the number of Task Managers and slots, Memory, and CPU resources. Understanding the data and workload patterns can help determine the right resource allocation strategy.

    2. Data Serialization and Deserialization: Choosing the appropriate serialization format can greatly impact performance. Flink provides multiple serialization formats, such as Avro, JSON, and Protobuf. Assessing the size and complexity of data structures can help decide the most suitable serialization method.

    3. Memory Management: Flink employs managed memory which consists of both heap and off-heap memory. Configuring the sizes of managed memory components, such as network buffers and managed memory fractions, can significantly impact performance

    4. Parallelism: Parallelism influences the throughput and resource utilization of Flink applications. Setting an appropriate degree of parallelism, considering the available resources and input characteristics, is important.

    5. Operators' Chaining and State Size: Operator chaining can optimize performance by reducing serialization and deserialization costs. Additionally, Flink provides various state backends, such as MemoryStateBackend and RocksDBStateBackend, that allow selecting different state storage options based on the state size and access patterns.

!!!- info "47. How does Flink handle exactly-once semantics and end-to-end consistency in data processing?:"
    Apache Flink provides built-in mechanisms to handle exactly-once semantics and ensure end-to-end consistency in data processing pipelines. This is essential in scenarios where duplicate or lost data cannot be tolerated, such as financial transactions, data pipelines, or event-driven applications.

    Flink achieves exactly-once semantics through a combination of checkpointing, state management, and transactional sinks. Checkpointing is a mechanism that periodically takes a snapshot of the application's state, including the operator's internal state and the position in the input streams. By storing these checkpoints persistently, Flink can recover the state and precisely revert to a previous consistent state when failures occur. The state managed by operators includes both user-defined operator state and Flink's internal bookkeeping state.

    To enable exactly-once semantics, it is important to ensure that the output of the pipeline is also processed atomically and deterministically. Flink achieves this through transactional sinks, which are responsible for writing the output of a stream into an external system (e.g., a database). When a failure occurs, these sinks coordinate with Flink's checkpointing to guarantee that the data is only committed if the checkpoint is successful. This ensures that the output of the pipeline is consistent and non-duplicative

!!!- info "48. How does Flink handle windowing in stream processing?:"
    Flink supports various windowing operations, such as tumbling windows, sliding windows, and session windows. Windowing in Flink allows you to group and process events based on time or count constraints. It provides flexibility in defining window sizes and slide intervals.

!!!- info "49. If everything is a stream, why are there a DataStream and a DataSet API in Flink?:"
    Bounded streams are often more efficient to process than unbounded streams. Processing unbounded streams of events in (near) real-time requires the system to be able to immediately act on events and to produce intermediate results (often with low latency). Processing bounded streams usually does not require producing low latency results, because the data is a while old anyway (in relative terms). That allows Flink to process the data in a simple and more efficient way.

    The DataStream API captures the continuous processing of unbounded and bounded streams, with a model that supports low latency results and flexible reaction to events and time (including event time).
    The DataSet API has techniques that often speed up the processing of bounded data streams. In the future, the community plans to combine these optimizations with the techniques in the DataStream API.

!!!- info "50. What are windowing strategies in Flink?"
    Windowing assigns unbounded streams into finite-sized windows for aggregation. Common strategies include: Time windows (fixed or sliding), Count windows (fixed number of events), and Session windows (gaps between events define windows).

!!!- info "51. What are the different types of operators in Flink?:"
     Flink operators include *map*, *flatmap*, *filter*, *keyBy*, *window*, *reduce*, *aggregate*, *join*, etc., offering a rich set of transformations for data processing.

!!!- info "52. What is the difference between a keyed and non-keyed stream in Flink?:"
    Keyed streams partition data based on a key, enabling operations like windowing and stateful aggregations on specific keys. Non-keyed streams process data without partitioning.

!!!- info "53. Explain the role of the process function in Flink."
    Process functions are low-level operators that provide fine-grained control over event processing and state management. They offer advanced features like timers and custom state management logic.

!!!- info "54. What are the different windowing techniques in Apache Flink?:"
    Apache Flink supports a variety of windowing techniques, including:

    Tumbling windows: These windows are fixed in size and slide across the stream.

    Sliding windows: These windows are variable in size and slide across the stream.

    Session windows: These windows are based on the arrival time of events.

    Count windows: These windows are based on the number of events that arrive within a given time interval.


!!!- info "55. What is the difference between bounded and unbounded streams?:"
    Bounded streams are datasets that have a defined start and end.
    Unbounded streams are datasets that have a defined start but no defined end.
    Bounded streams can be processed by ingesting the complete data and them preforming any computations.
    Unbounded streams have to be processed continuously as new data comes in.
    In most cases, unbounded streams have to be process in the order in which messages are received.
    Bounded messages can be processed in any order since the messages can be sorted as needed.

!!!- info "56. What features does flink framework provide to handle state?"
    Flink framework provides the following features to handle state.
    Data structure specific state primitives - Flink framework provides specific state primitives for different data structures such as lists and maps.
    Pluggable state storages - Flink supports multiple pluggable state storage systems that store state in-memory or on disc.
    Exactly-once state consistency - Flink framework has checkpoint and recovery algorithms, which guarantee the consistency of state in case of failures.
    Store large state data - Flink has the ability to store very large application state data, of several terabytes, due to its asynchronous and incremental checkpoint algorithm.
    Scalable Applications - Flink applications are highly scalable since the application state data can be distributed across containers.

!!!- info "57. What features does flink framework provide to handle time?:"
    Flink framework provides the following features to handle time.
    Event-time mode - Flink framework supports applications that process steams based on event-time mode, i.e. applications that process streams based on timestamp of events.
    Processing-time mode - Flink framework also supports applications that process streams based on processing-time mode, i.e. applications that process streams based on the clock time of the processing machine.
    Watermark support Flink framework provides watermark support in the processing of streams based on event-time mode.
    Late data processing Flink framework supports the processing of events that arrive late, after a related computation has already been performed.

