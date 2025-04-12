# Kafka Installation with ZooKeeper (On-Premise)
## 🚀 Prerequisites

- 3 VMs (Ensure pre-requisites like SELinux disabled, firewall off, THP disabled, etc.)
- Java 8 or higher
- Sufficient disk space
- Network connectivity


## 🛠️ Production Considerations

### 🧠 Kernel & OS Tuning

```bash
vm.swappiness = 1
vm.dirty_background_ratio = 10    # Consider 5 for certain workloads
vm.dirty_ratio = 20
```

📊 To monitor dirty pages:
```bash
cat /proc/vmstat | egrep "dirty|writeback"
```
Example output:
```text
nr_dirty 3875
nr_writeback 29
nr_writeback_temp 0
```

### 🌐 Networking Parameters

```bash
net.core.wmem_default = 131072
net.core.rmem_default = 131072
net.core.wmem_max     = 2097152
net.core.rmem_max     = 2097152
net.ipv4.tcp_window_scaling = 1

net.ipv4.tcp_wmem = 4096 65536 2048000
net.ipv4.tcp_rmem = 4096 65536 2048000
net.ipv4.tcp_max_syn_backlog = 4096
net.core.netdev_max_backlog = 5000
```

### 🧹 GC Tuning (for 64GB system with 5GB heap)

```bash
-XX:MaxGCPauseMillis=20
-XX:InitiatingHeapOccupancyPercent=35
```

---

## 🔧 Step-by-Step Installation (Repeat on All Nodes)

3. **Configure certificates**  
   📄 [Download cert.sh](../../files/zk_kafka/cert.sh)

2. **Download ZooKeeper**
   ```bash
   wget https://downloads.apache.org/zookeeper/zookeeper-3.8.1/apache-zookeeper-3.8.1-bin.tar.gz
   tar -xzf apache-zookeeper-3.8.1-bin.tar.gz
   cd apache-zookeeper-3.8.1-bin/conf/
   ```

3. **Configure `zoo.cfg`**  
   📄 [Download zoo.cfg](../../files/zk_kafka/zoo.cfg)

4. **Configure `jaas.conf`**  
   📄 [Download jaas.conf](../../files/zk_kafka/zk_jaas.conf)

5. **Configure `java.env`**  
   📄 [Download java.env](../../files/zk_kafka/java.env)

6. **Configure `myid`**
   ```bash
   echo 1 > /data/kafka/zookeeper/data/myid
   # Change the value for each node (e.g., 1, 2, 3)
   ```

7. **Start ZooKeeper**
   ```bash
   bin/zkServer.sh start
   ```

8. **Verify ZooKeeper via zkCli**
   ```bash
   bin/zkCli.sh -server hostname1:12182
   ```

9. **Download Kafka**
   ```bash
   wget https://downloads.apache.org/kafka/3.6.1/kafka_2.13-3.6.1.tgz
   tar -xzf kafka_2.13-3.6.1.tgz
   cd kafka_2.13-3.6.1
   ```

10. **Configure `server.properties`**  
    📄 [Download server.properties](../../files/zk_kafka/server.properties)

11. **Configure `kafka_jaas.conf`**  
    📄 [Download kafka_jaas.conf](../../files/zk_kafka/kafka_jaas.conf)

12. **Configure Kafka Environment**  
    📄 [Download kafka.env](../../files/zk_kafka/kafka.env)

13. **Create Admin User**
    ```bash
    kafka_2.13-3.4.0/bin/kafka-configs.sh \
    --zookeeper hostname1:12182 \
    --alter --add-config 'SCRAM-SHA-512=[password="password"]' \
    --entity-type users --entity-name admin
    ```

14. **Start Kafka Server**
    ```bash
    bin/kafka-server-start.sh -daemon config/server.properties
    ```

15. **Common Kafka Commands**

```bash
# Create Admin User
kafka-configs.sh --zookeeper hostname1:12182 \
  --alter --add-config 'SCRAM-SHA-512=[password="password"]' \
  --entity-type users --entity-name admin

# Grant Producer Rights
kafka-acls.sh --authorizer-properties zookeeper.connect=hostname1:12182 \
  --add --allow-principal User:dlkdeveloper --producer \
  --topic RRA_DL_TEST --resource-pattern-type prefixed

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
kafka-topics.sh --delete --topic RRA_DL_TEST \
  --bootstrap-server hostname1:6667 \
  --command-config /data1/kafkacerts/admin.properties
```

---

## ❗ Common Issues

- ❓ Is ZooKeeper running?
- 🌐 Network/firewall issues?
- ☕ Java installed and accessible?
- 💽 Disk space sufficient?
- 📋 Check Kafka logs!

---

## 🔄 Related Topics

- [Kafka Installation with KRaft](kafka_install_kraft.md)
- [Back to Kafka Overview](../kafka.md)

