#### Airflow DB Cleanup
A maintenance workflow that you can deploy into Airflow to periodically clean out the DagRun, TaskInstance, Log, XCom, Job DB and SlaMiss entries to avoid having too much data in your Airflow MetaStore.

1. Copy the airflow-db-cleanup.py file to this dags directory
```bash
wget https://github.com/manish-chet/DataEngineering/airflow/airflow-db-cleanup.py
```        
2. Update the global variables (SCHEDULE_INTERVAL, DAG_OWNER_NAME, ALERT_EMAIL_ADDRESSES and ENABLE_DELETE) in the DAG with the desired values

3. Modify the DATABASE_OBJECTS list to add/remove objects as needed. Each dictionary in the list features the following parameters:
    - airflow_db_model: Model imported from airflow.models corresponding to a table in the airflow metadata database
    - age_check_column: Column in the model/table to use for calculating max date of data deletion
    - keep_last: Boolean to specify whether to preserve last run instance
        - keep_last_filters: List of filters to preserve data from deleting during clean-up, such as DAG runs where the external trigger is set to 0. 
        - keep_last_group_by: Option to specify column by which to group the database entries and perform aggregate functions.

4. Create and Set the following Variables in the Airflow Web Server (Admin -> Variables)

    - airflow_db_cleanup__max_db_entry_age_in_days - integer - Length to retain the log files if not already provided in the conf. If this is set to 30, the job will remove those files that are 30 days old or older.

5. Enable the DAG in the Airflow Webserver

#### Airflow Log Cleanup   
A maintenance workflow that you can deploy into Airflow to periodically clean out the task logs to avoid those getting too big.

1. Copy the airflow-log-cleanup.py file to this dags directory
```bash
wget https://github.com/manish-chet/DataEngineering/airflow/airflow-log-cleanup.py
```
2. Update the global variables (SCHEDULE_INTERVAL, DAG_OWNER_NAME, ALERT_EMAIL_ADDRESSES, ENABLE_DELETE and NUMBER_OF_WORKERS) in the DAG with the desired values

3. Create and Set the following Variables in the Airflow Web Server (Admin -> Variables)

    - airflow_log_cleanup__max_log_age_in_days - integer - Length to retain the log files if not already provided in the conf. If this is set to 30, the job will remove those files that are 30 days old or older.
    - airflow_log_cleanup__enable_delete_child_log - boolean (True/False) - Whether to delete files from the Child Log directory defined under [scheduler] in the airflow.cfg file

4. Enable the DAG in the Airflow Webserver

#### Airflow Webserver - LDAP Authentication Configuration

A webserver config file to integrate Airflow with LDAP and RBAC

1. Copy the airflow-log-cleanup.py file to this dags directory
```bash
wget https://github.com/manish-chet/DataEngineering/airflow/webserver_config.py
```
2. Run the command airflow webserver -D