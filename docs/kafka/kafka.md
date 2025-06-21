# Apache Kafka Documentation

Welcome to the Apache Kafka Documentation – a comprehensive guide to understanding Kafka, a distributed streaming platform that enables building real-time data pipelines and streaming applications.

---
## What is Apache Kafka?

Apache Kafka is a distributed streaming platform that was developed by LinkedIn in 2010 and later donated to the Apache Software Foundation. It's designed to handle high-throughput, fault-tolerant, and real-time data streaming.

Key characteristics:
- Distributed: Runs as a cluster of servers
- Scalable: Can handle petabytes of data
- Fault-tolerant: Replicates data across multiple servers
- High-throughput: Can handle millions of messages per second

---
## Core Concepts

### 1. Messaging Systems

Kafka supports two fundamental messaging patterns:

#### Point-to-Point Messaging
- Messages are consumed by only one receiver
- No dependency on receiver availability
- Example: Email to a single recipient

#### Publish-Subscribe Messaging
- Messages are persisted in the system
- Can be consumed by multiple consumers
- Consumers must actively consume messages
- Example: Blog posts read by multiple subscribers

### 2. Key Components

#### Topics
- Logical feed of messages
- Unique identifier for categorization
- Example: sports_news, finance_updates

#### Partitions
- Topics are split into partitions
- Messages within partitions are ordered and immutable
- Each message has a unique offset
- Example: sports_news topic with partitions for different sports

#### Replication
- Backup copies of partitions
- Ensures fault tolerance
- Prevents data loss
- Example: If server hosting P0 fails, replica takes over

---
## Architecture

### 1. Kafka Participants

#### Producers
- Applications that publish data to topics
- Can write to specific partitions or let Kafka distribute
- Use Producer API for sending data

#### Consumers
- Applications that read data from topics
- Always part of a consumer group
- Use Consumer API for reading data

#### Consumer Groups
- Logical grouping of related consumers
- Ensures load balancing
- Prevents duplicate processing within group
- Multiple groups can consume same message

#### Zookeeper
- Manages Kafka cluster
- Stores metadata
- Handles leader election
- Coordinates cluster operations

### 2. Fault Tolerance

Kafka provides:
- Automatic recovery from node failures
- High availability
- Data replication
- Zero data loss guarantees

---
## Configuration

### Producer Configurations

1. Bootstrap Servers
   - Host/port for cluster connection
   - Initial connection point

2. Client ID
   - Request tracking
   - Server-side logging

3. Serializers
   - Convert objects to bytes
   - Required for network transmission

4. Acknowledgments (acks)
   - 0: No acknowledgment
   - 1: Leader acknowledgment
   - -1: Full replica acknowledgment

5. Batching
   - Reduces network latency
   - Default batch size: 16KB
   - Configurable with linger.ms

### Consumer Configurations

1. Group ID
   - Unique identifier for consumer group
   - Required for group management

2. Deserializers
   - Convert bytes back to objects
   - Must match producer serializers

3. Fetch Settings
   - fetch.min.bytes
   - max.partition.fetch.bytes
   - fetch.max.wait.ms

4. Session Management
   - heartbeat.interval.ms
   - session.timeout.ms

---
## Performance Tuning

### Producer Optimization
- Batch size configuration
- Compression settings
- Buffer memory management
- Replica management

### Consumer Optimization
- Fetch size tuning
- Consumer group balancing
- Partition assignment strategy
- Offset management

---
## Best Practices

1. Topic Design
   - Choose appropriate partition count
   - Set replication factor
   - Configure retention policies

2. Producer Guidelines
   - Use appropriate acks level
   - Implement retry logic
   - Monitor producer metrics

3. Consumer Guidelines
   - Handle rebalancing gracefully
   - Implement proper error handling
   - Monitor consumer lag

4. Cluster Management
   - Monitor broker health
   - Track partition leaders
   - Manage consumer groups

---
## Common Use Cases

1. Messaging
   - High-throughput messaging
   - Decoupling systems

2. Activity Tracking
   - User behavior analysis
   - Real-time monitoring

3. Metrics Collection
   - System monitoring
   - Performance tracking

4. Log Aggregation
   - Centralized logging
   - Real-time log processing

---
## References

[1] Apache Kafka Documentation
[2] Kafka: The Definitive Guide
[3] Kafka Internals
[4] Kafka Performance Tuning Guide

