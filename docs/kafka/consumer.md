## **Consumers**
Consumers are applications that read or consume data from the topics using the Consumer API .
Consumers can read data from the topic level (accessing all partitions of a topic) or from specific partitions .
Consumers are always associated with a consumer group .


*Illustrative Example*: A mobile news app that displays articles to users would be a consumer. If it's configured to show "sports news," it consumes messages from the sports_news topic.
    
**Consumer Groups**

A consumer group is a group of related consumers that perform a task .
Each message in a partition is consumed by only one consumer within a consumer group, ensuring load balancing and avoiding duplicate processing within that group. Multiple groups can consume the same message.

*Illustrative Example*: You might have a "mobile app news feed" consumer group and a "website news archive" consumer group. Both groups consume the same news articles, but within the "mobile app" group, if there are multiple instances of the app running, they will share the load of processing new articles.

Consumer groups in Apache Kafka have several key advantages:

1. **Load Balancing**: Consumer groups allow the messages from a topic's partitions to be divided among multiple consumers in the group. This effectively balances the load and allows for higher throughput.
2. **Fault Tolerance**: If a consumer in a group fails, the partitions it was consuming from are automatically reassigned to other consumers in the group, ensuring no messages are lost or left unprocessed.
3. **Scalability**: You can increase the processing speed by simply adding more consumers to a group. This makes it easy to scale your application according to the workload.
4. **Parallelism**: Since each consumer in a group reads from a unique set of partitions, messages can be processed in parallel, improving the overall speed and efficiency of data processing.
5. **Ordering Guarantee**: Within each partition, messages are consumed in order. As a single partition is consumed by only one consumer in the group, this preserves the order of messages as they were written into the partition.

**Consumer Configurations**

   1. **Key Deserializer**: This refers to the deserializer class used for keys, which must implement the org.apache.kafka.common.serialization.Deserializer interface .
   2. **Group ID**: A unique string (group.id) identifies the consumer group to which a consumer belongs . This property is essential if the consumer utilizes group management technology, the offset commit API, or a topic-based offset management strategy .
   3. **fetch.min.bytes**: This parameter sets the minimum amount of data the server should return for a fetch request . If the available data is less than this threshold, the request will wait for more data to accumulate . This strategy reduces the number of requests to the broker . The request will block until fetch.min.bytes data is available or the fetch.max.wait.ms timeout expires . While this can cause fetches to wait for larger data amounts, it generally improves throughput at the cost of some additional latency .
   4. **Heartbeat Interval**: This defines the periodic interval at which heartbeats are sent to the consumer coordinator when using logical group management facilities . Heartbeats serve to ensure the consumer session remains active and facilitate rebalancing when consumers join or leave the group . The value for the heartbeat interval must be less than session.timeout.ms, typically not exceeding one-third of session.timeout.ms . Adjusting this can help control the expected time for normal rebalances .
   5. **session.timeout.ms**: This timeout is used to detect client failures within Kafka's group management facility. Clients send periodic heartbeats to signal their liveness. If the session times out, the consumer is removed by the brokers from the group, triggering a rebalance. The value for session.timeout.ms must fall between group.min.session.timeout.ms and group.max.session.timeout.ms.
   6. **max.partition.fetch.bytes**: This sets the maximum amount of data the server will return per partition. However, if the very first record batch is larger than this specified size, that first batch will still be returned to ensure continuous progress. The maximum fetch.batch.size accepted by brokers is determined by message.max.bytes.
   7. **Max Bytes**: This refers to the maximum amount of data the server should return for a fetch request. Records are filtered in batches by the consumer. Similar to max.partition.fetch.bytes, if the first record batch exceeds this limit, it will still be returned to ensure continuous progress.

**When a consumer interacts with Kafka to consume messages**

   1. **Consumer Poll**: The consumer issues a Consumer.poll() request, which may retrieve a certain number of records (e.g., approximately 15 records) .
   2. **Consumer Commit**: After processing messages, the consumer calls Consumer.commit() to acknowledge that messages up to a certain offset (e.g., in P1, up to offset 5) have been successfully processed .

After the consumer receives messages from a poll request, a parallel process begins to manage offset commits. Offsets represent the position of the last consumed message in a partition. Committing an offset tells Kafka which messages have been successfully processed by a consumer.

This automatic commit mechanism is controlled by two key properties:

*   **`enable.auto.commit`**:
       By default, this property is set to `true` for Python consumer APIs.
       When `true`, the Kafka consumer will automatically commit offsets at regular intervals.
