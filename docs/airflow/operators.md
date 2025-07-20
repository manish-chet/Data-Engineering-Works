In Airflow, there's a task which perform 1 unique job across the DAG, the task is usually calling Airflow Operator.

An operator is essentially a Python class that defines what a task should do and how it should be executed within the context of the DAG.

- Operators can perform a wide range of tasks, such as running a Bash script or Python script, executing SQL, sending an email, or transferring files between systems.
- Operators provide a high-level abstraction of the tasks, letting us focus on the logic and flow of the workflow without getting bogged down in the implementation details.
- Apache Airflow has several types of operators that allow you to perform different types of tasks. 

## Task level Operator

!!! tip

    While Airflow provides a wide variety of operators out of the box, we may still need to create custom operators to address our specific use cases.

    All operators are extended from `BaseOperator` and we need to override two methods: `__init__` and `execute`.

    The `execute` method is invoked when the runner calls the operator.

The following example creates a custom operator `DataAnalysisOperator` that performs the requested type of analysis on an input file and saves the results to an output file.

!!! warning

    It's advised not to put expensive operations in `__init__` because it will be instantiated once per scheduler cycle.

```python
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class DataAnalysisOperator(BaseOperator):
    @apply_defaults
    def __init__(self, dataset_path, output_path, analysis_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dataset_path = dataset_path
        self.output_path = output_path
        self.analysis_type = analysis_type

    def execute(self, context):
        # Load the input dataset into a pandas DataFrame.
        data = pd.read_csv(self.dataset_path)

        # Perform the requested analysis.
        if self.analysis_type == 'mean':
            result = np.mean(data)
        elif self.analysis_type == 'std':
            result = np.std(data)
        else:
            raise ValueError(f"Invalid analysis type '{self.analysis_type}'")

        # Write the result to a file.
        with open(self.output_path, 'w') as f:
            f.write(str(result))
```

The extensibility of the operator is one of many reasons why Airflow is so powerful and popular.


!!! Tip "Tip"

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

## Sensor Operator

A special type of operator is called a sensor operator.
It's designed to wait until something happens and then succeed so their downstream tasks can run.
The DAG has a few sensors that are dependent on external files, time, etc.

Common sensor types are:

- **TimeSensor**: Wait for a certain amount of time to pass before executing a task.

- **FileSensor**: Wait for a file to be in a location before executing a task.

- **HttpSensor**: Wait for a web server to become available or return an expected result before executing a task.

- **ExternalTaskSensor**: Wait for an external task in another DAG to complete before executing a task.

We can create a custom sensor operator by extending the `BaseSensorOperator` class and overriding two methods: `__init__` and `poke`.

The `poke` method performs the necessary checks to determine whether the condition has been satisfied.
If so, return `True` to indicate that the sensor has succeeded. Otherwise, return `False` to continue checking in the next interval.

Here is an example of a custom sensor operator that pulls an endpoint until the response matches with `expected_text`.

```python
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults
import requests

class EndpointSensorOperator(BaseSensorOperator):

    @apply_defaults
    def __init__(self, url, expected_text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url
        self.expected_text = expected_text

    def poke(self, context):
        response = requests.get(self.url)
        if response.status_code != 200:
            return False
        return self.expected_text in response.text
```

#### Poke mode vs. Reschedule mode

There are two types of modes in a sensor:

- **poke**: the sensor repeatedly calls its `poke` method at the specified `poke_interval`, checks the condition, and reports it back to Airflow.
  As a consequence, the sensor takes up the worker slot for the entire execution time.

- **reschedule**: Airflow is responsible for scheduling the sensor to run at the specified `poke_interval`.
  But if the condition is not met yet, the sensor will release the worker slot to other tasks between two runs.

!!! tip

    In general, poke mode is more appropriate for sensors that require short run-time and `poke_interval` is less than five minutes.

    Reschedule mode is better for sensors that expect long run-time (e.g., waiting for data to be delivered by an external party) because it is less resource-intensive and frees up workers for other tasks.

### Backfilling

**Backfilling** is an important concept in data processing.
It refers to the process of populating or updating historical data in the system to ensure that the data is complete and up-to-date.

This is typically required in two use cases:

- **Implement a new data pipeline**: If the pipeline uses an incremental load, backfilling is needed to populate historical data that falls outside the reloading window.

- **Modify an existing data pipeline**: When fixing a SQL bug or adding a new column, we also want to backfill the table to update the historical data.

!!! warning

    When backfilling the table, we must ensure that the new changes are compatible with the existing data; otherwise, the table needs to be recreated from scratch.

    Sometimes, the backfilling job can consume significant resources due to the high volume of historical data.

    It's also worth checking any possible downstream failure before executing the backfilling job.

Airflow provides the backfilling process in its cli command.

```bash
airflow backfill [dag name] -s [start date] -e [end date]
```