### Kafka Overview

   Development and Purpose: Kafka was developed in 2010 and is described as a distributed message streaming platform [1]. It was initially developed by LinkedIn for internal tasks and was later donated to the Apache open-source project [1]. Its primary purpose is to allow different applications or nodes to transfer data efficiently [1].

### Messaging Systems

A messaging system is fundamentally responsible for transferring data between applications or nodes, whether the data is transmitted immediately or stored [1]. There are two main types:

   Point-to-Point Messaging: In this model, a message is consumed by a maximum of one receiver only [1]. There is no dependency on the receiver to ensure the message is received [1].
       Illustrative Example: Imagine sending an email to a single recipient. Once that recipient reads it, it's typically considered processed for that email.
   Publish-Subscribe Messaging: In contrast, messages in this system are persisted in a particular message system and can be consumed by any number of consumers [1]. There is a dependency that consumers actively consume the message [1].
       Illustrative Example: Think of a blog where posts (messages) are published. Many different subscribers (consumers) can read the same post, and the post remains available even after some have read it. Kafka primarily uses this model.

### Key Kafka Concepts

1.  Topics
       A topic is a stream of messages belonging to a particular category [1].
       It acts as a logical feed where all batch records (messages) are published [1].
       Each topic has a unique identifier to distinguish it [1].
       Illustrative Example: In a news application, you might have topics like sports_news, finance_updates, or weather_alerts. All messages related to sports news would go into the sports_news topic.

2.  Partitions
       Topics are split into partitions [1].
       All messages within a specific partition are ordered and immutable (meaning they cannot be changed after being written) [1].
       Each message within a partition has a unique ID called an Offset [1]. This offset denotes the message's position within that specific partition.
       Illustrative Example: If your sports_news topic has three partitions (P0, P1, P2), articles related to football might go to P0, basketball to P1, and tennis to P2. Within P0, all football articles will appear in the exact order they were published, each with its unique offset.

3.  Replication
       Replicas are essentially backups of partitions [1].
       They are not directly read as raw data [1].
       Their primary purpose is to prevent data loss and provide fault tolerance [1]. If the server hosting an active partition fails, a replica can take over.
       Illustrative Example: If the server hosting Partition P0 of sports_news crashes, a replica of P0 on another server immediately takes over, ensuring that no sports news articles are lost and the news feed remains continuous.

### Kafka Fault Tolerance

   Kafka is designed as a fault-tolerant messaging system that ensures communication between producers and consumers using message board topics [1].
   It is highly available and resilient to node failures, supporting automatic recovery [1].

### Kafka Participants

1.  Producers
       Producers are applications that write or publish data to the topics within a Kafka cluster [2].
       They use the Producer API to send data [2].
       Producers can choose to write data either at the topic level (letting Kafka distribute it across partitions) or to specific partitions of a topic [2].
       Illustrative Example: A journalist writing a new article would be a producer, publishing the article to the news topic.

2.  Consumers
       Consumers are applications that read or consume data from the topics using the Consumer API [2].
       Consumers can read data from the topic level (accessing all partitions of a topic) or from specific partitions [2].
       Consumers are always associated with a consumer group [2].
       Illustrative Example: A mobile news app that displays articles to users would be a consumer. If it's configured to show "sports news," it consumes messages from the sports_news topic.

3.  Consumer Groups
       A consumer group is a group of related consumers that perform a task [2].
       Each message in a partition is consumed by only one consumer within a consumer group, ensuring load balancing and avoiding duplicate processing within that group. Multiple groups can consume the same message.
       Illustrative Example: You might have a "mobile app news feed" consumer group and a "website news archive" consumer group. Both groups consume the same news articles, but within the "mobile app" group, if there are multiple instances of the app running, they will share the load of processing new articles.

4.  Zookeeper
       Zookeeper is a critical component used to monitor Kafka clusters and coordinate with them [2].
       It stores all the metadata information related to Kafka clusters, including the status of replicas and leaders [2].
       This metadata is crucial for configuration information, cluster health, and leader election within the cluster [2].
       Zookeeper nodes working together to manage distributed systems are known as a Zookeeper Cluster or Zookeeper Ensemble [2].
       Illustrative Example: If a Kafka server hosting a partition's leader fails, Zookeeper quickly identifies this and coordinates the election of a new leader from the available replicas, ensuring continuous operation.

