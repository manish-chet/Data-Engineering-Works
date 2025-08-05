## **Spark Architecture**
![Steps](sparkarc.svg)
 

1. **Driver Program**: The driver program is the heart of a Spark application. It runs the main() function of an application and is the place where the SparkContext is created. SparkContext is responsible for coordinating and monitoring the execution of tasks. The driver program defines datasets and applies operations (transformations & actions) on them.

2. **SparkContext**: The SparkContext is the main entry point for Spark functionality. It represents the connection to a Spark cluster and can be used to create RDDs, accumulators, and broadcast variables on that cluster.

3. **Cluster Manager**: SparkContext connects to the cluster manager, which is responsible for the allocation of resources (CPU, memory, etc.) in the cluster. The cluster manager can be Spark's standalone manager, Hadoop YARN, Mesos, or Kubernetes.

4. **Executors**: Executors are worker nodes' processes in charge of running individual tasks in a given Spark job. They run concurrently across different nodes. Executors have two roles. Firstly, they run tasks that the driver sends. Secondly, they provide in-memory storage for RDDs.

5. **Tasks**: Tasks are the smallest unit of work in Spark. They are transformations applied to partitions. Each task works on a separate partition and is executed in a separate thread in executors.

6. **RDD**: Resilient Distributed Datasets (RDD) are the fundamental data structures of Spark. They are an immutable distributed collection of objects, which can be processed in parallel. RDDs can be stored in memory between queries without the necessity for serialization.

7. **DAG (Directed Acyclic Graph)**: Spark represents a series of transformations on data as a DAG, which helps it optimize the execution plan. DAG enables pipelining of operations and provides a clear plan for task scheduling.
Spark Architecture & Its components

8. **DAG Scheduler**: The Directed Acyclic Graph (DAG) Scheduler is responsible for dividing operator graphs into stages and sending tasks to the Task Scheduler. It translates the data transformations from the logical plan (which represents a sequence of transformations) into a physical execution plan. It optimizes the plan by rearranging and combining operations where possible, groups them into stages, and then submits the stages to the Task Scheduler.

9. **Task Scheduler**: The Task Scheduler launches tasks via cluster manager. Tasks are the smallest unit of work in Spark, sent by the DAG Scheduler to the Task Scheduler. The Task Scheduler then launches the tasks on executor JVMs. Tasks for each stage are launched in as many parallel operations as there are partitions for the dataset.

10. **Master**: The Master is the base of a Spark Standalone cluster (specific to Spark's standalone mode, not applicable if Spark is running on YARN or Mesos). It's the central point and entry point of the Spark cluster. It is responsible for managing and distributing tasks to the workers. The Master communicates with each of the workers periodically to check if it is still alive and if it has completed tasks.

11. **Worker**: The Worker is a node in the Spark Standalone cluster (specific to Spark's standalone mode). It receives tasks from the Master and executes them. Each worker has multiple executor JVMs running on it. It communicates with the Master and Executors to facilitate task execution.The worker is responsible for managing resources and providing an execution environment for the executor JVMs.

## **What happens behind the scenes**

   | Step | What Happens                                                                |
   | ---- | --------------------------------------------------------------------------- |
   | 1️⃣  | You launch the application. Spark creates a **SparkContext** in the Driver. |
   | 2️⃣  | Spark connects to the **Cluster Manager** (e.g., YARN, standalone, k8s).    |
   | 3️⃣  | Cluster Manager allocates **Workers** and **starts Executors**.             |
   | 4️⃣  | RDD transformations are converted into a **DAG** (Directed Acyclic Graph).  |
   | 5️⃣  | Spark creates **Stages**, breaks them into **Tasks** (based on partitions). |
   | 6️⃣  | **Tasks** are shipped to Executors.                                         |
   | 7️⃣  | Executors run the tasks and return results back to the Driver.              |
   | 8️⃣  | Final results (e.g., word count) are written to HDFS.                       |


## **Spark Standalone**
![Steps](sparkstandalone.svg)

Spark Standalone mode is a built-in cluster manager in Apache Spark that enables you to set up a dedicated Spark cluster without needing external resource managers like Hadoop YARN or Kubernetes.

It is easy to deploy, suitable for development and testing, and supports distributed data processing across multiple nodes.

**Advantages of Spark Standalone**

1. Easy to set up and manage
2. No need for external resource managers
3. Built-in web UI for monitoring
4. Supports HA (High Availability) with ZooKeeper

**Limitations**

1. Less fault-tolerant than YARN or Kubernetes
2. Limited support for resource isolation and fairness
3. Not recommended for large-scale production


## **Spark with YARN**

![Steps](yarn.svg)

Apache Spark on YARN means running Spark applications on top of Hadoop YARN (Yet Another Resource Negotiator) — the resource manager in Hadoop ecosystems. This setup allows Spark to share cluster resources with other big data tools (like Hive, HBase, MapReduce) in a multi-tenant environment.

YARN handles resource management, job scheduling, and container allocation, while Spark focuses on data processing.

1. **Resource Manager**: It controls the allocation of system resources on all applications. A Scheduler and an Application Master are included. Applications receive resources from the Scheduler.

2. **Node Manager**: Each job or application needs one or more containers, and the Node Manager monitors these containers and their usage. Node Manager consists of an Application Master and Container. The Node Manager monitors the containers and resource usage, and this is reported to the Resource Manager.

3. **Application Master**: The ApplicationMaster (AM) is an instance of a framework-specific library and serves as the orchestrating process for an individual application in a distributed environment.

**Advantages**

1. Leverages existing Hadoop cluster (no separate setup)
2. Resource sharing across Hadoop ecosystem
3. Supports HDFS, Hive, HBase integration natively
4. Production-grade scalability and stability

**Considerations**

1. Slight overhead from YARN’s container management
2. Configuration tuning (memory, executor placement) is important
3. YARN needs to be properly secured (Kerberos, ACLs)

