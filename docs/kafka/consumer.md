
When a consumer interacts with Kafka to consume messages :

   1. Consumer Poll: The consumer issues a Consumer.poll() request, which may retrieve a certain number of records (e.g., approximately 15 records) .
   3. Consumer Commit: After processing messages, the consumer calls Consumer.commit() to acknowledge that messages up to a certain offset (e.g., in P1, up to offset 5) have been successfully processed .

### Consumer Group 

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


### Rebalancing
In Apache Kafka, rebalancing refers to the process of redistributing the partitions of topics across all consumers in a consumer group. Rebalancing ensures that all consumers in the group have an equal number of partitions to consume from, thus evenly distributing the load.

Rebalancing can be triggered by several events:

1. Addition or removal of a consumer: If a new consumer joins a consumer group, or an existing consumer leaves (or crashes), a rebalance is triggered to redistribute the partitions among the available consumers.
2. Addition or removal of a topic's partition: If a topic that a consumer group is consuming from has a partition added or removed, a rebalance will be triggered to ensure that the consumers in the group are consuming from the correct partitions.
3. Consumer finishes consuming all messages in its partitions: When a consumer has consumed all messages in its current list of partitions and commits the offset back to Kafka, a rebalance can be triggered to assign it new partitions to consume from.

While rebalancing ensures fair partition consumption across consumers, it's important to note that it can also cause some temporary disruption to the consuming process, as consumers may need to stop consuming during the rebalance. To minimize the impact, Kafka allows you to control when and how a consumer commits its offset, so you can ensure it happens at a point that minimizes any disruption from a rebalance.


### Read strategies in Kafka:

In Apache Kafka, the consumer's position is referred to as the "offset". Kafka maintains the record of the current offset at the consumer level and provides control to the consumer to consume records from a position that suits their use case. This ability to control where to start reading records provides flexibility to the consumers. Here are the main reading strategies:

1. Read From the Beginning: If a consumer wants to read from the start of a topic, it can do so by setting the consumer property auto.offset.reset to earliest. This strategy is useful for use cases where you want to process all the data in the topic.
2. Read From the End (Latest): If a consumer only cares about new messages and doesn't want to read the entire history of a topic, it can start reading from the end. This is done by setting auto.offset.reset to latest.
3. Read From a Specific Offset: If a consumer wants to read from a particular offset, it can do so using the seek() method on the KafkaConsumer object. This method changes the position of the consumer to the specified offset.
4. Committing and Reading from Committed Offsets: The consumer can commit offsets after it has processed messages. If the consumer dies and then restarts, it can continue processing from where it left off by reading the committed offset.


### Consumer Configurations

   1. Key Deserializer: This refers to the deserializer class used for keys, which must implement the org.apache.kafka.common.serialization.Deserializer interface .
   2. Group ID: A unique string (group.id) identifies the consumer group to which a consumer belongs . This property is essential if the consumer utilizes group management technology, the offset commit API, or a topic-based offset management strategy .
   3. fetch.min.bytes: This parameter sets the minimum amount of data the server should return for a fetch request . If the available data is less than this threshold, the request will wait for more data to accumulate . This strategy reduces the number of requests to the broker . The request will block until fetch.min.bytes data is available or the fetch.max.wait.ms timeout expires . While this can cause fetches to wait for larger data amounts, it generally improves throughput at the cost of some additional latency .
   4. Heartbeat Interval: This defines the periodic interval at which heartbeats are sent to the consumer coordinator when using logical group management facilities . Heartbeats serve to ensure the consumer session remains active and facilitate rebalancing when consumers join or leave the group . The value for the heartbeat interval must be less than session.timeout.ms, typically not exceeding one-third of session.timeout.ms . Adjusting this can help control the expected time for normal rebalances .
   5. session.timeout.ms: This timeout is used to detect client failures within Kafka's group management facility. Clients send periodic heartbeats to signal their liveness. If the session times out, the consumer is removed by the brokers from the group, triggering a rebalance. The value for session.timeout.ms must fall between group.min.session.timeout.ms and group.max.session.timeout.ms.
   6. max.partition.fetch.bytes: This sets the maximum amount of data the server will return per partition. However, if the very first record batch is larger than this specified size, that first batch will still be returned to ensure continuous progress. The maximum fetch.batch.size accepted by brokers is determined by message.max.bytes.
   7. Max Bytes: This refers to the maximum amount of data the server should return for a fetch request. Records are filtered in batches by the consumer. Similar to max.partition.fetch.bytes, if the first record batch exceeds this limit, it will still be returned to ensure continuous progress.
