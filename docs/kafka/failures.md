
What happens if the I/O thread fails to write a batch to the Kafka cluster? Kafka producers can be configured to retry sending the failed batches.

![Steps](kafkaretry.svg)

## **Configuring Retries**

   When creating the producer, you can specify whether to enable retries and for how long Kafka should attempt to rewrite a failed batch.
   `delivery.timeout.ms`: This parameter configures the maximum time (in milliseconds) Kafka will attempt to write a message or retry writing if it fails initially.

## **Error Handling**

   *If Retries are Not Enabled*: If the initial write fails and retries are disabled, the producer immediately invokes an error handler. On the client side, you will receive an error indicating that the messages were not written successfully. You would then need to handle this manually, perhaps by resending the messages from your application.

   *If Retries are Enabled*:
   Kafka will attempt to retry writing the batch.
   If the `delivery.timeout.ms` is exceeded during the retry attempts, the process will again go to the error handler, and an error will be reported to the client.
   If the timeout is not over, Kafka will continue to retry writing the batch.

## **Ensuring Exactly-Once Semantics: Idempotent Producer**

While retries are essential for reliability, they can introduce a new problem: message duplication. An idempotent producer helps solve this.

1. **The Duplication Problem**

Consider this scenario:

  A batch of messages is sent to Kafka.
  The batch is successfully written to the Kafka cluster.
  However, the acknowledgement (ACK) or return response from Kafka back to the producer is lost or fails to be sent.
  The producer, not having received the ACK, assumes the batch failed to write.
  Consequently, the producer resends the exact same batch of messages to the Kafka cluster.
  Without idempotence enabled, Kafka would simply write this "new" batch again, leading to duplicate messages in the topic.

2. **How Idempotence Works**

An idempotent producer prevents this duplication.

`enable.idempotence`: When this parameter is set to `true` (enabled), Kafka performs a duplicate check before writing any incoming batch.
Duplicate Detection: If Kafka detects that an incoming batch is a duplicate (meaning it has already been successfully written), it intelligently understands that the producer likely didn't receive the previous acknowledgement.
Action for Duplicates: Instead of rewriting the batch and causing duplication, Kafka's cluster will re-send the acknowledgement for that particular batch to the producer.
Outcome: The producer receives the ACK, understands the batch was successful, and avoids resending, thus avoiding duplication.

To avoid duplicacy in scenarios where ACKs might be lost, you should enable idempotence in your Kafka producer configuration.

## **Maintaining Message Order**

Even with retries and idempotence, another issue can arise: out-of-order messages within a single partition.

**The Ordering Problem**

Kafka guarantees message ordering within a single partition. However, with multiple "in-flight" requests, this guarantee can be compromised during retries:

Consider a scenario where three batches (Batch 1, Batch 2, Batch 3) are sent sequentially to the same partition:

1. Batch 1 is sent and successfully written.
2. Batch 2 is sent but fails to write initially. A retry operation for Batch 2 is initiated.
3. While Batch 2 is undergoing retry (which takes some time), the I/O thread proceeds to send Batch 3, which is then successfully written to the partition before Batch 2's retry completes.
4. Finally, Batch 2's retry succeeds, and it is written to the partition.

Actual order of sending: Batch 1, Batch 2, Batch 3.
Resulting order in the partition: Batch 1, Batch 3, Batch 2.

This "screws up" the intended message order within the partition, which is generally undesirable for many applications.

**Understanding `in-flight` Requests**

An `in-flight request` refers to a request that has been sent by the producer but has not yet received a completion response or acknowledgement.
The `max.in.flight.requests.per.connection` parameter determines the maximum number of requests that can be "in-flight" (sent but not yet acknowledged) at any given time for a particular connection. If this is set to, say, `5`, the producer can send up to five requests concurrently without waiting for any of them to complete.

*Solution: Setting `max.in.flight.requests.per.connection` to 1*

To guarantee strict message ordering within a partition, you can set `max.in.flight.requests.per.connection = 1`.

How it works: By setting this to `1`, the producer will send only one batch at a time and wait for its completion (i.e., receipt of the acknowledgement, even after retries) before sending the next batch.

Effect on ordering: If a batch fails and requires a retry, no other batches will be sent to the cluster until that specific batch (and its retries) are fully completed. This ensures that messages are always written in their original sequential order within the partition.

**Trade-offs**

While `max.in.flight.requests.per.connection = 1` ensures strict ordering, it comes at a cost:

Slower Message Writing: It effectively makes the message writing operation synchronous, meaning throughput will be reduced because the producer waits for each batch to complete before moving to the next. This is a trade-off between strict ordering and high throughput.


## **Ways to send messages to kafka**

