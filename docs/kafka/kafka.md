Apache Kafka is a distributed streaming platform that was developed by LinkedIn in 2010 and later donated to the Apache Software Foundation. It's designed to handle high-throughput, fault-tolerant, and real-time data streaming.

Key characteristics:

   1. Scalable: It supports horizontal scaling by allowing you to add new brokers (servers) to the clusters .
   Fault-tolerant: It can handle failures effectively due to its distributed nature and replication mechanisms .
   2. Durable: Kafka uses a "distributed commit log," which means messages are persisted on disk . This ensures data is not lost even if a server goes down.
   3. Fast: Designed to be as fast as possible .
   4. Performance: Achieves high throughput for both publishing (producers) and subscribing (consumers) .
   5. No data loss: Guarantees that messages are not lost once they are committed to Kafka .
   6. Zero down time: Designed for continuous operation without interruption .
   7. Reliability: Provides reliable message delivery .


###  Kafka Concepts

1.  Topics

       A topic is a stream of messages belonging to a particular category.
       It acts as a logical feed where all batch records (messages) are published.
       Each topic has a unique identifier to distinguish it.
       Illustrative Example: In a news application, you might have topics like sports_news, finance_updates, or weather_alerts. All messages related to sports news would go into the sports_news topic.

2.  Partitions

       Topics are split into partitions.
       All messages within a specific partition are ordered and immutable (meaning they cannot be changed after being written).
       Each message within a partition has a unique ID called an Offset. This offset denotes the message's position within that specific partition.
       Illustrative Example: If your sports_news topic has three partitions (P0, P1, P2), articles related to football might go to P0, basketball to P1, and tennis to P2. Within P0, all football articles will appear in the exact order they were published, each with its unique offset.

3.  Replication

       Replicas are essentially backups of partitions.
       They are not directly read as raw data.
       Their primary purpose is to prevent data loss and provide fault tolerance. If the server hosting an active partition fails, a replica can take over.
       Illustrative Example: If the server hosting Partition P0 of sports_news crashes, a replica of P0 on another server immediately takes over, ensuring that no sports news articles are lost and the news feed remains continuous.

4.  Producers

       Producers are applications that write or publish data to the topics within a Kafka cluster .
       They use the Producer API to send data .
       Producers can choose to write data either at the topic level (letting Kafka distribute it across partitions) or to specific partitions of a topic .
       Illustrative Example: A journalist writing a new article would be a producer, publishing the article to the news topic.

5.  Consumers

       Consumers are applications that read or consume data from the topics using the Consumer API .
       Consumers can read data from the topic level (accessing all partitions of a topic) or from specific partitions .
       Consumers are always associated with a consumer group .
       Illustrative Example: A mobile news app that displays articles to users would be a consumer. If it's configured to show "sports news," it consumes messages from the sports_news topic.

6.  Consumer Groups

       A consumer group is a group of related consumers that perform a task .
       Each message in a partition is consumed by only one consumer within a consumer group, ensuring load balancing and avoiding duplicate processing within that group. Multiple groups can consume the same message.
       Illustrative Example: You might have a "mobile app news feed" consumer group and a "website news archive" consumer group. Both groups consume the same news articles, but within the "mobile app" group, if there are multiple instances of the app running, they will share the load of processing new articles.

7.  Zookeeper

       Zookeeper is a critical component used to monitor Kafka clusters and coordinate with them .
       It stores all the metadata information related to Kafka clusters, including the status of replicas and leaders .
       This metadata is crucial for configuration information, cluster health, and leader election within the cluster .
       Zookeeper nodes working together to manage distributed systems are known as a Zookeeper Cluster or Zookeeper Ensemble .
       Illustrative Example: If a Kafka server hosting a partition's leader fails, Zookeeper quickly identifies this and coordinates the election of a new leader from the available replicas, ensuring continuous operation.


### Zookeeper Configuration and Internal States

Zookeeper uses specific parameters and maintains various internal states to manage Kafka.

Zookeeper Configuration Concepts:

   1. initLimit: Defines the time in milliseconds that a Zookeeper follower node can take to initially connect to a leader. For example, 5  2 seconds means 10 seconds. If a node doesn't get in sync within this limit, it's considered out of time.
   2. syncLimit: Defines the time in milliseconds that a Zookeeper follower can be out of sync with the leader. For example, 10  2 seconds means 20 seconds. If a node doesn't sync within this limit, it's considered out of time.
   3. clientPort: This is the port number (e.g., 2181) where Zookeeper clients connect. It refers to the data directory used to store client node server details.
   4. maxClientCnxns: This parameter sets the maximum number of client connections that a single Zookeeper server can handle at once.
   5. server.1, server.2, server.3: These entries define the server IDs and their IP addresses/ports within the Zookeeper ensemble (e.g., server.1: 2888:3888). These are crucial for leader election among the Zookeeper servers.