### Features of Kafka

Kafka boasts several key features:

   Scalable: It supports horizontal scaling by allowing you to add new brokers (servers) to the clusters [2].
   Fault-tolerant: It can handle failures effectively due to its distributed nature and replication mechanisms [2].
   Durable: Kafka uses a "distributed commit log," which means messages are persisted on disk [2]. This ensures data is not lost even if a server goes down.
   Fast: Designed to be as fast as possible [2].
   Performance: Achieves high throughput for both publishing (producers) and subscribing (consumers) [2].
   No data loss: Guarantees that messages are not lost once they are committed to Kafka [2].
   Zero down time: Designed for continuous operation without interruption [2].
   Reliability: Provides reliable message delivery [2].

### Zookeeper Configuration and Internal States

Zookeeper uses specific parameters and maintains various internal states to manage Kafka.

Zookeeper Configuration Concepts [3]:

   initLimit: Defines the time in milliseconds that a Zookeeper follower node can take to initially connect to a leader [3]. For example, 5  2 seconds means 10 seconds. If a node doesn't get in sync within this limit, it's considered out of time [3].
   syncLimit: Defines the time in milliseconds that a Zookeeper follower can be out of sync with the leader [3]. For example, 10  2 seconds means 20 seconds. If a node doesn't sync within this limit, it's considered out of time [3].
   clientPort: This is the port number (e.g., 2181) where Zookeeper clients connect [3]. It refers to the data directory used to store client node server details [3].
   maxClientCnxns: This parameter sets the maximum number of client connections that a single Zookeeper server can handle at once [3].
   server.1, server.2, server.3: These entries define the server IDs and their IP addresses/ports within the Zookeeper ensemble (e.g., server.1: 2888:3888) [3]. These are crucial for leader election among the Zookeeper servers [3].

Kafka Partition States (as managed by Zookeeper) [3]:

   New Nonexistent Partition: This state indicates that a partition was either never created or was created and then subsequently deleted [3].
   Nonexistent Partition (after deletion): This state specifically means the partition was deleted [3].
   Offline Partition: A partition is in this state when it should have replicas assigned but has no leader elected [3].
   Online Partition: A partition enters this state when a leader is successfully elected for it [3]. If all leader election processes are successful, the partition transitions from Offline Partition to Online Partition [3].

Kafka Replica States (as managed by Zookeeper) [3]:

   New Replica: Replicas are created during topic creation or partition reassignment [3]. In this state, a replica can only receive follower state change requests [3].
   Online Replica: A replica is considered Online when it is started and has assigned replicas for its partition [3]. In this state, it can either become a leader or become a follower based on state change requests [3].
   Offline Replica: If a replica dies (becomes unavailable), it moves to this state [3]. This typically happens when the replica is down [3].
   Nonexistent Replica: If a replica is deleted, it moves into this state [3].

---



### Kafka Cluster & Partition Reassignment

   Kafka Cluster Controller: In a Kafka cluster, one of the brokers is designated as the controller [1]. This controller is responsible for managing the states of partitions and replicas and for performing administrative tasks such as reassigning partitions [1].
   Partition Growth: It is important to note that the partition count of a Kafka topic can always be increased, but never decreased. This is because reducing partitions could lead to data loss [1].
   Partition Reassignment Use Cases: Partition reassignment is used in several scenarios [1]:
       Moving a partition across different brokers [1].
       Rebalancing the replicas of a partition to a specific set of brokers [1].
       Increasing the replication factor of a topic [1].

### Internals: Producer Sends Messages

When a producer sends messages in Kafka, the process involves [1]:
   Sending Messages: A producer might send a batch of messages, for example, 10 messages with IDs {0, 1, 2, ..., 9} [1].
   Partitioning: Messages are sent to different partitions (e.g., P0, P1, P2), potentially including a key, a NULL value (if the key is unused), and the payload [1].
   Offsets: Within each partition, messages are assigned offsets. For example, P0 might have messages with offsets (0,1,2,3,4), P1 with (0,1,2,3,4,5), and P2 with (0,1,2,3,4,5,6) [1].
       Effect of Offsets: Offsets help in finding the location of messages and are always significant when reading messages [1].

### Offsets