**Method 1: Fire and Forget**

The "Fire and Forget" method is the simplest way to send messages.

**Concept**: In this technique, the producer sends a message to the Kafka server and does not wait for any acknowledgment or confirmation about its successful arrival. The producer simply "fires" the message and "forgets" about it.

**Assumption**: Kafka is a highly reliable system, and Kafka clusters are generally highly available. The producer also automatically retries sending messages if the first attempt fails. Therefore, most of the time (99.9%), messages will arrive successfully.
   
**Analogy**: Imagine sending a letter by mail without requesting a delivery confirmation. You assume it will arrive because the postal service is generally reliable.
   
**Advantages**:
Very fast: Messages are sent immediately without any delay for waiting on responses.
High throughput: You can send a large number of messages in a very short amount of time.
   
**Disadvantages**:
   Messages can be lost without notification: If something goes wrong (e.g., the Kafka broker goes down), the producer will not be aware that the messages failed to reach the cluster. These messages will be permanently lost.
   "The client is not even getting any information that whether really the message is written or not".

```python
for i in range(100):
data = {"number": i, "message": f"This is message {i}"}
producer.send(TOPIC_NAME, data) # - No waiting for response
print(f"Sent message: {data}")
time.sleep(0.5) # - Optional sleep for demonstration
```

**Method 2: Synchronous Send**

The "Synchronous Send" method ensures that the producer receives a confirmation for each message sent before proceeding to the next.

**Concept**: After sending a message, the producer waits for a response (acknowledgment or error) from the Kafka cluster before sending the next message. This makes the entire sending process sequential.
   
**Analogy**: This is like waiting in a queue to get a movie ticket. You cannot get your ticket until the person in front of you has successfully received theirs.
   
**How it Works**: The `producer.send()` method returns a `Future` object. By calling the `.get()` method on this `Future` object, the producer blocks and waits for the operation to complete. You can specify a `timeout` for how long to wait.
   
**Expected Response**: If successful, the `get()` method returns `RecordMetadata` containing information like the topic name, partition number, and offset where the message was published. If it fails, an exception is raised.
   
**Advantages**:
   Guaranteed delivery notification. The producer knows whether each message was successfully written or if an error occurred. This allows for robust error handling and logging on the client side.
   
**Disadvantages**:
Very slow. This method makes the overall message sending process significantly slower because each message requires a full "round trip" to the Kafka cluster and back. For example, if the network round-trip time is 10 milliseconds, sending 100 messages would take at least 1 second (100 messages  10 ms/message).
"This is kind of making the whole process little bit slow".

```python
for i in range(100):
data = {"number": i, "message": f"This is message {i}"}
try:
# send method returns a Future object, .get() waits for up to 10 seconds
record_metadata = producer.send(TOPIC_NAME, data).get(timeout=10)
print(f"Successfully produced message {data['number']} to topic {record_metadata.topic} "
f"in partition {record_metadata.partition} and offset {record_metadata.offset}") #
except Exception as ex:
print(f"Failed to write message {data['number']}: {ex}") #
# Log the error, retry, or take other appropriate action
time.sleep(0.5) # Optional sleep
```

**Method 3: Asynchronous Send (with Callbacks)**

The Asynchronous Send method with callbacks offers a middle ground, combining the speed of "Fire and Forget" with the error-handling capabilities of "Synchronous Send".

**Concept**: The producer sends messages rapidly without waiting for an immediate response, similar to "Fire and Forget." However, it attaches callback functions that will be invoked automatically in the background once the message delivery operation (success or failure) is complete.
   
**How it Works**: When `producer.send()` is called, it still returns a `Future` object. Instead of calling `.get()`, you use `.add_callback()` to register a function to be called on success, and `.add_errback()` to register a function to be called on failure. These callback functions receive information about the success (e.g., `RecordMetadata`) or failure (e.g., exception).
   
**Advantages**:
   High Performance: Messages are sent very quickly, as the producer does not wait for a response for each message before sending the next. This is "ultra fast" compared to synchronous sending.
   Reliable Error Handling: Despite sending rapidly, the producer is still notified of message delivery status (success or failure) through the callback functions. This overcomes the main drawback of the "Fire and Forget" method.
   Common in Industry: This technique is widely followed in real-world Kafka applications due to its balance of speed and reliability.