*   **`auto.commit.interval.ms`**:
       This property defines the time interval (in milliseconds) between automatic offset commits.
       The default value is 5,000 milliseconds (5 seconds).

    !!! Tip
        The commit timer starts after a polling request is completed and messages are received.

## **How Consumers in Consumer Group read messages?**

1. A single Kafka consumer can read from all partitions of a topic. This is often the case when you have only one consumer in a consumer group. 
2. However, when you have multiple consumers in a consumer group, the partitions of a topic are divided among the consumers. This allows Kafka to distribute the data across the consumers, enabling concurrent data processing and improving overall throughput.
3. It's also important to note that while a single consumer can read from multiple partitions, a single partition can only be read by one consumer from a specific consumer group at a time. This ensures that the order of the messages in the partition is maintained when being processed.


![Steps](4.png)

When a poll is complete, a parallel thread starts an "autocommit timer". This thread waits for the `auto.commit.interval.ms` duration to elapse. Once the configured time is over, the offset is committed to the `__consumer_offset` topic in Kafka. If an error occurs during message processing before the commit interval is over, the commit is interrupted.

In the main thread, while the auto-commit timer runs in parallel, the consumer processes the messages received from the broker.

1.  **Processing Records**: The consumer collects all records received in a poll response and begins processing individual messages one by one. This processing can involve various activities, such as writing messages to a database or performing business logic.
2.  **Continuous Polling**: Once all messages from a particular poll response are processed successfully, the consumer automatically makes another polling request to fetch the next set of messages. This creates a continuous loop of fetching and processing.

**Consumer Group** 

   1. **Consumer Group**: A consumer group is a logical entity within the Kafka ecosystem that primarily facilitates parallel processing and scalable message consumption for consumer clients .
       Every consumer must be associated with a consumer group .
       There is no duplication of messages among consumers within the same consumer group .
   2. **Consumer Group Rebalancing**: This is the process of re-distributing partitions among the consumers within a consumer group.

      Scenarios for Rebalancing: Rebalancing occurs in several situations:
           A consumer joins the consumer group.
           A consumer leaves the consumer group.
           New partitions are added to a topic, making them available for new consumers.
           Changes in connection states.

   3. **Group Coordinator**: In a Kafka cluster, one of the brokers is assigned the role of group coordinator to manage consumer groups.
       The group coordinator maintains and manages the list of consumer groups.
       It initiates a callback to communicate the new partition assignments to all consumers during rebalancing.
       Important Note: Consumers within a group undergoing rebalancing will be blocked from reading messages until the rebalance process is complete.
   4. **Group Leader**: The first consumer to join a consumer group is elected as the Group Leader.
       The Group Leader maintains a list of active members and selects the assignment strategy.
       The Group Leader is responsible for executing the rebalance process.
       Once the new assignment is determined, the Group Leader sends it to the group coordinator.
   5. **Consumer Joining a Group**: When a consumer starts:
       It sends a "Find Coordinator" request to locate the group coordinator for its group.
       It then initiates the rebalance protocol by sending a "Joining" request.
       Subsequently, members of the consumer group send a "SyncGroup" request to the coordinator.
       Each consumer also periodically sends a "Heartbeat" request to the coordinator to keep its session alive.


## **Rebalancing**
In Apache Kafka, rebalancing refers to the process of redistributing the partitions of topics across all consumers in a consumer group. Rebalancing ensures that all consumers in the group have an equal number of partitions to consume from, thus evenly distributing the load.

Rebalancing can be triggered by several events:

1. **Addition or removal of a consumer**: If a new consumer joins a consumer group, or an existing consumer leaves (or crashes), a rebalance is triggered to redistribute the partitions among the available consumers.
2. **Addition or removal of a topic's partition**: If a topic that a consumer group is consuming from has a partition added or removed, a rebalance will be triggered to ensure that the consumers in the group are consuming from the correct partitions.
3. **Consumer finishes consuming all messages in its partitions**: When a consumer has consumed all messages in its current list of partitions and commits the offset back to Kafka, a rebalance can be triggered to assign it new partitions to consume from.

While rebalancing ensures fair partition consumption across consumers, it's important to note that it can also cause some temporary disruption to the consuming process, as consumers may need to stop consuming during the rebalance. To minimize the impact, Kafka allows you to control when and how a consumer commits its offset, so you can ensure it happens at a point that minimizes any disruption from a rebalance.


## **Read strategies in Kafka**

In Apache Kafka, the consumer's position is referred to as the "offset". Kafka maintains the record of the current offset at the consumer level and provides control to the consumer to consume records from a position that suits their use case. This ability to control where to start reading records provides flexibility to the consumers. Here are the main reading strategies:

1. **Read From the Beginning**: If a consumer wants to read from the start of a topic, it can do so by setting the consumer property auto.offset.reset to earliest. This strategy is useful for use cases where you want to process all the data in the topic.
2. **Read From the End (Latest)**: If a consumer only cares about new messages and doesn't want to read the entire history of a topic, it can start reading from the end. This is done by setting auto.offset.reset to latest.
3. **Read From a Specific Offset**: If a consumer wants to read from a particular offset, it can do so using the seek() method on the KafkaConsumer object. This method changes the position of the consumer to the specified offset.
4. **Committing and Reading from Committed Offsets**: The consumer can commit offsets after it has processed messages. If the consumer dies and then restarts, it can continue processing from where it left off by reading the committed offset.


## **Manual Commit, At most once & Exactly Once**

**Message Processing Loop and Manual Offset Commit**

![Steps](3.png)

After receiving messages from a poll request, the consumer processes them in a continuous loop, and then explicitly commits its progress.

 1.  Collect Records: All records received in the poll response are collected by the consumer.
 2.  Individual Record Processing: The consumer then picks up and processes each individual record one by one. This processing might involve various operations, such as:
       Storing data in a database: Persisting the message content into a data store.
       Performing business logic: Executing specific application functions based on the message.
       Sending to another service: Forwarding the message to another part of your system.
 3.  Continuous Loop: If there are more records in the collected batch, the consumer loops back to process the next one until all records from that poll response are handled.
 4.  Manual Offset Commitment: Once all the messages received in that particular poll response have been successfully processed, the consumer program explicitly issues a command to commit the offset to the Kafka broker. This action updates Kafka's record of the consumer's progress, marking the messages as processed.
 5.  Return to Poll State: After the successful commit, the consumer then returns to the polling state, making another request for new messages, continuing the infinite loop of fetching, processing, and committing.

**Understanding "At-Least-Once" Processing with Manual Commits**

![Steps](1.png)

Even with manual offset commits, Kafka's guarantee remains at-least-once processing. This means that a message might be processed more than once, especially if an error occurs before the offset for that message (or batch) is committed.

Consider the following scenario:

1.  A consumer polls and receives a batch of 10 messages.
2.  The consumer successfully processes the first 3 messages.
3.  While attempting to process the 4th message, an error occurs (e.g., a database connection drops, or invalid data is encountered).
4.  Immediate Interruption: As soon as the error occurs, the processing flow is interrupted, and the consumer immediately reverts back to the poll step.
5.  No Offset Commit: Since not all 10 messages were successfully processed (specifically, the 4th message failed) and the manual commit step for the entire batch had not yet been reached, no offset was committed for the first 3 messages either.
6.  Reprocessing: When the consumer polls again, Kafka will send messages from the last committed offset. Since the offset for the previous batch was never committed, Kafka will re-send the same set of 10 messages.
7.  Consequently, the first 3 messages, which were already processed in the previous attempt, will be reprocessed.


**Message Processing Loop and Manual Offset Commitment for Exactly-Once**
![Steps](2.png)

After receiving messages from a poll request, the consumer processes them in a continuous loop. The key to the "exactly-once" strategy demonstrated is the immediate commitment of the offset after processing each single message.

1.  Iterate Records: The consumer iterates through each `message` object received from the `consumer.poll()` call (often simplified to `for message in consumer:`).
2.  Extract Message Properties: Important details like `message.value`, `message.key`, `message.topic`, `message.partition`, `message.offset`, and `message.timestamp` can be extracted from each `message` object.
3.  Process Individual Record: The consumer then performs its application logic (e.g., storing data in a database, executing business logic) using the message's content. The `print` statements in the demo code are considered the "processing engine" for this example.
4.  Manual Offset Commitment (Immediately After Each Message): As soon as a single message is successfully processed, the consumer program explicitly issues a command to commit the offset to the Kafka broker. This is the core mechanism ensuring that if the consumer crashes after processing a message but before a batch commit, that specific message won't be reprocessed.

       The `consumer.commit()` Method: This method takes a dictionary where keys are `TopicPartition` objects and values are `OffsetAndMetadata` objects.
           `TopicPartition`: Identifies the specific topic and partition. It's constructed using `message.topic` and `message.partition`.
           `OffsetAndMetadata`: Contains the offset to commit and optional metadata.
               Offset Value: The offset value provided for commit is `current_message_offset + 1`. This is because Kafka interprets a committed offset `X` as meaning messages up to `X-1` have been successfully processed, and the next message to send should be `X`.
               Metadata: You can pass additional metadata (e.g., `message.timestamp`).

