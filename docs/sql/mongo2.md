1. NoSQL Database: MongoDB is a NoSQL database, meaning it does not use traditional table-based relational database structures. It's designed for large scale data storage and for handling diverse data types.
2. Document-Oriented: It stores data in JSON-like documents (BSON format), which allows for varied, dynamic schemas. This is in contrast to SQL databases which use a fixed table schema.
3. Schema-less: MongoDB is schema-less, meaning that the documents in the same collection (equivalent to tables in SQL) do not need to have the same set of fields or structure, and the common field in different documents can hold different types of data.
4. Scalability: It offers high scalability through sharding, which distributes data across multiple machines.
5. Replication: MongoDB provides high availability with replica sets. A replica set consists of two or more copies of the data. Each replica set member may act in the role of primary or secondary replica at any time. The primary replica performs all write operations, while secondary replicas maintain a copy of the data of the primary using built-in replication.
6. Querying: Supports a rich set of querying capabilities, including document-based queries, range queries, regular expression searches, and more.
7. Indexing: Any field in a MongoDB document can be indexed, which improves the performance of search operations.

### MongoDB Architecture
![Mongo arch](mongoarch.svg)

1. Document Model:
BSON Format: MongoDB stores data in BSON (Binary JSON) documents, which are JSON-like structures. This format supports a rich variety and complexity of data types. Unlike relational databases, MongoDB does not require a predefined schema. The structure of documents can change over time.

2. Collections:
Similar to Tables: Collections in MongoDB are analogous to tables in relational databases. They hold sets of documents.
Schema-less: Each document in a collection can have a completely different structure.

3. Database:
Multiple Collections: A MongoDB instance can host multiple databases, each containing their own collections.
 
4. Sharding:
a shard typically refers to a group of multiple nodes (machines), especially in production environments. 
Each shard is often a replica set, which is a group of mongod instances that hold the same data set. In this setup, each shard consists of multiple machines - one primary and multiple secondaries.

    Shard Key: The distribution of data across shards is determined by a shard key. MongoDB partitions data in the collection based on this 
    key, and different partitions (or chunks of data) are stored on different shards.

    Primary Node: Within each shard (replica set), there is one primary node that handles all write operations. All data changes are first written to the primary.

    Secondary Nodes: The secondary nodes replicate data from the primary node, providing redundancy and increasing data availability. They can also serve read operations to distribute the read load.

5. Query Router
Role in Sharded Clusters:The Query Router is typically a mongos instance in MongoDB. It acts as an intermediary between client applications and the MongoDB sharded cluster.

    Query Distribution: The Query Router receives queries from client applications and determines the appropriate shard(s) that hold the relevant data. It routes the query to the correct shard(s) based on the shard key and the cluster’s current configuration.

    Aggregation of Results: After receiving responses from the shards, the Query Router aggregates these results and returns them to the client application. This process is transparent to the client, which interacts with the Query Router as if it were a single MongoDB server.

    Load Balancing: Query Routers can help distribute read and write loads across the shards, enhancing the overall performance of the database system.In larger deployments, multiple Query Routers can be used to balance the load and provide redundancy.

    Shard Management: The Query Router communicates with the cluster’s config servers to keep track of the metadata about the cluster's current state, including the distribution of data across shards.

    Simplifies Client Interaction: By abstracting the complexity of the sharded cluster, Query Routers simplify how clients interact with the database. Clients do not need to know the details of data distribution across shards.

    Write Operations: For write operations, the Query Router forwards the request to the primary replica set member of the appropriate shard.

    Caching: Query Routers cache the cluster’s metadata to quickly route queries without needing to frequently access config servers.


### MongoDB Indexes
Indexing in MongoDB is a critical feature that improves the performance of database operations, particularly in querying and sorting data. 

Purpose: Indexes in MongoDB are used to efficiently fetch data from a database. Without indexes, MongoDB must perform a full scan of a collection to select those documents that match the query statement.
    Default Index: Every MongoDB collection has an automatic index created on the _id field. The _id index is the primary key and ensures the uniqueness of each document in the collection.
    Index Types: MongoDB supports various types of indexes, catering to different types of data and queries.

Types of Indexes

1. Single Field Index: Indexes a single field of a document in either ascending or descending order. Besides the default _id index, you can create custom single field indexes.
2. Compound Index: Indexes multiple fields within a document. The order of fields listed in a compound index is significant. It determines the sort order and query capability of the index.
3. Multikey Index: Created automatically for fields that hold an array. If you index a field that contains an array, MongoDB creates separate index entries for each element of the array.
4. Text Index: Used for searching text strings. A text index stores the content of a field tokenized as words, optimized for text search operations.
5. Hashed Index: Stores the hash of the value of a field. These are primarily used in sharding scenarios to evenly distribute data across shards.
6. Partial Index: Indexes only the documents in a collection that meet a specified filter expression. This can be more efficient and consume less space than indexing all documents.
7. TTL (Time-To-Live) Index: Automatically deletes documents from a collection after a certain amount of time. This is useful for data that needs to expire, like sessions or logs.

### Use cases of MongoDB

1. Content Management Systems:
	Flexible schema accommodates various content types and changing data structures.
	Efficiently stores and retrieves diverse and complex data sets.

2. Mobile Apps:
	Scales easily with user growth.
	Offers real-time data synchronization and integration capabilities.

3. Internet of Things (IoT):
	Handles high volumes of time-series data from sensors and devices. Supports geospatial queries and real-time analytics.

4. E-commerce Applications:
	Manages diverse and evolving product catalogs.
	Offers personalized customer experiences through robust data handling.

5. Gaming Industry:
	Provides high performance for real-time analytics.
	Scales dynamically to handle fluctuating user loads.

6. Real-Time Analytics:
	Facilitates real-time data processing and aggregation. Offers quick insights from live data.

7. Catalogs and Inventory Management:
	Easily manages complex and varied product data.
	Supports fast queries for efficient inventory tracking.

8. Log Data Storage and Analysis:
	Stores large volumes of log data for analysis.
	Offers time-to-live (TTL) indexes for expiring old logs.

9. Document and Asset Management:
	Ideal for storing, retrieving, and managing document-based information. Supports rich document structures and metadata.

10. Social Networks:
	Manages dynamic and large-scale user-generated data.
	Handles complex friend networks and social graph data efficiently.