```python
# Define callback functions
def on_send_success(record_metadata, message_data): #
"""
This function is called when a message is successfully written to Kafka.
It receives the RecordMetadata and the original message data.
"""
print(f"Successfully produced message {message_data} to topic {record_metadata.topic} "
f"in partition {record_metadata.partition} and offset {record_metadata.offset}") #

def on_send_error(ex, message_data): #
"""
This function is called when a message fails to be written to Kafka.
It receives the exception and the original message data.
"""
print(f"Failed to write message {message_data}: {ex}") #
# Here you can log the error, store the failed message, etc.

#
for i in range(100):
data = {"number": i, "message": f"This is message {i}"}

# Send the message without blocking
future = producer.send(TOPIC_NAME, data) #

# Attach callback functions for success and failure
# Note: The video's code passes `data` as a second argument to the callbacks
# which is a useful pattern for associating context.
future.add_callback(on_send_success, data) #
future.add_errback(on_send_error, data) #

print(f"Sent message (asynchronously): {data}")
time.sleep(0.5) # - Optional sleep, useful for demoing failures
```

**Choosing the Right Method**

The choice of sending method depends on your application's specific requirements:

**Fire and Forget**: Use when maximum throughput is critical, and occasional message loss is acceptable or can be handled by downstream systems (e.g., logging, metrics, real-time analytics where exact message counts aren't critical).
   
**Synchronous Send**: Use when guaranteed per-message delivery status is paramount, and you can tolerate lower throughput due to the blocking nature. This might be suitable for low-volume, high-value data where immediate confirmation is essential.
   
**Asynchronous Send (with Callbacks)**: This is generally the most recommended approach for most production scenarios. It offers a good balance of high throughput and reliable error handling, providing notifications without blocking the main sending thread.


## **The Challenge of key=null**

When a Kafka producer sends messages to a topic, it typically uses a **message key** to determine which partition the message should go to. Messages with the same key are guaranteed to land in the same partition, ensuring ordered processing for those related messages.

However, a common scenario arises when **no key is provided** (the `key` is `null`). In this situation, Kafka needs a strategy to distribute these messages across the available partitions. The video discusses how this distribution happens and how Kafka has optimized this process over time.

**Approach 1: Simple Round-Robin Distribution**

**How it Works**

The simplest way to distribute messages when `key=null` is using a **round-robin fashion**.

  The first message is published to Partition 0 (P0).
  The second message goes to Partition 1 (P1).
  The third message goes to Partition 2 (P2), and so on.
  Once all partitions have received a message, the distribution cycles back to Partition 0.

Example: Let's assume a Kafka topic has 5 partitions (P0, P1, P2, P3, P4) and messages `1, 2, 3, 4, 5, 6` are being produced.

  Message `1` goes to P0.
  Message `2` goes to P1.
  Message `3` goes to P2.
  Message `4` goes to P3.
  Message `5` goes to P4.
  Message `6` goes back to P0.

**Drawbacks**:

  1. **More Time Consuming**: Each individual message is published to a different partition. This constant switching between partitions adds overhead and consumes more time.  
  2. **High CPU Utilization for Broker**: The Kafka broker, which is responsible for receiving and storing messages, has to individually send each message to a potentially different partition. This task is CPU-intensive for the broker, which also needs to handle many other important activities.

**Approach 2: Optimized Sticky Partitioning**

To overcome the drawbacks of round-robin distribution, Kafka introduced an optimized approach known as **Sticky Partitioning**. This method focuses on efficiency by leveraging Kafka producer's internal batching mechanism.

**How Sticky Partitioning Works**
When the message `key` is `null`, Kafka optimizes distribution by publishing all messages within a particular batch to a single partition.

1.  The producer creates a batch of messages.
2.  This entire batch is published to one partition (e.g., P0).
3.  The next batch created by the producer will then be published to the next partition (e.g., P1), and so on, in a round-robin like fashion for the *batches*, not individual messages.

Example:
Using the same 5 partitions (P0, P1, P2, P3, P4) and messages `1, 2, 3, 4, 5, 6`.
Suppose the producer's internal batching accumulates messages `1, 2, 3` into the first batch, and `4, 5, 6` into the second batch.

1.  Batch 1 (`1, 2, 3`)** goes to P0.
2.  Batch 2 (`4, 5, 6`)** goes to P1.
3.  The next batch (if any) would go to P2, and so on.

This approach is called "Sticky Partitioning" because the producer/broker "sticks" to one particular partition for an entire batch of messages, rather than switching partitions for individual messages within that batch.

**Advantages**

  1. **Faster (Lower Latency)**: The complete batch is written to one place (a single partition). This reduces the overhead of writing to different locations for individual messages, resulting in faster processing and lower latency.
  2. **Less CPU Utilization for Broker**: The broker is not constantly computing partition assignments for individual messages. Once a batch is created by the producer, the broker simply publishes that entire batch to a designated partition. This makes the process less CPU-intensive for the broker.

Because of these advantages, **sticky partitioning is the approach followed by Kafka's backend nowadays** when no key is passed with the messages.