Offsets represent the position of each message within a partition and are uniquely identifiable, ever-increasing integers [2]. There are three main variations of offsets [2]:
   Log End Offset: This refers to the offset of the last message written to any given partition [2].
   Current Offset: This is a pointer to the last record that Kafka has already sent to the consumer in the current poll [2].
   Committed Offset: This indicates the offset of a message that a consumer has successfully consumed [2].
   Relationship: The committed offset is typically less than the current offset [2].

### Internals: Consumer Consumes Messages

When a consumer interacts with Kafka to consume messages [2]:
   Consumer Poll: The consumer issues a Consumer.poll() request, which may retrieve a certain number of records (e.g., approximately 15 records) [2].
   Consumer Commit: After processing messages, the consumer calls Consumer.commit() to acknowledge that messages up to a certain offset (e.g., in P1, up to offset 5) have been successfully processed [2].

### Consumer Group & Rebalancing

   Consumer Group: A consumer group is a logical entity within the Kafka ecosystem that primarily facilitates parallel processing and scalable message consumption for consumer clients [2].
       Every consumer must be associated with a consumer group [2].
       There is no duplication of messages among consumers within the same consumer group [2].
   Consumer Group Rebalancing: This is the process of re-distributing partitions among the consumers within a consumer group [3].
       Scenarios for Rebalancing: Rebalancing occurs in several situations [3]:
           A consumer joins the consumer group [3].
           A consumer leaves the consumer group [3].
           New partitions are added to a topic, making them available for new consumers [3].
           Changes in connection states [3].
   Group Coordinator: In a Kafka cluster, one of the brokers is assigned the role of group coordinator to manage consumer groups [3].
       The group coordinator maintains and manages the list of consumer groups [3].
       It initiates a callback to communicate the new partition assignments to all consumers during rebalancing [3].
       Important Note: Consumers within a group undergoing rebalancing will be blocked from reading messages until the rebalance process is complete [3].
   Group Leader: The first consumer to join a consumer group is elected as the Group Leader [3].
       The Group Leader maintains a list of active members and selects the assignment strategy [3].
       The Group Leader is responsible for executing the rebalance process [3].
       Once the new assignment is determined, the Group Leader sends it to the group coordinator [3].
   Consumer Joining a Group: When a consumer starts [3]:
       It sends a "Find Coordinator" request to locate the group coordinator for its group [3].
       It then initiates the rebalance protocol by sending a "Joining" request [3].
       Subsequently, members of the consumer group send a "SyncGroup" request to the coordinator [3].
       Each consumer also periodically sends a "Heartbeat" request to the coordinator to keep its session alive [3].

### Producer Configurations

