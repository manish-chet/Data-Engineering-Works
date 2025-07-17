Apache Hadoop YARN (Yet Another Resource Negotiator) is a resource management layer in Hadoop. YARN came into the picture with the introduction of Hadoop 2.x. It allows various data processing engines such as interactive processing, graph processing, batch processing, and stream processing to run and process data stored in HDFS (Hadoop Distributed File System).

In essence, YARN is responsible for managing cluster resources, which include CPU, memory, disk I/O, and network bandwidth. It provides APIs that computation engines use to request and work with Hadoop cluster resources for their task scheduling and resource requirements. It's important to note that YARN APIs are not designed for individual application developers; instead, they target teams creating new computation engines. The ambition of YARN is to consolidate all types of distributed computation capabilities into a single cluster, thereby eliminating the need for multiple clusters and the associated pain of data movement or duplication. Popular execution engines that operate on top of YARN include Apache Spark, Apache Storm, Apache Solr, and Apache Tez. While some NoSQL databases like Cassandra are not yet YARN-enabled, an incubating Apache project called Slider aims to integrate them into a YARN-managed Hadoop cluster, including existing implementations for HBase and Accumulo, without requiring changes to those systems themselves. Apache Slider also seeks to introduce on-demand scale-up and scale-down capabilities, offering elasticity similar to cloud providers.

### **Components of YARN**

#### Resource Manager 
Resource Manager is the master daemon of YARN. It is responsible for managing several other applications, along with the global assignments of resources such as CPU and memory. It is used for job scheduling. Resource Manager has two components:

a. Scheduler: Schedulers’ task is to distribute resources to the running applications. It only deals with the scheduling of tasks and hence it performs no tracking and no monitoring of applications.

b. Application Manager: The application Manager manages applications running in the cluster. Tasks, such as the starting of Application Master or monitoring, are done by the Application Manager.

#### Node Manager
Node Manager is the slave daemon of YARN. It has the following responsibilities:

a. Node Manager has to monitor the container’s resource usage, along with reporting it to the Resource Manager.

b. The health of the node on which YARN is running is tracked by the Node Manager.

c. It takes care of each node in the cluster while managing the workflow, along with user jobs on a particular node.

d. It keeps the data in the Resource Manager updated

e. Node Manager can also destroy or kill the container if it gets an order from the Resource Manager to do so.

#### Application Master
Every job submitted to the framework is an application, and every application has a specific Application Master associated with it. Application Master performs the following tasks:

It coordinates the execution of the application in the cluster, along with managing the faults.

It negotiates resources from the Resource Manager.

It works with the Node Manager for executing and monitoring other components’ tasks.

At regular intervals, heartbeats are sent to the Resource Manager for checking its health, along with updating records according to its resource demands.

Now, we will step forward with the fourth component of Apache Hadoop YARN.

#### Container
A container is a set of physical resources (CPU cores, RAM, disks, etc.) on a single node. The tasks of a container are listed below:
   It grants the right to an application to use a specific amount of resources (memory, CPU, etc.) on a specific host.
   YARN containers are particularly managed by a Container Launch context which is Container Life Cycle
   (CLC). This record contains a map of environment variables, dependencies stored in remotely accessible storage, security tokens, the payload for Node Manager services, and the command necessary to create the process.


#### **Running and application through YARN**


![Steps](yarnnew.svg)

When an application is submitted to YARN, the request goes to the Resource Manager, which then instructs a Node Manager to launch the first container for that application, known as the Application Master. The Application Master then assumes responsibility for executing and monitoring the entire job, with its specific functionality varying depending on the application framework (e.g., MapReduce Application Master functions differently than a Spark Application Master). For a MapReduce application, the Application Master requests more containers from the Resource Manager to initiate map and reduce tasks. Once these containers are allocated, the Application Master directs the Node Managers to launch the containers and execute the tasks. Tasks directly report their status and progress back to the Application Master. Upon completion of all tasks, all containers, including the Application Master, perform necessary cleanup and terminate.


1.	Application Submission: The RM accepts the application, causing the creation of an ApplicationMaster (AM) instance. The AM is responsible for negotiating resources from the RM and working with the Node Managers (NMs) to execute and monitor the tasks.

2.	Resource Request: The AM starts by requesting resources from the RM. It specifies what resources are needed, in which locations, and other constraints. These resources are encapsulated in terms of "Resource Containers" which include specifications like memory size, CPU cores, etc.

3.	Resource Allocation: The Scheduler in the RM, based on the current system load and capacity, as well as policies (e.g., capacity, fairness), allocates resources to the applications by granting containers. The specific strategy depends on the scheduler type (e.g., FIFO, Capacity Scheduler).

4.	Container Launching: Post-allocation, the RM communicates with relevant NMs to launch the containers. The Node Manager sets up the container's environment, then starts the container by executing the specified commands.

5.	Task Execution: Each container then runs the task assigned by the ApplicationMaster. These are actual data processing tasks, specific to the application's purpose.

6.	Monitoring and Fault Tolerance: The AM monitors the progress of each task. If a container fails, the AM requests a new container from the RM and retries the task, ensuring fault tolerance in the execution phase.

7.	Completion and Release of Resources: Upon task completion, the AM releases the allocated containers, freeing up resources. After all tasks are complete, the AM itself is terminated, and its resources are also released.

8.	Finalization: The client then polls the RM or receives a notification to know the status of the application. Once informed of the completion, the client retrieves the result and finishes the process.