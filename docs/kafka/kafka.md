Apache Kafka is a distributed streaming platform that was developed by LinkedIn in 2010 and later donated to the Apache Software Foundation. It's designed to handle high-throughput, fault-tolerant, and real-time data streaming.

## **Messaging Systems in Kafka**

The main task of managing system is to transfer data from one application to another so that the applications can mainly work on data without worrying about sharing it.
Distributed messaging is based on the reliable message queuing process. Messages are queued non-synchronously between the messaging system and client applications.
There are two types of messaging patterns available:

1. **Point to point messaging system**: 
    In this messaging system, messages continue to remain in a queue. More than one consumer can consume the messages in the queue but only one consumer can consume a particular message. After the consumer reads the message in the queue, the message disappears from that queue.
2. **Publish-subscribe messaging system**:
    In this messaging system, messages continue to remain in a Topic. Contrary to Point to point messaging system, consumers can take more than one topic and consume every message in that topic. Message producers are known as publishers and Kafka consumers are known as subscribers.


## **Key characteristics**

   1. **Scalable**: It supports horizontal scaling by allowing you to add new brokers (servers) to the clusters .
   2. **Fault-tolerant**: It can handle failures effectively due to its distributed nature and replication mechanisms .
   3. **Durable**: Kafka uses a "distributed commit log," which means messages are persisted on disk . This ensures data is not lost even if a server goes down.
   4. **Fast**: Designed to be as fast as possible .
   5. **Performance**: Achieves high throughput for both publishing (producers) and subscribing (consumers) .
   6. **No data loss**: Guarantees that messages are not lost once they are committed to Kafka .
   7. **Zero down time**: Designed for continuous operation without interruption .
   8. **Reliability**: Provides reliable message delivery .

