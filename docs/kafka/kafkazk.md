
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

What does ZooKeeper do in Kafka Cluster?

1. Broker Management: It helps manage and coordinate the Kafka brokers, and keeps a list of them.
2. Topic Configuration Management: ZooKeeper maintains a list of topics, number of partitions for each topic, location of each partition and the list of consumer groups.
3. Leader Election: If a leader (the node managing write and read operations for a partition) fails, ZooKeeper can trigger leader election and choose a new leader.
4. Cluster Membership: It keeps track of all nodes in the cluster, and notifies if any of these nodes fail.
5. Synchronization: ZooKeeper helps in coordinating and synchronizing between different nodes in a Kafka cluster.

Kafka Cluster & Partition Reassignment

   1. Kafka Cluster Controller: In a Kafka cluster, one of the brokers is designated as the controller. This controller is responsible for managing the states of partitions and replicas and for performing administrative tasks such as reassigning partitions.
   2. Partition Growth: It is important to note that the partition count of a Kafka topic can always be increased, but never decreased. This is because reducing partitions could lead to data loss.
   3. Partition Reassignment Use Cases: Partition reassignment is used in several scenarios:
       Moving a partition across different brokers.
       Rebalancing the replicas of a partition to a specific set of brokers.
       Increasing the replication factor of a topic.