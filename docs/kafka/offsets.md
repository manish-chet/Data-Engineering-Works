## **Offsets**
Offsets represent the position of each message within a partition and are uniquely identifiable, ever-increasing integers . There are three main variations of offsets :

   1. **Log End Offset**: This refers to the offset of the last message written to any given partition .
   2. **Current Offset**: This is a pointer to the last record that Kafka has already sent to the consumer in the current poll .
   3. **Committed Offset**: This indicates the offset of a message that a consumer has successfully consumed .
   4. **Relationship**: The committed offset is typically less than the current offset .

In Apache Kafka, consumer offset management – that is, tracking what messages have been consumed – is handled by Kafka itself.

When a consumer in a consumer group reads a message from a partition, it commits the offset of that message back to Kafka. This allows Kafka to keep track of what has been consumed, and what messages should be delivered if a new consumer starts consuming, or an existing consumer restarts.

Earlier versions of Kafka used Apache ZooKeeper for offset tracking, but since version 0.9, Kafka uses an internal topic named "**__consumer_offsets**" to manage these offsets. This change has helped to improve scalability and durability of consumer offsets.

Kafka maintains two types of offsets:

1.	**Current Offset** : The current offset is a reference to the most recent record that Kafka has already provided to a consumer. As a result of the current offset, the consumer does not receive the same record twice.
2.	**Committed Offset** : The committed offset is a pointer to the last record that a consumer has successfully processed. We work with the committed offset in case of any failure in application or replaying from a certain point in event stream.

## **Committing an offset**

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


## **What if AsyncCommit failure is non-retryable?**

Asynchronous commits can fail for a variety of reasons. For example, the Kafka broker might be temporarily down, the consumer may be considered dead by the group coordinator and kicked out of the group, the committed offset may be larger than the last offset the broker has, and so on.

When the commit fails with a non-retryable error, the commitAsync method doesn't retry the commit, and your application doesn't get a direct notification about it, because it runs in the background. However, you can provide a callback function that gets triggered upon a commit failure or success, which can log the error and you can take appropriate actions based on it.

But keep in mind, even if you handle the error in the callback, the commit has failed and it's not retried, which means the consumer offset hasn't been updated in Kafka. The consumer will continue to consume messages from the failed offset. In such scenarios, manual intervention or alerts might be necessary to identify the root cause and resolve the issue.

On the other hand, synchronous commits (commitSync) will retry indefinitely until the commit succeeds or encounters a 
non-retryable failure, at which point it throws an exception that your application can catch and handle directly. This is why it's often recommended to have a final synchronous commit when you're done consuming messages.

As a general strategy, it's crucial to monitor your consumers and Kafka infrastructure for such failures and handle them appropriately to ensure smooth data processing and prevent data loss or duplication.

## **When to use SyncCommit vs AsyncCommit?**

Choosing between synchronous and asynchronous commit in Apache Kafka largely depends on your application's requirements around data reliability and processing efficiency.

Here are some factors to consider when deciding between synchronous and asynchronous commit:

1. **Synchronous commit (commitSync)**: Use it when data reliability is critical, as it retries indefinitely until successful or a fatal error occurs. However, it can block your consumer, slowing down processing speed.

2. **Asynchronous commit (commitAsync)**: Use it when processing speed is important and some data loss is tolerable. It doesn't block your consumer but doesn't retry upon failures.

**Combination**: Many applications use commitAsync for regular commits and commitSync before shutting down to ensure the final offset is committed. This approach balances speed and reliability.


## **What is Out-of-Order Commit?**


Normally, you might expect offsets to be committed sequentially (e.g., commit for message 1, then 2, then 3, and so on). However, Kafka's design allows for *out-of-order commits*, meaning a consumer can commit a later offset even if earlier messages in the sequence haven't been explicitly committed.

**A Simple Scenario**

Consider a Kafka topic with messages 1, 2, 3, 4, 5, 6, etc..

1.  A consumer polls messages and receives 1, 2, 3, and 4.
2.  However, for some reason, the consumer only commits the offset for message 4 to the `__consumer_offset` topic. It does not send explicit commits for messages 1, 2, or 3.
3.  Then, the consumer goes down.

The Broker's Behavior

When the consumer spins up again, a crucial question arises: Will the Kafka broker re-send messages 1, 2, and 3 (for which no explicit commit was received), or will it start from message 5?

The correct answer is: The Kafka broker will not re-send messages 1, 2, or 3.

 1. The broker simply checks the `__consumer_offset` topic for the latest committed offset for that particular consumer group and topic.
 2. In our scenario, the latest committed offset is for message 4 (which means the next message to read is 5).
 3. The broker will then start sending messages from message 5 onwards (i.e., 5, 6, 7, etc.).
 3. Kafka assumes that all messages prior to the latest committed offset have been successfully processed, even if individual commits for those messages were not received. This committed offset acts like a "bookmark".


This behavior is termed "out-of-order commit" because, ideally, commits should be sequential (1, then 2, then 3, then 4). However, in this scenario, a commit for message 4 is received directly, without commits for messages 1, 2, or 3.

## **Advantages of Out-of-Order Commit**

The primary advantage of out-of-order commit is reduced overhead.

 1. Committing an offset for every single message individually can produce a lot of overhead, as it's a complex operation.
 2. Instead, consumers can consume a batch of messages (e.g., 1, 2, 3, 4).
 3. After processing the entire batch, the consumer only needs to commit the offset of the last message in that batch (e.g., message 4).
 4. This way, the entire batch is effectively acknowledged, and the broker will not re-send any messages within that batch, understanding them as successfully processed. This significantly improves efficiency by reducing the number of commit operations.

## **Disadvantages of Out-of-Order Commit**

While efficient, out-of-order commit has a significant disadvantage: potential message loss.

 1. Imagine a scenario where a consumer processes messages using multiple threads or a complex backend system.
 2. If messages 1, 2, and 3 fail during processing, but message 4 (which was processed by a separate, successful thread) is committed.
 3. Even though messages 1, 2, and 3 failed, because message 4's offset was committed, the broker will *not re-send* those failed messages when the consumer restarts.
 4. This can lead to *data loss* or inconsistent processing if not handled carefully at the application level.

