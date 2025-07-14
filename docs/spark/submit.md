spark-submit is a command-line interface to submit your Spark applications to run on a cluster. It can use a number of supported master URL's to distribute your application across a cluster, or can run the application locally.

Here is the general structure of the spark-submit command:
   
    spark-submit \
    --class <main-class> \
    --master <master-url> \
    --deploy-mode <deploy-mode> \
    --conf <key>=<value> \
    <application-jar> \
    [application-arguments]

    --class: This is the entry point for your application, i.e., where your main method runs. For Java and Scala, this would be a fully qualified class name.

    --master: This is the master URL for the cluster. It can be a URL for any Spark-supported cluster manager. For example, local for local mode, spark://HOST:PORT for standalone mode, mesos://HOST:PORT for Mesos, or yarn for YARN.

    --deploy-mode: This can be either client (default) or cluster. In client mode, the driver runs on the machine from which the job is submitted. In cluster mode, the framework launches the driver inside the cluster.

    --conf: This is used to set any Spark property. For example, you can set Spark properties like spark.executor.memory, spark.driver.memory, etc.

    <application-jar>: This is a path to your compiled Spark application.
    
    [application-arguments]: These are arguments that you need to pass to your Spark application


For example, if you have a Spark job written in Python and you want to run it on a local machine, your spark-submit command might look like this:

    spark-submit \
    --master local[4] \
    --py-files /path/to/other/python/files \   /path/to/your/python/application.py \   arg1 arg2

    In this example, --master local[4] means the job will run locally with 4 worker threads (essentially, 4 cores). --py-files is used to add .py, .zip or .egg files to be distributed with your application. Finally, arg1 and arg2 are arguments that will be passed to your Spark application.

### Prod Spark submit

Example:

    spark-submit \
    --master spark://10.0.0.1:7077 \
    --deploy-mode client \
    --executor-memory 4G \
    --driver-memory 2G \
    --conf spark.app.name=WordCountApp \
    --conf spark.executor.cores=2 \
    --conf spark.executor.instances=5 \
    --conf spark.default.parallelism=20 \
    --conf spark.driver.maxResultSize=1G \
    --conf spark.network.timeout=800 \
    --py-files /path/to/other/python/files.zip \
    /path/to/your/python/wordcount.py \   /path/to/input/textfile.txt 
  

Explaination:

    --master spark://10.0.0.1:7077 tells Spark to connect to a standalone Spark cluster at the given IP address.
    --deploy-mode client tells Spark to run the driver program on the machine that the job is submitted from, as opposed to within one of the worker nodes.
    --executor-memory 4G and --driver-memory 2G set the amount of memory for the executor and driver processes, respectively.
    --conf spark.app.name=WordCountApp sets a name for your application, which can be useful when monitoring your cluster.
    --conf spark.executor.cores=2 sets the number of cores to use on each executor.
    --conf spark.executor.instances=5 sets the number of executor instances
    --conf spark.default.parallelism=20 sets the default number of partitions in RDDs returned by transformations like join(), reduceByKey(), and parallelize() when not set by user.
    --conf spark.driver.maxResultSize=1G limits the total size of the serialized results of all partitions for each Spark action (e.g., collect). This should be at least as large as the largest object you want to collect.
    --conf spark.network.timeout=800 sets the default network timeout value to 800 seconds. This configuration plays a vital role in cases where you deal with large shuffles.
    --py-files /path/to/other/python/files.zip adds Python .zip, .egg or .py files to distribute with your application. If you have Python files that your wordcount.py depends on, you can bundle them into a .zip or .egg file and pass it with --py-files.
    /path/to/your/python/wordcount.py is the path to the Python file that contains your Spark application.
    /path/to/input/textfile.txt is an argument that will be passed to your Spark application. In this case, it's a path to the text file that your WordCount application will process.
