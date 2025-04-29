# Apache Airflow Overview

## What is Apache Airflow?

Apache Airflow is an open-source platform to **programmatically author**, **schedule**, and **monitor** workflows. It allows you to orchestrate complex computational workflows using Python.

---

## Key Concepts

| Term            | Description |
|-----------------|-------------|
| **DAG (Directed Acyclic Graph)** | Defines a workflow with tasks and their dependencies |
| **Operator**    | Defines a single task (e.g., BashOperator, PythonOperator) |
| **Task**        | A unit of work within a DAG |
| **TaskInstance**| A specific run of a task |
| **Scheduler**   | Triggers tasks at the right time |
| **Executor**    | Handles task execution |
| **Web UI**      | UI to monitor, trigger and debug workflows |

---

## Core Components

- **Scheduler**: Monitors DAGs and triggers task executions.
- **Executor**: Executes tasks (e.g., Sequential, Local, Celery, Kubernetes).
- **Metadata Database**: Stores state of DAGs, tasks, and other Airflow metadata.
- **Web Server**: Provides a user-friendly interface to manage workflows.
- **Workers**: Executes tasks when using distributed executors like Celery or Kubernetes.

---

## Common Use Cases

- ETL pipelines
- ML model training & deployment
- Data validation and quality checks
- Data warehouse loading
- Report generation

---

