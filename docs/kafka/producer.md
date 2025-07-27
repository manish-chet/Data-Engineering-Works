## **Producers**

Producers are applications that write or publish data to the topics within a Kafka cluster .
They use the Producer API to send data .
Producers can choose to write data either at the topic level (letting Kafka distribute it across partitions) or to specific partitions of a topic.


*Illustrative Example*: A journalist writing a new article would be a producer, publishing the article to the news topic.
 
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
    **Acks = 0**: Producers will not wait for any acknowledgement from the server.  

    ![Steps](acks0.svg)

    !!! Note

            Behavior: The producer does not wait for any reply from the broker after sending a message. It assumes the message is successfully written immediately.
            Risk: This is the riskiest approach regarding data loss. If the broker goes offline, an exception occurs, or the message is simply not received due to network issues, the producer will not be aware of it, and the message will be lost.
            Latency: Offers the lowest latency because there's no waiting period for acknowledgements.

       
    **Acks = 1 (Default)**: The leader broker will write the record to its local log and respond without waiting for full acknowledgement from all followers. In this case, if the leader fails immediately after acknowledgement (before followers replicate), the record will be lost.

    ![Steps](acks1.svg)

    !!! Note
    
            Behavior: The producer waits for a success response from the broker only when the leader partition has received the message. Once the leader has written the message, it sends an acknowledgment back to the producer, allowing the producer to proceed.
            Data Safety: Improves data safety compared to `acks=0`. If the message cannot be written to the leader (e.g., leader crashes), the producer receives an error and can retry sending the message, thus avoiding potential data loss.
            Disadvantage: While better, `acks=1` does not guarantee that the message has been replicated to other in-sync replicas. If the leader partition fails after acknowledging the message to the producer but before the message is replicated to its followers, the message could still be lost.

       
    **Acks = -1**: The leader will wait for the full set of in-sync replicas to acknowledge the record. This guarantees that the record will not be lost as long as at least one in-sync replica remains alive. This provides the strongest guarantee and is equivalent to acks=all.

    
    ![Steps](acksall.svg)  

    !!! Note
    
            Behavior: The producer receives a success response from the broker only when the message has been successfully written not only to the leader partition but also to all configured in-sync replicas (ISRs).
                The leader receives the message and writes it.
                The leader then sends the message to all its in-sync follower replicas.
                Once all in-sync replicas confirm they have written the message, they send acknowledgements back to the leader.
                Only after the leader accumulates acknowledgements from all in-sync replicas, does it send the final success response to the producer.
            Data Safety: This approach offers the highest level of data safety and guarantees against message loss. The chance of message loss is very low.
            Disadvantage: The primary drawback is added latency. The producer has to wait longer for the message to be fully replicated across all replicas before it gets the final acknowledgment. This makes it a slower process compared to `acks=0` or `acks=1`.


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

## **How Keys Determine Partition Assignment**

Kafka uses the message key to decide which partition an incoming message will be written to.

   1. **With a Key (Hashing Algorithm)**:

       When a key is provided, Kafka applies a hashing algorithm to the key.
       The output of the hashing function (which is based on the key) is then mapped to a specific partition out of the topic's available partitions.

       ![Steps](key.svg)  
       
       *Example*: If the hashing concept is "divide by three and use the remainder," a key of `7` would result in a remainder of `1`, so the message would go to partition 1. A key of `5` would result in a remainder of `2`, so that message would go to partition 2.
       
       **Crucial Point**: All messages that share the same key will always go to the same partition. This is because the same key will consistently produce the same hash output, leading to the same partition assignment. This property is vital for maintaining message order for a specific logical entity (e.g., all events related to a particular user ID).
       
    !!! Tip
        It's possible for different keys to end up in the same partition if their hash outputs happen to be the same, but messages with an identical key will always map to the same partition.           

   2. **Without a Key (Null Key - Round Robin)**:

       ![Steps](null.svg)  
       If the message key is `null` (i.e., no key is provided), Kafka uses a round-robin fashion to distribute messages among partitions.
       This means the first message goes to partition 0, the second to partition 1, the third to partition 2, and then it cycles back to partition 0, and so on. This ensures an even distribution of messages when order per key is not a concern.



## **When a producer sends messages in Kafka, the process involves**

![Steps](producerinternal.svg)

When an application produces a message using a Kafka API (e.g., Java or Python API), the record goes through a series of internal steps before being sent to the Kafka cluster.

**From Application to Producer**

An application sends a "record".
A record typically contains a topic (where the record should go), an optional partition (though rarely specified directly by the user), a key, and the value (the actual message content). The key is primarily used for calculating the target partition.

**Step 1: Serialization**

The first thing the producer does is serialization for both the key and value.

Purpose: Messages need to be sent over a network, which requires them to be converted into a binary format (a stream of zeros and ones or a byte array). The serializer handles this conversion from an object (your message data) to a byte array.

**Step 2: Partitioning**

After serialization, the binary data is sent to the partitioner.
At this stage, the producer determines to which partition of the topic the record will be sent.

How it works:

If a key is provided: A hashing algorithm is applied to the key. The output of this hash is then typically divided by the total number of partitions for the topic, and the remainder determines the destination partition.
Example: If a key `7` is hashed and then processed with "divide by three and use the remainder", it might map to partition `1`. A key `5` might map to partition `2` [based on video explanation in previous context]. The key ensures that messages with the same key consistently go to the same partition.
If no key is provided (null key): Messages are distributed in a round-robin fashion across all available partitions, ensuring an even distribution.

