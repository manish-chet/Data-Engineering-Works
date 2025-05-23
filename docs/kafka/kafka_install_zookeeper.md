# Kafka Installation with ZooKeeper

## Prerequisites

- 3 VMs (Ensure pre-requisites like SELinux disabled, firewall off, THP disabled, etc.)
- Java 8 or higher
- Sufficient disk space
- Network connectivity

## VM settings

???-  "Kernel & OS tuning"
      ```bash
      vm.swappiness = 1
      vm.dirty_background_ratio = 10 # Consider 5 for certain workloads
      vm.dirty_ratio = 20
      ```

???-  "Networking Parameters "
      ```bash
      net.core.wmem_default = 131072
      net.core.rmem_default = 131072
      net.core.wmem_max  = 2097152
      net.core.rmem_max  = 2097152
      net.ipv4.tcp_window_scaling = 1
      net.ipv4.tcp_wmem = 4096 65536 2048000
      net.ipv4.tcp_rmem = 4096 65536 2048000
      net.ipv4.tcp_max_syn_backlog = 4096
      net.core.netdev_max_backlog = 5000
      ```

???-  "GC Tuning"
    ```bash
    (for 64GB system with 5GB heap)
    -XX:MaxGCPauseMillis=20
    -XX:InitiatingHeapOccupancyPercent=35
    ```

## Certs Creation
???-  "Creating certificates for SASL_SSL"
    ```bash
    wget https://github.com/manish-chet/DataEngineering/blob/main/kafkawithzk/cert.sh
    To execute - use bash cert.sh hostname
    ```

## Zookeeper Installation

???-  "Download tar file from apache zookeeper"
    ```bash
    wget https://downloads.apache.org/zookeeper/zookeeper-3.8.1/apache-zookeeper-3.8.1-bin.tar.gz
    tar -xzf apache-zookeeper-3.8.1-bin.tar.gz
    cd apache-zookeeper-3.8.1-bin/conf/
    ```

???-  "Configure zookeeper properties"

    ```bash
    wget https://github.com/manish-chet/DataEngineering/blob/main/kafkawithzk/zoo.cfg
    Copy the above file in zookeeper conf directory
    ```

???-  "create jaas conf file for authentication"
    ```bash
    wget https://github.com/manish-chet/DataEngineering/blob/main/kafkawithzk/jaas.conf
    Copy the above file in zookeeper conf directory
    ```

???-  "Configure the Java Env variables"
    ```bash
    wget https://github.com/manish-chet/DataEngineering/blob/main/kafkawithzk/java.env
    Copy the above file in zookeeper conf directory
    ```

???-  "Create Id for each zk node"
    ```bash
    echo 1 > /data/kafka/zookeeper/data/myid
    # Change the value for each node (e.g., 1, 2, 3)
    ```

???-  "Start zookeper server one each node"
    ```bash
    bin/zkServer.sh start
    ```

???-  "Login to cli and verify the status "
    ```bash
    bin/zkCli.sh -server hostname1:12182
    ```

## Kafka Installation

???-  "Download tar file from apache kafka"
    ```bash
    wget https://downloads.apache.org/kafka/3.6.1/kafka_2.13-3.6.1.tgz
    tar -xzf kafka_2.13-3.6.1.tgz
    cd kafka_2.13-3.6.1
    ```

???-  "Configure server.properties"
    ```bash
    wget https://github.com/manish-chet/DataEngineering/blob/main/kafkawithzk/server.properties
    Copy the above file in kafka conf directory
    ```

???-  "Create kafka_jaas.conf file for authentication"
    ```bash
    wget https://github.com/manish-chet/DataEngineering/blob/main/kafkawithzk/kafka_jaas.conf
    Copy the above file in kafka conf directory
    ```

???-  "Configure KAFKA_OPTS and KAFKA-ENV properties"
    ```bash
    wget https://github.com/manish-chet/DataEngineering/blob/main/kafkawithzk/kafka.env
    Copy the above file in kafka conf directory or set in bashrc
    ```

???-  "Create Admin user for Kafka Server"
    ```bash
    kafka_2.13-3.4.0/bin/kafka-configs.sh \
    --zookeeper hostname1:12182 \
    --alter --add-config 'SCRAM-SHA-512=[password="password"]' \
    --entity-type users --entity-name admin
    ```

???-  "Start the Kafka Server"
    ```bash
    bin/kafka-server-start.sh -daemon config/server.properties
    ```

???-  "Kafka ACl commands for authorization"

    ```bash
    # Create Admin User
    kafka-configs.sh --zookeeper hostname1:12182 \
      --alter --add-config 'SCRAM-SHA-512=[password="password"]' \
      --entity-type users --entity-name admin

    # Grant Producer Rights
    kafka-acls.sh --authorizer-properties zookeeper.connect=hostname1:12182 \
      --add --allow-principal User:dlkdeveloper --producer \
      --topic TEST --resource-pattern-type prefixed

    # Grant Consumer Rights
    kafka-acls.sh --authorizer-properties zookeeper.connect=hostname1:12182 \
      --add --allow-principal User:$1 --consumer \
      --group $1 --topic $2 --resource-pattern-type prefixed

    # List ACLs
    kafka-acls.sh --list --authorizer-properties zookeeper.connect=hostname1:12182

    # List Topics
    kafka-topics.sh --list \
      --command-config /data1/kafkacerts/admin.properties \
      --bootstrap-server hostname2:6667

    # Delete Topics
    kafka-topics.sh --delete --topic DL_TEST \
      --bootstrap-server hostname1:6667 \
      --command-config /data1/kafkacerts/admin.properties
    ```