Kafka Partition States (as managed by Zookeeper):

   1. New Nonexistent Partition: This state indicates that a partition was either never created or was created and then subsequently deleted.
   2. Nonexistent Partition (after deletion): This state specifically means the partition was deleted.
   3. Offline Partition: A partition is in this state when it should have replicas assigned but has no leader elected.
   4. Online Partition: A partition enters this state when a leader is successfully elected for it. If all leader election processes are successful, the partition transitions from Offline Partition to Online Partition.

Kafka Replica States (as managed by Zookeeper):

   1. New Replica: Replicas are created during topic creation or partition reassignment. In this state, a replica can only receive follower state change requests.
   2. Online Replica: A replica is considered Online when it is started and has assigned replicas for its partition. In this state, it can either become a leader or become a follower based on state change requests.
   3. Offline Replica: If a replica dies (becomes unavailable), it moves to this state. This typically happens when the replica is down.
   4. Nonexistent Replica: If a replica is deleted, it moves into this state [3].


### Kafka Cluster & Partition Reassignment

   1. Kafka Cluster Controller: In a Kafka cluster, one of the brokers is designated as the controller. This controller is responsible for managing the states of partitions and replicas and for performing administrative tasks such as reassigning partitions.
   2. Partition Growth: It is important to note that the partition count of a Kafka topic can always be increased, but never decreased. This is because reducing partitions could lead to data loss.
   3. Partition Reassignment Use Cases: Partition reassignment is used in several scenarios:
       Moving a partition across different brokers.
       Rebalancing the replicas of a partition to a specific set of brokers.
       Increasing the replication factor of a topic.

### Internals: Producer Sends Messages

   When a producer sends messages in Kafka, the process involves:

   1. Sending Messages: A producer might send a batch of messages, for example, 10 messages with IDs {0, 1, 2, ..., 9}.
   Partitioning: Messages are sent to different partitions (e.g., P0, P1, P2), potentially including a key, a NULL value (if the key is unused), and the payload.
   2. Offsets: Within each partition, messages are assigned offsets. For example, P0 might have messages with offsets (0,1,2,3,4), P1 with (0,1,2,3,4,5), and P2 with (0,1,2,3,4,5,6).
   3. Effect of Offsets: Offsets help in finding the location of messages and are always significant when reading messages.

### Offsets

Offsets represent the position of each message within a partition and are uniquely identifiable, ever-increasing integers . There are three main variations of offsets :

   1. Log End Offset: This refers to the offset of the last message written to any given partition .
   2. Current Offset: This is a pointer to the last record that Kafka has already sent to the consumer in the current poll .
   3. Committed Offset: This indicates the offset of a message that a consumer has successfully consumed .
   4. Relationship: The committed offset is typically less than the current offset .

### Internals: Consumer Consumes Messages

When a consumer interacts with Kafka to consume messages :

   1. Consumer Poll: The consumer issues a Consumer.poll() request, which may retrieve a certain number of records (e.g., approximately 15 records) .
   3. Consumer Commit: After processing messages, the consumer calls Consumer.commit() to acknowledge that messages up to a certain offset (e.g., in P1, up to offset 5) have been successfully processed .

#### Consumer Group & Rebalancing

   1. Consumer Group: A consumer group is a logical entity within the Kafka ecosystem that primarily facilitates parallel processing and scalable message consumption for consumer clients .
       Every consumer must be associated with a consumer group .
       There is no duplication of messages among consumers within the same consumer group .
   2. Consumer Group Rebalancing: This is the process of re-distributing partitions among the consumers within a consumer group.

      Scenarios for Rebalancing: Rebalancing occurs in several situations:
           A consumer joins the consumer group.
           A consumer leaves the consumer group.
           New partitions are added to a topic, making them available for new consumers.
           Changes in connection states.

   3. Group Coordinator: In a Kafka cluster, one of the brokers is assigned the role of group coordinator to manage consumer groups.
       The group coordinator maintains and manages the list of consumer groups.
       It initiates a callback to communicate the new partition assignments to all consumers during rebalancing.
       Important Note: Consumers within a group undergoing rebalancing will be blocked from reading messages until the rebalance process is complete.
   4. Group Leader: The first consumer to join a consumer group is elected as the Group Leader.
       The Group Leader maintains a list of active members and selects the assignment strategy.
       The Group Leader is responsible for executing the rebalance process.
       Once the new assignment is determined, the Group Leader sends it to the group coordinator.
   5. Consumer Joining a Group: When a consumer starts:
       It sends a "Find Coordinator" request to locate the group coordinator for its group.
       It then initiates the rebalance protocol by sending a "Joining" request.
       Subsequently, members of the consumer group send a "SyncGroup" request to the coordinator.
       Each consumer also periodically sends a "Heartbeat" request to the coordinator to keep its session alive.

### Producer Configurations