**Step 3: Buffering**

Once the destination partition for a record is determined, the record is not immediately sent to the Kafka cluster.
Instead, it is written into an internal buffer specifically assigned to that partition. Buffers accumulate multiple messages. 
   
This accumulation allows the producer to:

Perform I/O operations more efficiently. Sending many small messages individually is less efficient than sending them in larger chunks.
Apply compression more effectively. Compression algorithms often work better with larger blocks of data, as they can identify more patterns and redundancies.
The producer aims to "patch" (batch) records for this efficiency.

**Step 4: Batching**

From the internal buffer, multiple messages are "clubbed" together into batches. These batches are then sent to the Kafka cluster.
   
Two important configuration parameters control when a batch is sent:

 `linger.ms`: This parameter instructs the producer to wait up to a certain number of milliseconds (e.g., 5 milliseconds) before sending the accumulated content. This allows more messages to collect in the buffer, potentially forming a larger, more efficient batch.

 `batch.size`: This parameter defines the maximum size (in bytes) that a batch can reach (e.g., 5 MB).
   
Batch Sending Logic: A batch is sent to the Kafka cluster when either the `linger.ms` timeout expires OR the `batch.size` limit is reached, whichever condition is satisfied first.

**Step 5: Sending to Kafka Cluster**

   Once a batch is formed based on `linger.ms` or `batch.size` conditions, the complete batch is sent to the Kafka cluster.

**Step 6: Retries**

   It's possible for message writing to fail due to networking issues or other problems.
   Kafka producers can be configured to retry sending a message if the initial attempt fails.
   You can set the number of retries (e.g., `retry=5`), meaning the producer will attempt to rewrite the message up to five times before throwing an exception.

**Step 7: Receiving Record Metadata**

   If the message writing is successful (after retries, if any), the Kafka cluster sends `RecordMetadata` back to the producing application.

   This `RecordMetadata` provides crucial information about the successfully written record, including:
    Partition: The specific partition where the data was written.
    Offset: The offset (position) of the record within that partition.
    Timestamp: The time when the record arrived or was written to Kafka.

## **Importance of Understanding Producer Internals**

Having a clear understanding of these internal mechanisms is vital for:

1. **Troubleshooting**: For instance, if messages are being produced at a very high rate and exceeding the producer's internal buffer volume (e.g., 32 MB), messages might not be written to Kafka. Knowing this allows you to increase the buffer volume to accommodate the incoming message flow.
    
2. **Performance Tuning**: Properly configuring parameters like `linger.ms` and `batch.size` can significantly impact throughput and latency.
     
3. **Reliability**: Understanding how retries work helps in building resilient applications that can handle transient failures.


## **Producer Corner Cases in Kafka Tuning (Replica Management)**

   1. **Replica Fetchers**: This setting determines the number of threads responsible for replicating data from leaders. It's crucial to have a sufficient number of replica fetchers to enable complete parallel replication if multiple threads are available.
   2. **replica.fetch.max.bytes**: This parameter dictates the maximum amount of data used to fetch from any partition in each fetch request. It is generally beneficial to increase this parameter.
   3. **replica.socket.receive.buffer.bytes**: The size of buffers can be increased, especially if more threads are available.
   4. **Creating Replicas**: Increasing the level of parallelism allows for data to be written in parallel, which automatically leads to an increase in throughput.
   5. **num.io.threads**: This parameter is determined by the amount of disk available in the cluster and directly influences the value for I/O threads .


## **Experiment Scenario**
A Kafka producer is configured with default settings, including `linger.ms=0` and `buffer.memory=32MB` (which is sufficient for small messages).
The producer attempts to send 1000 messages (numbered 0 to 999) rapidly in a loop.

**Observed Result**: The consumer only receives messages up to number `997`, and the Kafka logs confirm messages only up to `997` were written. Messages `998` and `999` are lost.

**Reason**: The messages `998` and `999` were still present in the Kafka producer's internal buffer when the Python code finished execution (`Process finished with exit code 0`). The I/O thread did not get enough time to take these remaining messages from the buffer and publish them to the Kafka cluster before the application terminated.

**Solution**:
To ensure all messages are delivered, even when sending rapidly, you must explicitly tell the producer to flush its buffer before exiting or closing the connection. This is done using `producer.flush()` and `producer.close()` methods.

   `producer.flush()`: This method explicitly flushes all accumulated messages from the producer's buffer to the Kafka cluster. It blocks until all messages in the buffer have been successfully sent and acknowledged by the brokers.

   `producer.close()`: This method closes the producer connection, releasing any resources it holds. It implicitly calls `flush()` before closing, but it's often good practice to call `flush()` explicitly beforehand, especially if there's any risk of the `close()` method being interrupted.


**Before Fix (Potential Message Loss)**:
```python
from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic_name = 'hello-world'
num_messages = 1000

for i in range(num_messages):
    data = {"number": i}
    # print(f"Sending: {data}") # For debugging
    producer.send(topic_name, value=data)

# Application ends here. If messages are still in buffer, they are lost.
print("Producer finished sending messages.")
```

**After Fix (Ensured Delivery)**:
```python
from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic_name = 'hello-world'
num_messages = 1000

for i in range(num_messages):
    data = {"number": i}
    producer.send(topic_name, value=data)

# Ensure all messages are sent from buffer to Kafka cluster
producer.flush()
# Close the producer connection
producer.close()

print("Producer finished sending all messages and closed.")
```