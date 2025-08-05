### **Application > Job > Stage > Task**


![Steps](job.svg)

1. **Application**
An application in Spark refers to any command or program that you submit to your Spark cluster for execution.
Typically, one spark-submit command creates one Spark application. You can submit multiple applications, but each spark-submit initiates a distinct application.

2. **Job**
Within an application, jobs are created based on "actions" in your Spark code.
An action is an operation that triggers the computation of a result, such as collect(), count(), write(), show(), or save().
If your application contains five actions, then five separate jobs will be created.
Every job will have a minimum of one stage and one task associated with it.

3. **Stage**
A job is further divided into smaller parts called stages.
Stages represent a set of operations that can be executed together without shuffling data across the network. Think of them as logical steps in a job's execution plan. Stages are primarily defined by "wide dependency transformations".
  
    a. Wide Dependency Transformations (e.g., repartition(), groupBy(), join()) require shuffling data across partitions, meaning data from one partition might be needed by another. Each wide dependency transformation typically marks the end of one stage and the beginning of a new one.
   
    b. Narrow Dependency Transformations (e.g., filter(), select(), map()) do not require data shuffling; an output partition can be computed from only one input partition. Multiple narrow transformations can be grouped into a single stage.

4. **Task**
A task is the actual unit of work that is executed on an executor.
It performs the computations defined within a stage on a specific partition of data.
The number of tasks within a stage is directly determined by the number of partitions the data has at that point in the execution. If a stage operates on 200 partitions, it will typically launch 200 tasks.

**Relationship Summary**:
• One Application can contain Multiple Jobs.
• One Job can contain Multiple Stages.
• One Stage can contain Multiple Tasks

### **Example Spark Code Snippet**

```bash
# Assume spark_session is already created
df = spark_session.read.csv("path/to/data.csv") # Action (read is an action sometimes, specifically if inferSchema is used or it's implicitly reading)
# In this specific context, the source treats 'read' as an action that triggers a job [1, 9]

df_repartitioned = df.repartition(2) # Wide Dependency Transformation

df_filtered = df_repartitioned.filter("salary > 90000") # Narrow Dependency Transformation

df_selected = df_filtered.select("age", "salary") # Narrow Dependency Transformation

df_grouped = df_selected.groupBy("age").count() # Wide Dependency Transformation

df_grouped.collect() # Action
```

### **Step-by-Step Analysis of Execution**

1. **Job Creation**:
    The source explicitly states that read and collect are actions that create jobs.
    Therefore, this code snippet will trigger two jobs.

    ▪ Job 1: Triggered by the spark_session.read.csv() operation.

    ▪ Job 2: Triggered by the df_grouped.collect() operation.
    
2. **Stage Creation (within Job 2, as it's more complex)**:
    Remember, stages are split at wide dependency transformations.
    Initial Data State: When df is read, the source assumes it's small (e.g., less than 128MB), so it initially fits into one partition.
    
    **Stage 1 (triggered by repartition)**:
    
    ▪ df.repartition(2): This is a wide dependency transformation. It means the single initial partition will be repartitioned into two partitions.
    
    ▪ This repartition operation will mark the end of one stage and the beginning of a new one. It becomes Stage 1 of Job 2.
    
    **Stage 2 (triggered by filter and select)**:
     
     ▪ df_repartitioned.filter("salary > 90000"): This is a narrow dependency transformation.
     
     ▪ df_filtered.select("age", "salary"): This is also a narrow dependency transformation.
     
     ▪ Since both are narrow transformations and follow repartition without another wide dependency, they will be executed within the same stage, which is Stage 2 of Job 2.
    
    **Stage 3 (triggered by groupBy)**:
      
     ▪ df_selected.groupBy("age").count(): This is a wide dependency transformation. Grouping by a key requires data shuffling to bring all records with the same key to the same partition.
     
     ▪ This groupBy operation will trigger a new stage, becoming Stage 3 of Job 2.
    
    **Total Stages**:

     ▪ Job 1 (from read) would have a minimum of one stage.
     
     ▪ Job 2 (from collect) would have three stages (one for repartition, one for filter/select, and one for groupBy).
     
     ▪ Thus, the total number of stages for this entire application would be 1 + 3 = 4 stages.

3. **Task Creation (within stages of Job 2)**:

    The number of tasks in a stage depends on the number of partitions.
    
    **Job 1 Stage 1 (from read)**:
     
     ▪ Initially, the data is in one partition (assuming less than 128MB).
     
     ▪ Therefore, 1 task will be created for this stage.
    
    **Job 2 Stage 1 (from repartition)**:
     
     ▪ After repartition(2), the data is now in two partitions.
     
     ▪ Therefore, 2 tasks will be created in this stage to handle the two partitions.
    
    **Job 2 Stage 2 (from filter and select)**:
     
     ▪ These operations are on the two partitions created by repartition.
     
     ▪ Thus, 2 tasks will run in parallel for this stage, one for each partition.
    
    **Job 2 Stage 3 (from groupBy)**:
     
     ▪ When groupBy is performed, Spark, by default, creates 200 partitions for shuffle operations (like groupBy or join). Even if the input data had fewer partitions, the output of a shuffle stage will default to 200 partitions.
     
     ▪ Therefore, 200 tasks will be created for this stage, one for each of the 200 output partitions.
    
    **Total Tasks**:
     
     ▪ Job 1: 1 task.
     
     ▪ Job 2: (Stage 1: 2 tasks) + (Stage 2: 2 tasks) + (Stage 3: 200 tasks) = 204 tasks.
    
     ▪ The source shows 203 tasks as a total. This discrepancy might arise from the initial read task not being explicitly counted in the later sum, or some tasks being optimized away. However, the explanation for 2 tasks (from repartition) and 200 tasks (from groupBy default) is consistent. The sum presented in the source for the latter part of the job is 200+2 = 202, and adding the initial 1 task for the read gives 203.