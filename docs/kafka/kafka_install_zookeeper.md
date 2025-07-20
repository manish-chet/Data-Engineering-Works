# **Kafka Installation with ZooKeeper**

## **Prerequisites**

- 3 VMs (Ensure pre-requisites like SELinux disabled, firewall off, THP disabled, etc.)
- Java 8 or higher
- Sufficient disk space
- Network connectivity

## **VM settings**

!!!-  "Kernel & OS tuning"
    ```
    vm.swappiness = 1
    vm.dirty_background_ratio = 10 # Consider 5 for certain workloads
    vm.dirty_ratio = 20
    ```

!!!-  "Networking Parameters "
    ```
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

!!!-  "GC Tuning"
    ```
    (for 64GB system with 5GB heap)
    -XX:MaxGCPauseMillis=20
    -XX:InitiatingHeapOccupancyPercent=35
    ```

## **Certs Creation**
!!!-  "Creating certificates for SASL_SSL"
    ```
    #!/bin/
    # Generates several self-signed keys <name>.cer, <name>.jks, and <name>.p12.
    # Truststore is set with name truststore.jks and set password of password12345
    # Usage: createKey.sh <user> <password>
    #createKey.sh somebody password123
    # -ext "SAN=DNS:"
    export NAME=$1
    export IP1=$2
    export PASSWORD=7ecETGlHjzs
    export STORE_PASSWORD=7ecETGlHjzs
    echo "Creating key for $NAME using password $PASSWORD"
    keytool -genkey -alias $NAME -keyalg RSA -keysize 4096 -dname "CN=$NAME,OU=RRA,O=ABC,L=ABC,ST=ABC,C=IN" -ext "SAN=DNS:$NAME,IP:$IP1" -keypass $PASSWORD -keystore $NAME.jks -storepass $PASSWORD -validity 7200
    keytool -export -keystore $NAME.jks -storepass $PASSWORD -alias $NAME -file $NAME.cer
    keytool -import -trustcacerts -file $NAME.cer -alias $NAME -keystore truststore.jks -storepass $STORE_PASSWORD -noprompt
    echo "Done creating key for $NAME"
    keytool -list -keystore truststore.jks -storepass $STORE_PASSWORD -noprompt

    -------------JKStoPEM--------------
    /opt/jdk1.8.0_151/bin/keytool -exportcert -alias hostname1.com -keystore truststore.jks -storepass 7ecETGlHjzs -file hostname1.crt
    /opt/jdk1.8.0_151/bin/keytool -exportcert -alias hostname2.com -keystore truststore.jks -storepass 7ecETGlHjzs -file hostname2.crt
    /opt/jdk1.8.0_151/bin/keytool -exportcert -alias hostname3.com -keystore truststore.jks -storepass 7ecETGlHjzs -file hostname3.crt
    openssl x509 -inform der -in hostname1.crt -out hostname1.pem
    openssl x509 -inform der -in hostname2.crt -out hostname2.pem
    openssl x509 -inform der -in hostname3.crt -out hostname3.pem
    cat *.pem > truststore_combined.pem
    
    To execute - use  cert.sh hostname
    ```

## **Zookeeper Installation**

!!!-  "Download tar file from apache zookeeper"
    ```
    wget https://downloads.apache.org/zookeeper/zookeeper-3.8.1/apache-zookeeper-3.8.1-bin.tar.gz
    tar -xzf apache-zookeeper-3.8.1-bin.tar.gz
    cd apache-zookeeper-3.8.1-bin/conf/
    ```

!!!-  "Configure zookeeper properties"

    ```
    tickTime=1000
    initLimit=10
    syncLimit=5
    dataDir=/home/testing/apache-zookeeper-3.8.1-bin/zkdata
    maxClientCnxns=120
    maxCnxns=120
    ssl.client.enable=true
    #portUnification=true
    #client.portUnification=true
    #multiAddress.reachabilityCheckEnabled=true
    #quorumListenOnAllIPs=true
    #4lw.commands.whitelist=*
    admin.enableServer=false
    authProvider.sasl=org.apache.zookeeper.server.auth.SASLAuthenticationProvider
    zookeeper.superUser=superadmin
    secureClientPort=12182
    clientCnxnSocket=org.apache.zookeeper.ClientCnxnSocketNetty
    serverCnxnFactory=org.apache.zookeeper.server.NettyServerCnxnFactory 
    authProvider.x509=org.apache.zookeeper.server.auth.X509AuthenticationProvider
    ssl.keyStore.location=/home/testing/certs/localhost1.jks
    ssl.keyStore.password=7ecETGlHjzs
    ssl.trustStore.location=/home/testing/certs/truststore.jks
    ssl.trustStore.password=7ecETGlHjzs
    sslQuorum=true
    ssl.quorum.keyStore.location=/home/testing/certs/localhost1.jks
    ssl.quorum.keyStore.password=7ecETGlHjzs
    ssl.quorum.trustStore.location=/home/testing/certs/truststore.jks
    ssl.quorum.trustStore.password=7ecETGlHjzs
    sessionRequireClientSASLAuth=true
    #jute.maxbuffer=50000000
    DigestAuthenticationProvider.digestAlg=SHA3-512
    secureClientPortAddress=localhost1
    server.1=localhost1:4888:5888
    server.2=localhost2:4888:5888
    server.3=localhost3:4888:5888
    ```

!!!-  "create jaas conf file for authentication"
    ```
    Server{
    org.apache.zookeeper.server.auth.DigestLoginModule required
    user_superadmin="SuperSecret123"
    user_bob="bobsecret"
    user_kafka="kafkasecret";
    };
    Client{
    org.apache.zookeeper.server.auth.DigestLoginModule required
    username="bob"
    password="bobsecret";
    };
    ```

!!!-  "Configure the Java Env variables"
    ```
    export ZOO_LOG_DIR=/home/testing/apache-zookeeper-3.8.1-bin/zklogs

    export ZK_SERVER_HEAP=1024

    export SERVER_JVM_FLAGS="$SERVER_JVMFLAGS -Dzookeeper.db.autocreate=false -Djava.security.auth.login.config=/home/testing/apache-zookeeper-3.8.1-bin/conf/jaas.conf"

    #export ZOO_DATADIR_AUTOCREATE_DISABLE=1

    export CLIENT_JVMFLAGS="$CLIENT_JVMFLAGS -Dzookeeper.clientCnxnSocket=org.apache.zookeeper.ClientCnxnSocketNetty -Dzookeeper.ssl.trustStore.location=/home/testing/certs/truststore.jks -Dzookeeper.ssl.trustStore.password=7ecETGlHjzs -Dzookeeper.ssl.keyStore.location=/home/testing/certs/localhost1.jks -Dzookeeper.ssl.keyStore.password=7ecETGlHjzs -Dzookeeper.client.secure=true -Djava.security.auth.login.config=/home/testing/apache-zookeeper-3.8.1-bin/conf/jaas.conf"

    export JVMFLAGS="-Djava.security.auth.login.config=/home/testing/apache-zookeeper-3.8.1-bin/conf/jaas.conf"
    ```

!!!-  "Create Id for each zk node"
    ```
    echo 1 > /data/kafka/zookeeper/data/myid
    # Change the value for each node (e.g., 1, 2, 3)
    ```

!!!-  "Start zookeper server one each node"
    ```
    bin/zkServer.sh start
    ```
    
!!!-  "Create ZK TLS properties file"
    ```
    zookeeper.ssl.client.enable=true
    zookeeper.clientCnxnSocket=org.apache.zookeeper.ClientCnxnSocketNetty
    zookeeper.ssl.keystore.location=/root/certs/localhost.jks
    zookeeper.ssl.keystore.password=7ecETGlHjzs
    zookeeper.ssl.truststore.location=/root/certs/truststore.jks
    zookeeper.ssl.truststore.password=7ecETGlHjzs
    ```

!!!-  "Login to cli and verify the status "
    ```
    bin/zkCli.sh -server hostname1:12182
    ```

## **Kafka Installation**

!!!-  "Download tar file from apache kafka"
    ```
    wget https://downloads.apache.org/kafka/3.6.1/kafka_2.13-3.6.1.tgz
    tar -xzf kafka_2.13-3.6.1.tgz
    cd kafka_2.13-3.6.1
    ```

!!!-  "Configure server.properties"
    ```
    broker.id=1
    listeners=SASL_SSL://hostname:6667
    listener.security.protocol.map=SASL_SSL:SASL_SSL
    advertised.listeners=SASL_SSL://hostname:6667
    authorizer.class.name=kafka.security.authorizer.AclAuthorizer
    sasl.enabled.mechanisms=SCRAM-SHA-512
    sasl.mechanism.inter.broker.protocol=SCRAM-SHA-512
    security.inter.broker.protocol=SASL_SSL
    ssl.client.auth=required
    #ssl.endpoint.identification.algorithm=
    ssl.keystore.location=/root/certs/hostname.jks
    ssl.keystore.password=7ecETGlHjzs
    ssl.truststore.location=/root/certs/truststore.jks
    ssl.truststore.password=7ecETGlHjzs
    super.users=User:admin
    zookeeper.connect=hostname:12182,hostname2:12182,hostnamedb:12182
    zookeeper.ssl.client.enable=true
    # Timeout in ms for connecting to zookeeper
    zookeeper.connection.timeout.ms=18000 
    zookeeper.clientCnxnSocket=org.apache.zookeeper.ClientCnxnSocketNetty
    zookeeper.ssl.keystore.location=/root/certs/hostname.jks
    zookeeper.ssl.keystore.password=7ecETGlHjzs
    zookeeper.ssl.truststore.location=/root/certs/truststore.jks
    zookeeper.ssl.truststore.password=7ecETGlHjzs
    ```

!!!-  "Create kafka_jaas.conf file for authentication"
    ```
    Client{
    org.apache.zookeeper.server.auth.DigestLoginModule required
    username="bob"
    password="bobsecret";
    };
    KafkaServer{
    org.apache.kafka.common.security.scram.ScramLoginModule required
    username="admin"
    password="password";
    };
    KafkaClient{
    org.apache.kafka.common.security.scram.ScramLoginModule required
    username="admin"
    password="password";
    };
    ```

!!!-  "Configure KAFKA_OPTS and KAFKA-ENV properties"
    ```
    export KAFKA_HOME=/root/kafka_2.13-3.4.0

    export KAFKA_OPTS="-Djava.security.auth.login.config=/root/kafka_2.13-3.4.0/config/kafka_jaas.conf -Dzookeeper.clientCnxnSocket=org.apache.zookeeper.ClientCnxnSocketNetty  -Dzookeeper.client.secure=true  -Dzookeeper.ssl.truststore.location=/root/certs/truststore.jks -Dzookeeper.ssl.truststore.password=7ecETGlHjzs"

    export KAFKA_HEAP_OPTS="-Xmx8G -Xms8G"

    #export JMX_PORT=9999

    #export JMX_PROMETHEUS_PORT=9991

    #export KAFKA_JMX_OPTS="-Dcom.sun.management.jmxremote=true -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -javaagent:/root/certs/jmx_prometheus_javaagent-0.20.0.jar=$JMX_PROMETHEUS_PORT:/root/certs/kafka_broker.yml"
    ```

!!!-  "Create Admin user for Kafka Server"
    ```
    bin/kafka-configs.sh --zk-tls-config-file /home/testing/certs/zk_tls_config.properties --zookeeper zkhost:12182 --alter --add-config 'SCRAM-SHA-512=[password='password']' --entity-type users --entity-name admin
    ```

!!!-  "Start the Kafka Server"
    ```
    bin/kafka-server-start.sh -daemon config/server.properties
    ```

!!!-  "Kafka ACl commands for authorization"

    ```
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
