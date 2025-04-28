# 🚀 Apache Airflow Setup Guide (MySQL + RabbitMQ + Celery + Flower UI)

## 🌟 Prerequisites

- 🖥️ 3 VMs (Ensure SELinux disabled, firewall off, THP disabled, etc.)
- ☕ Java 8 or higher
- 💽 Sufficient disk space
- 🌐 Network connectivity
- 🐍 Python 3

---

## 🔧 Step-by-Step Installation

### 1️⃣ Install MySQL/PostgreSQL

```bash
yum -y install @mysql

# Start MySQL service and create symlink
systemctl status mysqld
systemctl start mysqld
systemctl enable --now mysqld
systemctl status mysqld

# Change root password and configure MySQL
mysql_secure_installation  # {password:-root}

# Create airflow user and grant privileges
mysql -u"root" -p"root"

# Inside MySQL prompt
CREATE DATABASE airflow;
CREATE USER 'airflowuser'@'%' IDENTIFIED BY 'airflowuser';
GRANT ALL PRIVILEGES ON airflow.* TO 'airflowuser'@'%';

CREATE USER 'airflowuser'@'localhost' IDENTIFIED BY 'airflowuser';
GRANT ALL PRIVILEGES ON airflow.* TO 'airflowuser'@'localhost';

FLUSH PRIVILEGES;
```

---

### 2️⃣ Install and Setup RabbitMQ

📄 [Download rabbitmq.conf]

```bash
# Extract the RabbitMQ setup file
# Edit the rabbitmq.conf

# Set environment variables in bashrc
export RABBITMQ_LOG_BASE=/data/rabbitmq/rabbitmq/logs
export PATH=$PATH:/data/rabbitmq/rabbitmq/rabbitmq_server-3.13.7/sbin

# Create the conf file

# Start the server and create Airflow user
rabbitmq-plugins enable rabbitmq_management
sbin/rabbitmqctl shutdown
rabbitmq-server -detached
rabbitmqctl add_user airflow airflow
rabbitmqctl set_user_tags airflow administrator
rabbitmqctl set_permissions -p / airflow ".*" ".*" ".*"
rabbitmqctl eval 'application:set_env(rabbit, consumer_timeout, undefined).'
```

---

### 3️⃣ Install Airflow and Setup

📄 [Download airflow.cfg]
📄 [Download webserver_config.py]

```bash
pip install virtualenv
python3.8 -m pip install --upgrade pip
virtualenv -p python3.8 airflow_env
source airflow_env/bin/activate

pip install "apache-airflow==2.10.2" --constraint constraints.txt

airflow version

# Create users
airflow create_user -r Admin -u airflow -e your_email@domain.com -f Airflow -l Admin -p password
airflow users create -r Admin -u manishkumar2.c -f manishkumar -l chetpalli -e manishkumar2.c@email.com -p manish123

# Initialize and run Airflow services
airflow db migrate
airflow webserver -D
airflow scheduler -D
airflow celery worker -D
airflow celery flower -D
airflow triggerer -D
```