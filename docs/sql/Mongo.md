### What is NoSQL Database?
NoSQL databases, also known as "non-SQL" or "not only SQL", are databases that provide a mechanism to store and retrieve data modeled in ways other than the tabular format used in relational databases. They are typically used in large-scale or real-time web applications where the ability to scale quickly and handle large, diverse types of data is critical.

Here are some key characteristics and features of NoSQL databases:

1.	Schema-less: NoSQL databases do not require a fixed schema, which gives you the flexibility to store different types of data entities together.
2.	Scalability: NoSQL databases are designed to expand easily to handle more traffic. They are horizontally scalable, meaning you can add more servers to handle larger amounts of data and higher loads.
3.	Diverse Data Models: NoSQL databases support a variety of data models including key-value pairs, wide-column, graph, or document. This flexibility allows them to handle diverse types of data and complex data structures.
4.	Distributed Architecture: Many NoSQL databases are designed with a distributed architecture, which can improve fault tolerance and data availability.
5.	Performance: Without the need for data relationships and joins as in relational databases, NoSQL databases can offer high-performance reads and writes.

### Types of NoSQL Databases
NoSQL databases are categorized into four basic types based on the way they organize data. Let's go through each type and provide examples:

1. Document Databases: These store data in documents similar to JSON (JavaScript Object Notation) objects. Each document contains pairs of fields and values, and the values can typically be a variety of types including strings, numbers, booleans, arrays, or objects. Each document is unique and can contain different data from other documents in the collection. This structure makes document databases flexible and adaptable to various data models.
    Example: MongoDB, CouchDB.
2. Key-Value Databases: These are the simplest type of NoSQL databases. Every single item in the database is stored as 
an attribute name (or 'key') and its value. The main advantage of a key-value store is the ability to read and write operations using a simple key. This type of NoSQL database is typically used for caching and session management.
    Example: Redis, Amazon DynamoDB
3. Wide-Column Stores: These databases store data in tables, rows, and dynamic columns. Wide-column stores offer high performance and a highly scalable architecture. They're ideal for analyzing large datasets and are capable of storing vast amounts of data (Big Data).
    Example: Apache Cassandra, Google BigTable.
4. Graph Databases: These are used to store data whose relations are best represented as a graph. Each node of the graph represents an entity, and the relationship between nodes is stored directly, which allows the data to be retrieved in one operation. They're ideal for storing data with complex relationships, like social networks or a network of IoT devices.
    Example: Neo4j, Amazon Neptune

### Difference between Transactional & NoSQL Database
![Difference between Transactional & NoSQL Database](mongo.svg)


### NoSQL Databases are Good fit for Analytical Queries?
While NoSQL databases can handle certain analytical tasks, their primary purpose is not for heavy analytical queries. Traditional relational databases and data warehousing solutions, such as Hive, Redshift, Snowflake or BigQuery, are often better suited for complex analytical queries due to their ability to handle operations like joins and aggregations more efficiently

### NoSQL Databases in BigData Ecosystem
The strength of NoSQL databases lies in their flexibility, scalability, and speed for certain types of workloads, making them ideal for specific use-cases in the Big Data ecosystem:

1.	Handling Large Volumes of Data at Speed: NoSQL databases are designed to scale horizontally across many servers, which enables them to handle large volumes of data at high speed. This is particularly useful for applications that need real-time read/write operations on Big Data.
2.	Variety of Data Formats: NoSQL databases can handle a wide variety of data types (structured, semi-structured, unstructured), making them ideal for Big Data scenarios where data formats are diverse and evolving.
3.	Fault Tolerance and Geographic Distribution: NoSQL databases have a distributed architecture that provides high availability and fault tolerance, critical for applications operating on Big Data.
4.	Real-time Applications: Many Big Data applications require real-time or near-real-time functionality. NoSQL databases, with their high-speed read/write capabilities and ability to handle high volumes of data, are often used for real-time analytics, IoT data, and other similar scenarios.
That said, the choice between SQL, NoSQL, or other database technologies should be based on the specific needs of the use-case at hand.


### CAP Theorem
The CAP theorem is a concept that a distributed computing system is unable to simultaneously provide all three of the following guarantees:

1.	Consistency (C): Every read from the system receives the most recent write or an error. This implies that all nodes see the same data at the same time. It's the idea that you're always reading fresh data.
2.	Availability (A): Every request receives a (non-error) response, without the guarantee that it contains the most recent write. It's the idea that you can always read or write data, even if it's not the most current data.
3.	Partition Tolerance (P): The system continues to operate despite an arbitrary number of network or message failures (dropped, delayed, scrambled messages). It's the idea that the system continues to function even when network failures occur between nodes.
Now, the key aspect of the CAP theorem, proposed by computer scientist Eric Brewer, is that a distributed system can satisfy any two of these three guarantees at the same time, but not all three. Hence the term "CAP" - Consistency, Availability, and Partition tolerance.

![Difference between Transactional & NoSQL Database](mongo2.svg)

Here's how the three dichotomies look like:

1. CA (Consistent and Available) systems prioritize data consistency and system availability but cannot tolerate network partitions. In such a system, if there is a partition between nodes, the system won't work as it doesn't support partition tolerance.
2. CP (Consistent and Partition-tolerant) systems prioritize data consistency and partition tolerance. If a network partition occurs, the system sacrifices availability to ensure data consistency across all nodes.
3. AP (Available and Partition-tolerant) systems prioritize system availability and partition tolerance. If a network partition occurs, all nodes may not immediately reflect the same data, but the system remains available.
Remember, real-world systems must tolerate network partitions (P), so the practical choice is between consistency (C) and availability (A) when partitions occur.

