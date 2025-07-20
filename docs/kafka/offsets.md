
##  **Partitions**

![Steps](partition.svg)

Topics are split into partitions.
All messages within a specific partition are ordered and immutable (meaning they cannot be changed after being written).
Each message within a partition has a unique ID called an Offset. This offset denotes the message's position within that specific partition.
Illustrative Example: If your sports_news topic has three partitions (P0, P1, P2), articles related to football might go to P0, basketball to P1, and tennis to P2. Within P0, all football articles will appear in the exact order they were published, each with its unique offset.

##  **Replication**

![Steps](replicator.svg)

Replicas are essentially backups of partitions.
They are not directly read as raw data.
Their primary purpose is to prevent data loss and provide fault tolerance. If the server hosting an active partition fails, a replica can take over.
Illustrative Example: If the server hosting Partition P0 of sports_news crashes, a replica of P0 on another server immediately takes over, ensuring that no sports news articles are lost and the news feed remains continuous.

## **Offsets**
Offsets represent the position of each message within a partition and are uniquely identifiable, ever-increasing integers . There are three main variations of offsets :

   1. **Log End Offset**: This refers to the offset of the last message written to any given partition .
   2. **Current Offset**: This is a pointer to the last record that Kafka has already sent to the consumer in the current poll .
   3. **Committed Offset**: This indicates the offset of a message that a consumer has successfully consumed .
   4. **Relationship**: The committed offset is typically less than the current offset .

In Apache Kafka, consumer offset management – that is, tracking what messages have been consumed – is handled by Kafka itself.

When a consumer in a consumer group reads a message from a partition, it commits the offset of that message back to Kafka. This allows Kafka to keep track of what has been consumed, and what messages should be delivered if a new consumer starts consuming, or an existing consumer restarts.

Earlier versions of Kafka used Apache ZooKeeper for offset tracking, but since version 0.9, Kafka uses an internal topic named "__consumer_offsets" to manage these offsets. This change has helped to improve scalability and durability of consumer offsets.

Kafka maintains two types of offsets:

1.	**Current Offset** : The current offset is a reference to the most recent record that Kafka has already provided to a consumer. As a result of the current offset, the consumer does not receive the same record twice.
2.	**Committed Offset** : The committed offset is a pointer to the last record that a consumer has successfully processed. We work with the committed offset in case of any failure in application or replaying from a certain point in event stream.

### **Committing an offset**
1. **Auto Commit**: By default, the consumer is configured to use an automatic commit policy, which triggers a commit on a periodic interval. This feature is controlled by setting two properties:
 enable.auto.commit & auto.commit.interval.ms

    Although auto-commit is a helpful feature, it may result in duplicate data being processed.
    Let’s have a look at an example.
    You’ve got some messages in the partition, and you’ve requested your first poll. Because you received ten messages, the consumer raises the current offset to ten. You process these ten messages and initiate a new call in four seconds. Since five seconds have not passed yet, the consumer will not commit the offset. Then again, you’ve got a new batch of records, and rebalancing has been triggered for some reason. 
    The first ten records have already been processed, but nothing has yet been committed. Right? The rebalancing process has begun. As a result, the partition is assigned to a different consumer. Because we don’t have a committed offset, the new partition owner should begin reading from the beginning and process the first ten entries all over again.
    A manual commit is the solution to this particular situation. As a result, we may turn off auto-commit and manually commit the records after processing them.

2. **Manual Commit**: With Manual Commits, you take the control in your hands as to what offset you’ll commit and when. You can enable manual commit by setting the enable.auto.commit property to false.
There are two ways to implement manual commits :
    1. **Commit Sync**: The synchronous commit method is simple and dependable, but it is a blocking mechanism. It will pause your call while it completes a commit process, and if there are any recoverable mistakes, it will retry. Kafka Consumer API provides this as a prebuilt method.
    2. **Commit Async**: The request will be sent and the process will continue if you use asynchronous commit. The disadvantage is that commitAsync does not attempt to retry. However, there is a legitimate justification for such behavior.
    Let’s have a look at an example.
    Assume you’re attempting to commit an offset as 70. It failed for whatever reason that can be fixed, and you wish to try again in a few seconds. Because this was an asynchronous request, you launched another commit without realizing your prior commit was still waiting. It’s time to commit-100 this time. Commit-100 is successful, however commit-75 is awaiting a retry. Now how would we handle this? Since you don’t want an older offset to be committed.
    This could cause issues. As a result, they created asynchronous commit to avoid retrying. This behavior, however, is unproblematic since you know that if one commit fails for a reason that can be recovered, the following higher level commit will succeed.


### **What if AsyncCommit failure is non-retryable?**

Asynchronous commits can fail for a variety of reasons. For example, the Kafka broker might be temporarily down, the consumer may be considered dead by the group coordinator and kicked out of the group, the committed offset may be larger than the last offset the broker has, and so on.

When the commit fails with a non-retryable error, the commitAsync method doesn't retry the commit, and your application doesn't get a direct notification about it, because it runs in the background. However, you can provide a callback function that gets triggered upon a commit failure or success, which can log the error and you can take appropriate actions based on it.

But keep in mind, even if you handle the error in the callback, the commit has failed and it's not retried, which means the consumer offset hasn't been updated in Kafka. The consumer will continue to consume messages from the failed offset. In such scenarios, manual intervention or alerts might be necessary to identify the root cause and resolve the issue.

On the other hand, synchronous commits (commitSync) will retry indefinitely until the commit succeeds or encounters a 
non-retryable failure, at which point it throws an exception that your application can catch and handle directly. This is why it's often recommended to have a final synchronous commit when you're done consuming messages.

As a general strategy, it's crucial to monitor your consumers and Kafka infrastructure for such failures and handle them appropriately to ensure smooth data processing and prevent data loss or duplication.

### **When to use SyncCommit vs AsyncCommit?**

Choosing between synchronous and asynchronous commit in Apache Kafka largely depends on your application's requirements around data reliability and processing efficiency.

Here are some factors to consider when deciding between synchronous and asynchronous commit:
1. **Synchronous commit (commitSync)**: Use it when data reliability is critical, as it retries indefinitely until successful or a fatal error occurs. However, it can block your consumer, slowing down processing speed.

2. **Asynchronous commit (commitAsync)**: Use it when processing speed is important and some data loss is tolerable. It doesn't block your consumer but doesn't retry upon failures.

3. **Combination**: Many applications use commitAsync for regular commits and commitSync before shutting down to ensure the final offset is committed. This approach balances speed and reliability.