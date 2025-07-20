

Producers are applications that write or publish data to the topics within a Kafka cluster .
They use the Producer API to send data .
Producers can choose to write data either at the topic level (letting Kafka distribute it across partitions) or to specific partitions of a topic.


![Steps](kafkaproducer.svg)

Illustrative Example: A journalist writing a new article would be a producer, publishing the article to the news topic.

Partitions play a crucial role in Kafka's functionality and scalability. 

1. **Parallelism**: Partitions enable parallelism. Since each partition can be placed on a separate machine (broker), a topic can handle an amount of data that exceeds a single server's capacity. This allows producers and consumers to read and write data to a topic concurrently, thus increasing throughput.

2. **Ordering**: Kafka guarantees that messages within a single partition will be kept in the exact order they were produced. However, if order is important across partitions, additional design considerations are needed.

3. **Replication**: Partitions of a topic can be replicated across multiple brokers based on the topic's replication factor. This increases data reliability and availability.


4. **Failover**: In case of a broker failure, the leadership of the partitions owned by that broker will be automatically taken over by another broker, which has the replica of these partitions.

5. **Consumer Groups**: Each partition can be consumed by one consumer within a consumer group at a time. If more than one consumer is needed to read data from a topic simultaneously, the topic needs to have more than one partition.

6. **Offset**: Every message in a partition is assigned a unique (per partition) and sequential ID called an offset. Consumers use this offset to keep track of their position in the partition.

## **When a producer sends messages in Kafka, the process involves**:

   1. **Sending Messages**: A producer might send a batch of messages, for example, 10 messages with IDs {0, 1, 2, ..., 9}.
   Partitioning: Messages are sent to different partitions (e.g., P0, P1, P2), potentially including a key, a NULL value (if the key is unused), and the payload.
   2. **Offsets**: Within each partition, messages are assigned offsets. For example, P0 might have messages with offsets (0,1,2,3,4), P1 with (0,1,2,3,4,5), and P2 with (0,1,2,3,4,5,6).
   3. **Effect of Offsets**: Offsets help in finding the location of messages and are always significant when reading messages.
 
## **Producer Configurations**

When configuring a Kafka producer, several important settings are available:

   1. **Bootstrap Servers**:
       Used to connect to the Kafka Cluster.
       This specifies the host/port for establishing the initial connection.
   2. **Client ID**:
       Used to track requests and is mainly for debugging purposes.
       Primarily used for server-side logging.
   3. **Key Serializer (and Value Serializer)**:
       Converts the key/value into a stream of bytes.
       Kafka producers send objects as a stream of bytes, and this setting is used to persist and transmit the object across the network.
   4. **Connection Max Idle Ms**:
       Specifies the maximum number of milliseconds for an idle connection.
       After this period, if the producer sends to the broker, it will use a disconnected connection.
   5. **Acks (Acknowledgements)**:
       Determines the acknowledgement behavior when a producer sends records. 
       Three settings are possible:
       
       Acks = 0: Producers will not wait for any acknowledgement from the server.
       
       Acks = 1 (Default): The leader broker will write the record to its local log and respond without waiting for full acknowledgement from all followers. In this case, if the leader fails immediately after acknowledgement (before followers replicate), the record will be lost.
       
       Acks = -1: The leader will wait for the full set of in-sync replicas to acknowledge the record. This guarantees that the record will not be lost as long as at least one in-sync replica remains alive. This provides the strongest guarantee and is equivalent to acks=all.

   6. **Compression Type**:
       Used to compress the messages.
       The default value is "none".
       Supported types include gzip, snappy, lz4, and zstd.
       Compression is particularly useful for batches of data, and the efficiency of batching also affects the compression ratio.
   7. **Max Request Size**:
       Defines the maximum size of a request in bytes.
       This setting impacts the number of record batches the producer will send in a single request.
       It is used for sending large requests and also affects the cap on the maximum compressed record batch size .
   8. **Batching**:
       Producer Batching: The producer collects records together and sends them in a single batch. This approach aims to reduce network latency and CPU load, thereby improving overall performance.
       
       **Batch Size Configuration**: The size of a batch is determined by a configuration parameter called batch.size, with a default value of 16KB. Each partition will contain multiple records within a batch. Importantly, all records within a single batch will be sent to the same topic and partition.
       
       **linger.ms**: This parameter specifies a duration the producer will wait to allow more records to accumulate and be sent together in a batch, further optimizing the sending process.
       Memory Usage: Configuring larger batches may lead the producer to use more memory. There's also a concept of "pre-allocation" where a specific batch size is anticipated for additional records.
   
   9. **Buffer Memory**:
       Producers use buffer memory to facilitate batching records.
       Records ranging from 1MB to 2MB can be delivered to the server.
       If the buffer memory becomes full, the producer will block for a duration specified by max.block.ms until memory becomes available. This max.block.ms represents the maximum time the producer will wait.
       It is crucial to compare this max.block.ms setting with the total memory the producer is configured to use.
       It's noted that not all producer memory is exclusively used for batching; some additional memory is allocated for compression and insight requests.

## **Producer Corner Cases in Kafka Tuning (Replica Management)**

   1. **Replica Fetchers**: This setting determines the number of threads responsible for replicating data from leaders. It's crucial to have a sufficient number of replica fetchers to enable complete parallel replication if multiple threads are available.
   2. **replica.fetch.max.bytes**: This parameter dictates the maximum amount of data used to fetch from any partition in each fetch request. It is generally beneficial to increase this parameter.
   3. **replica.socket.receive.buffer.bytes**: The size of buffers can be increased, especially if more threads are available.
   4. **Creating Replicas**: Increasing the level of parallelism allows for data to be written in parallel, which automatically leads to an increase in throughput.
   5. **num.io.threads**: This parameter is determined by the amount of disk available in the cluster and directly influences the value for I/O threads .