When configuring a Kafka producer, several important settings are available:

   1. Bootstrap Servers:
       Used to connect to the Kafka Cluster.
       This specifies the host/port for establishing the initial connection.
   2. Client ID:
       Used to track requests and is mainly for debugging purposes.
       Primarily used for server-side logging.
   3. Key Serializer (and Value Serializer):
       Converts the key/value into a stream of bytes.
       Kafka producers send objects as a stream of bytes, and this setting is used to persist and transmit the object across the network.
   4. Connection Max Idle Ms:
       Specifies the maximum number of milliseconds for an idle connection.
       After this period, if the producer sends to the broker, it will use a disconnected connection.
   5. Acks (Acknowledgements):
       Determines the acknowledgement behavior when a producer sends records. Three settings are possible:
           Acks = 0: Producers will not wait for any acknowledgement from the server.
           Acks = 1 (Default): The leader broker will write the record to its local log and respond without waiting for full acknowledgement from all followers. In this case, if the leader fails immediately after acknowledgement (before followers replicate), the record will be lost.
           Acks = -1: The leader will wait for the full set of in-sync replicas to acknowledge the record. This guarantees that the record will not be lost as long as at least one in-sync replica remains alive. This provides the strongest guarantee and is equivalent to acks=all.
   6. Compression Type:
       Used to compress the messages.
       The default value is "none".
       Supported types include gzip, snappy, lz4, and zstd.
       Compression is particularly useful for batches of data, and the efficiency of batching also affects the compression ratio.
   7. Max Request Size:
       Defines the maximum size of a request in bytes.
       This setting impacts the number of record batches the producer will send in a single request.
       It is used for sending large requests and also affects the cap on the maximum compressed record batch size .
   8. Batching:
       Producer Batching: The producer collects records together and sends them in a single batch. This approach aims to reduce network latency and CPU load, thereby improving overall performance.
       Batch Size Configuration: The size of a batch is determined by a configuration parameter called batch.size, with a default value of 16KB. Each partition will contain multiple records within a batch. Importantly, all records within a single batch will be sent to the same topic and partition.
       linger.ms: This parameter specifies a duration the producer will wait to allow more records to accumulate and be sent together in a batch, further optimizing the sending process.
       Memory Usage: Configuring larger batches may lead the producer to use more memory. There's also a concept of "pre-allocation" where a specific batch size is anticipated for additional records.
   9. Buffer Memory:
       Producers use buffer memory to facilitate batching records.
       Records ranging from 1MB to 2MB can be delivered to the server.
       If the buffer memory becomes full, the producer will block for a duration specified by max.block.ms until memory becomes available. This max.block.ms represents the maximum time the producer will wait.
       It is crucial to compare this max.block.ms setting with the total memory the producer is configured to use.
       It's noted that not all producer memory is exclusively used for batching; some additional memory is allocated for compression and insight requests.

   Producer Corner Cases in Kafka Tuning (Replica Management)

   1. Replica Fetchers: This setting determines the number of threads responsible for replicating data from leaders. It's crucial to have a sufficient number of replica fetchers to enable complete parallel replication if multiple threads are available.
   2. replica.fetch.max.bytes: This parameter dictates the maximum amount of data used to fetch from any partition in each fetch request. It is generally beneficial to increase this parameter.
   3. replica.socket.receive.buffer.bytes: The size of buffers can be increased, especially if more threads are available.
   4. Creating Replicas: Increasing the level of parallelism allows for data to be written in parallel, which automatically leads to an increase in throughput.
   5. num.io.threads: This parameter is determined by the amount of disk available in the cluster and directly influences the value for I/O threads .

### Consumer Configurations

   1. Key Deserializer: This refers to the deserializer class used for keys, which must implement the org.apache.kafka.common.serialization.Deserializer interface .
   2. Group ID: A unique string (group.id) identifies the consumer group to which a consumer belongs . This property is essential if the consumer utilizes group management technology, the offset commit API, or a topic-based offset management strategy .
   3. fetch.min.bytes: This parameter sets the minimum amount of data the server should return for a fetch request . If the available data is less than this threshold, the request will wait for more data to accumulate . This strategy reduces the number of requests to the broker . The request will block until fetch.min.bytes data is available or the fetch.max.wait.ms timeout expires . While this can cause fetches to wait for larger data amounts, it generally improves throughput at the cost of some additional latency .
   4. Heartbeat Interval: This defines the periodic interval at which heartbeats are sent to the consumer coordinator when using logical group management facilities . Heartbeats serve to ensure the consumer session remains active and facilitate rebalancing when consumers join or leave the group . The value for the heartbeat interval must be less than session.timeout.ms, typically not exceeding one-third of session.timeout.ms . Adjusting this can help control the expected time for normal rebalances .
   5. session.timeout.ms: This timeout is used to detect client failures within Kafka's group management facility. Clients send periodic heartbeats to signal their liveness. If the session times out, the consumer is removed by the brokers from the group, triggering a rebalance. The value for session.timeout.ms must fall between group.min.session.timeout.ms and group.max.session.timeout.ms.
   6. max.partition.fetch.bytes: This sets the maximum amount of data the server will return per partition. However, if the very first record batch is larger than this specified size, that first batch will still be returned to ensure continuous progress. The maximum fetch.batch.size accepted by brokers is determined by message.max.bytes.
   7. Max Bytes: This refers to the maximum amount of data the server should return for a fetch request. Records are filtered in batches by the consumer. Similar to max.partition.fetch.bytes, if the first record batch exceeds this limit, it will still be returned to ensure continuous progress.

   