```python
# Conceptual Python Code for Exactly-Once Processing (simplified)
for message in consumer:
    # 1. Extract message details
    print(f"Topic: {message.topic}, Partition: {message.partition}, "
          f"Offset: {message.offset}, Key: {message.key}, Value: {message.value}") #
    
    # 2. Process the message (e.g., save to DB, perform business logic)
    # This print statement is considered the "processing engine"
    print("Processing message:", message.value) 
    
    # 3. Prepare TopicPartition and OffsetAndMetadata for commit
    tp = TopicPartition(message.topic, message.partition)
    # Commit the next offset (current_offset + 1)
    offset_meta = OffsetAndMetadata(message.offset + 1, message.timestamp) 
    
    # 4. Create the dictionary for commit
    offsets_to_commit = {tp: offset_meta}
    
    # 5. Manually commit the offset for this single message
    consumer.commit(offsets_to_commit) #
    print(""  100) # Print stars to visually differentiate processed messages

```
5.  Return to Poll State: After successfully processing and committing the offset for a single message, the consumer continues the loop, ready to process the next message in the fetched batch or poll for new messages if the batch is exhausted.

This approach of committing after each message significantly reduces the window for reprocessing, making it align with the "exactly-once" claim by the source. If the consumer crashes after processing a message but before its specific offset is committed, that message could be re-processed. However, with per-message commits, this window is minimized to the time it takes to process and commit one message.


## **Why the One-Consumer-Per-Partition Rule?**

The central question addressed is: Why does Kafka not allow multiple consumers to consume messages from the same partition simultaneously?. This restriction is in place to prevent several critical issues related to data integrity and efficient processing.

**Problem 1: Load Balancing and Message Reprocessing**

 The primary reason for introducing consumer groups was to achieve load balancing and accelerate message processing. However, if multiple consumers were allowed to consume from the same partition, this goal would be undermined.

 Consider a scenario where a topic has a partition, say Partition 3, which contains messages arranged in segments with offsets (unique identifiers for messages within a partition).

 Scenario: Suppose Consumer 4 and Consumer 5 are both consuming from Partition 3.
    
 The Issue:

  1. Consumer 4 processes messages from `offset 0` to `offset 4096`. Consumer 4 knows it has consumed up to `offset 4096` and expects to pull from `offset 4097` next time.
  2. However, Consumer 5, running in parallel, does not know what Consumer 4 has already processed. Consumer 5 might also attempt to consume messages starting from `offset 0`.
  3. Result: Both Consumer 4 and Consumer 5 would end up processing the same range of messages (`offset 0` to `offset 4096`).
    
 Consequence: This leads to reprocessing of the same messages multiple times, which is not genuine parallel processing or load balancing. True parallel processing involves different workers handling different parts of a larger task, not the same part repeatedly. The consumer group concept was designed for multiple consumers to process different chunks of messages.

**Problem 2: Violation of Message Order Guarantees**

 Kafka guarantees message ordering only within a single partition. This means that messages sent to a specific partition will always be processed by consumers in the order they were written, based on their offsets. This guarantee is crucial for many applications, especially those where the sequence of events is vital.

 Consider a banking domain example:
 
 1. A customer first adds money to their account (Event A) and then withdraws money (Event B).
 2. It's essential that the addition of money is processed *before* the deduction to maintain correct account balance and display the correct sequence of events in the application.
 3. To ensure all events related to a specific account go to the same partition, a common strategy is to use hashing based on the account number (e.g., `account_number % total_partitions`). This ensures that if Event A goes to Partition 2, Event B (for the same account) will also go to Partition 2, and Event B will have a higher offset than Event A.

 The Issue if multiple consumers were allowed on one partition:

 1. Suppose Consumer 4 and Consumer 5 are both consuming from the same partition, and you somehow try to split the offset ranges (e.g., one consumes one range, the other consumes another).
 2. If they consume messages in parallel, the order of execution cannot be guaranteed.
 3. Consumer 5 might process the "deduction of money" event first, update the database, and display it in the front-end application. Simultaneously, Consumer 4 might process the "addition of money" event later.
 4. Consequence: This would result in a poor customer experience, as the transactions would not be displayed in the order they occurred. Kafka's design prevents this violation of crucial message ordering.

 Therefore, even if the reprocessing issue were somehow overcome by splitting offset ranges, the critical guarantee of message ordering within a partition would be lost if multiple consumers processed it concurrently.