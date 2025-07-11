### Opeartors in Airflow
Apache Airflow has several types of operators that allow you to perform different types of tasks. 
Here are some of the most common ones:

    BashOperator: Executes a bash command.
    PythonOperator: Calls a Python function.
    EmailOperator: Sends an email.
    SimpleHttpOperator: Sends an HTTP request.
    MySqlOperator, SqliteOperator, PostgresOperator, MsSqlOperator, OracleOperator, etc.: Executes a SQL command.
    DummyOperator: A placeholder operator that does nothing.
    Sensor: Waits for a certain time, file, database row, S3 key, etc. There are many types of sensors, like HttpSensor, SqlSensor, S3KeySensor, TimeDeltaSensor, ExternalTaskSensor, etc.
    SSHOperator: Executes commands on a remote server using SSH.
    DockerOperator: Runs a Docker container.
    SparkSubmitOperator: Submits a Spark job.
    Operators in Airflow 
    S3FileTransformOperator: Copies data from a source S3 location to a temporary location on the local filesystem, transforms the data, and then uploads it to a destination S3 location.
    S3ToRedshiftTransfer: Transfers data from S3 to Redshift.
    EmrAddStepsOperator: Adds steps to an existing EMR (Elastic Map Reduce) job flow.
    EmrCreateJobFlowOperator: Creates an EMR JobFlow, i.e., a cluster.
    AthenaOperator: Executes a query on AWS Athena.
    AwsGlueJobOperator: Runs an AWS Glue Job.
    S3DeleteObjectsOperator: Deletes objects from an S3 bucket.
    BigQueryOperator: Executes a BigQuery SQL query.
    BigQueryToBigQueryOperator: Copies data from one BigQuery table to another.
    DataprocClusterCreateOperator: This operator is used to create a new cluster of machines on GCP's Dataproc service.
    DataProcPySparkOperator: This operator is used to submit PySpark jobs to a running Dataproc cluster.
    DataProcSparkOperator: This operator is used to submit Spark jobs written in Scala or Java to a running Dataproc cluster.
    DataprocClusterDeleteOperator: This operator is used to delete an existing cluster.