When configuring a Kafka producer, several important settings are available [4]:

   1. Bootstrap Servers:
       Used to connect to the Kafka Cluster [4].
       This specifies the host/port for establishing the initial connection [4].
   2. Client ID:
       Used to track requests and is mainly for debugging purposes [4].
       Primarily used for server-side logging [4].
   3. Key Serializer (and Value Serializer):
       Converts the key/value into a stream of bytes [4].
       Kafka producers send objects as a stream of bytes, and this setting is used to persist and transmit the object across the network [4].
   4. Connection Max Idle Ms:
       Specifies the maximum number of milliseconds for an idle connection [4].
       After this period, if the producer sends to the broker, it will use a disconnected connection [4].
   5. Acks (Acknowledgements):
       Determines the acknowledgement behavior when a producer sends records [4]. Three settings are possible [4]:
           Acks = 0: Producers will not wait for any acknowledgement from the server [4].
           Acks = 1 (Default): The leader broker will write the record to its local log and respond without waiting for full acknowledgement from all followers [4]. In this case, if the leader fails immediately after acknowledgement (before followers replicate), the record will be lost [4].
           Acks = -1: The leader will wait for the full set of in-sync replicas to acknowledge the record [4]. This guarantees that the record will not be lost as long as at least one in-sync replica remains alive [4]. This provides the strongest guarantee and is equivalent to acks=all [4].
   Compression Type:
       Used to compress the messages [4].
       The default value is "none" [4].
       Supported types include gzip, snappy, lz4, and zstd [4].
       Compression is particularly useful for batches of data, and the efficiency of batching also affects the compression ratio [4].
   Max Request Size:
       Defines the maximum size of a request in bytes [4].
       This setting impacts the number of record batches the producer will send in a single request [4].
       It is used for sending large requests and also affects the cap on the maximum compressed record batch size [4].


   Batching [1]
       Producer Batching: The producer collects records together and sends them in a single batch [1]. This approach aims to reduce network latency and CPU load, thereby improving overall performance [1].
       Batch Size Configuration: The size of a batch is determined by a configuration parameter called batch.size, with a default value of 16KB [1]. Each partition will contain multiple records within a batch [1]. Importantly, all records within a single batch will be sent to the same topic and partition [1].
       linger.ms: This parameter specifies a duration the producer will wait to allow more records to accumulate and be sent together in a batch, further optimizing the sending process [1].
       Memory Usage: Configuring larger batches may lead the producer to use more memory [1]. There's also a concept of "pre-allocation" where a specific batch size is anticipated for additional records [1].

   Buffer Memory [1]
       Producers use buffer memory to facilitate batching records [1].
       Records ranging from 1MB to 2MB can be delivered to the server [1].
       If the buffer memory becomes full, the producer will block for a duration specified by max.block.ms until memory becomes available [1]. This max.block.ms represents the maximum time the producer will wait [1].
       It is crucial to compare this max.block.ms setting with the total memory the producer is configured to use [1].
       It's noted that not all producer memory is exclusively used for batching; some additional memory is allocated for compression and insight requests [1].

   Consumer Configurations [2, 3]
       Key Deserializer: This refers to the deserializer class used for keys, which must implement the org.apache.kafka.common.serialization.Deserializer interface [2].
       Group ID: A unique string (group.id) identifies the consumer group to which a consumer belongs [2]. This property is essential if the consumer utilizes group management technology, the offset commit API, or a topic-based offset management strategy [2].
       fetch.min.bytes: This parameter sets the minimum amount of data the server should return for a fetch request [2]. If the available data is less than this threshold, the request will wait for more data to accumulate [2]. This strategy reduces the number of requests to the broker [2]. The request will block until fetch.min.bytes data is available or the fetch.max.wait.ms timeout expires [2]. While this can cause fetches to wait for larger data amounts, it generally improves throughput at the cost of some additional latency [2].
       Heartbeat Interval: This defines the periodic interval at which heartbeats are sent to the consumer coordinator when using logical group management facilities [2]. Heartbeats serve to ensure the consumer session remains active and facilitate rebalancing when consumers join or leave the group [2]. The value for the heartbeat interval must be less than session.timeout.ms, typically not exceeding one-third of session.timeout.ms [2]. Adjusting this can help control the expected time for normal rebalances [2].
       session.timeout.ms: This timeout is used to detect client failures within Kafka's group management facility [3]. Clients send periodic heartbeats to signal their liveness [3]. If the session times out, the consumer is removed by the brokers from the group, triggering a rebalance [3]. The value for session.timeout.ms must fall between group.min.session.timeout.ms and group.max.session.timeout.ms [3].
       max.partition.fetch.bytes: This sets the maximum amount of data the server will return per partition [3]. However, if the very first record batch is larger than this specified size, that first batch will still be returned to ensure continuous progress [3]. The maximum fetch.batch.size accepted by brokers is determined by message.max.bytes [3].
       Max Bytes: This refers to the maximum amount of data the server should return for a fetch request [3]. Records are filtered in batches by the consumer [3]. Similar to max.partition.fetch.bytes, if the first record batch exceeds this limit, it will still be returned to ensure continuous progress [3].

   Producer Corner Cases in Kafka Tuning (Replica Management) [4]
       Replica Fetchers: This setting determines the number of threads responsible for replicating data from leaders [4]. It's crucial to have a sufficient number of replica fetchers to enable complete parallel replication if multiple threads are available [4].
       replica.fetch.max.bytes: This parameter dictates the maximum amount of data used to fetch from any partition in each fetch request [4]. It is generally beneficial to increase this parameter [4].
       replica.socket.receive.buffer.bytes: The size of buffers can be increased, especially if more threads are available [4].
       Creating Replicas: Increasing the level of parallelism allows for data to be written in parallel, which automatically leads to an increase in throughput [4].
       num.io.threads: This parameter is determined by the amount of disk available in the cluster and directly influences the value for I/O threads [4].


        