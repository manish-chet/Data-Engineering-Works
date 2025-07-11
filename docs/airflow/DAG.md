### How to write AirFlow DAG Script?
    ```bash
    # Import necessary libraries
    from datetime import datetime, timedelta
    from airflow import DAG
    from airflow.operators.dummy_operator import DummyOperator

    # Define the default_args dictionary 
    default_args = {
    'owner': 'airflow',
    'depends_on_past': False, 'email_on_failure': False, 'email_on_retry': False,
    'email': ['your-email@example.com'], 'retries': 1,
    'retry_delay': timedelta(minutes=5) 
    }

    # Instantiate a DAG 
    dag = DAG(
    'example_dag', default_args=default_args, description='An example DAG', schedule_interval=timedelta(days=1), start_date=datetime(2022, 1, 1), catchup=False,
    tags=['example']
    )

    # Define tasks and set their dependencies
    start_task = DummyOperator(task_id='start', dag=dag) end_task = DummyOperator(task_id='end', dag=dag)
    start_task >> end_task
    ```
Attribute Description

1.	'owner': 'airflow' -> The owner of the task, using it can help identify the person who should be notified in case of task/job issues.
2.	'depends_on_past': False ->  If set to True, the task instance will fail if the previous task did not succeed.
3.	'email_on_failure': False -> If set to True, Airflow will email the address specified in the 'email' key upon task failure.
4.	'email_on_retry': False -> If set to True, Airflow will email the address specified in the 'email' key if the task needs to be retried.
5.	'email': ['your-email@example.com'] -> List of email addresses to notify if defined conditions such as failure or retries are met.
6.	'retries': 1 -> Number of retries in case of task failure.
7.	'Retry_delay': timedelta(minutes=5) -> Time delay between retries.
8.	'example_dag' -> Unique string identifier for the DAG.
9.	default_args=default_args -> Dictionary of parameters & their default values.
10.	description='An example DAG' -> String describing the purpose of the DAG.
11.	schedule_interval=timedelta(days=1) -> How often the DAG should run. Uses cron-like string, or timedelta objects.
12.	start_date=datetime(2022, 1, 1) -> The earliest logical date for starting the DAG.
13.	catchup=False -> If set to True, then the DAG will catch up for all the missed runs since 'start_date'.
14.	tags=['example'] -> List of tags that can be used for filtering in the UI.




### How to execute tasks parallelly?
    ```bash
    start_task = DummyOperator(task_id='start_task', dag=dag)
    parallel_task_1 = DummyOperator(task_id='parallel_task_1', dag=dag) 
    parallel_task_2 = DummyOperator(task_id='parallel_task_2', dag=dag) 
    parallel_task_3 = DummyOperator(task_id='parallel_task_3', dag=dag) 
    end_task = DummyOperator(task_id='end_task', dag=dag)
    # Setting up the dependencies start_task >> [parallel_task_1, parallel_task_2, parallel_task_3] >> end_task
    ```
In this example, the three parallel tasks (parallel_task_1, parallel_task_2, parallel_task_3) are specified as a list in the dependency chain. The start_task runs first. Once it completes, all three parallel tasks begin. When all three of them complete, the end_task starts.

### How to overwrite depends_on_past property?
The depends_on_past attribute in the default_args dictionary of a DAG applies globally to all tasks in the DAG when set. However, if you want to override this behavior for specific tasks, you can specify the depends_on_past attribute directly on those tasks.

For specific tasks where you want to override this behavior, set depends_on_past directly on the task:
    ```bash
    task_with_custom_dep = DummyOperator(     
        task_id='task_with_custom_dep',
        depends_on_past=False, 
        dag=dag
        )
    ```
