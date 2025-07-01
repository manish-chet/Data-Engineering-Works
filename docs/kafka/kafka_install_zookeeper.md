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
    #!/bin/bash
    # Generates several self-signed keys <name>.cer, <name>.jks, and <name>.p12.
    # Truststore is set with name truststore.jks and set password of password12345
    # Usage: createKey.sh <user> <password>
    #        createKey.sh somebody password123
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
    # The number of milliseconds of each tick
    tickTime=1000
    # The number of ticks that the initial 
    # synchronization phase can take
    initLimit=10
    # The number of ticks that can pass between 
    # sending a request and getting an acknowledgement
    syncLimit=5
    # the directory where the snapshot is stored.
    # do not use /tmp for storage, /tmp here is just 
    # example sakes.
    dataDir=/home/testing/apache-zookeeper-3.8.1-bin/zkdata
    # the port at which the clients will connect
    #clientPort=2181
    # the maximum number of client connections.
    # increase this if you need to handle more clients
    maxClientCnxns=120
    maxCnxns=120
    ssl.client.enable=true
    #portUnification=true
    #client.portUnification=true
    #multiAddress.reachabilityCheckEnabled=true
    #quorumListenOnAllIPs=true
    #4lw.commands.whitelist=*

    # Be sure to read the maintenance section of the 
    # administrator guide before turning on autopurge.
    #
    # https://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_maintenance
    #
    # The number of snapshots to retain in dataDir
    autopurge.snapRetainCount=30
    # Purge task interval in hours
    # Set to "0" to disable auto purge feature
    autopurge.purgeInterval=24

    ## Metrics Providers
    #
    # https://prometheus.io Metrics Exporter
    #metricsProvider.className=org.apache.zookeeper.metrics.prometheus.PrometheusMetricsProvider
    #metricsProvider.httpHost=0.0.0.0
    #metricsProvider.httpPort=7000
    #metricsProvider.exportJvmInfo=true

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

???-  "create jaas conf file for authentication"
    ```bash
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

???-  "Configure the Java Env variables"
    ```bash
    export ZOO_LOG_DIR=/home/testing/apache-zookeeper-3.8.1-bin/zklogs

    export ZK_SERVER_HEAP=1024

    export SERVER_JVM_FLAGS="$SERVER_JVMFLAGS -Dzookeeper.db.autocreate=false -Djava.security.auth.login.config=/home/testing/apache-zookeeper-3.8.1-bin/conf/jaas.conf"

    #export ZOO_DATADIR_AUTOCREATE_DISABLE=1

    export CLIENT_JVMFLAGS="$CLIENT_JVMFLAGS -Dzookeeper.clientCnxnSocket=org.apache.zookeeper.ClientCnxnSocketNetty -Dzookeeper.ssl.trustStore.location=/home/testing/certs/truststore.jks -Dzookeeper.ssl.trustStore.password=7ecETGlHjzs -Dzookeeper.ssl.keyStore.location=/home/testing/certs/localhost1.jks -Dzookeeper.ssl.keyStore.password=7ecETGlHjzs -Dzookeeper.client.secure=true -Djava.security.auth.login.config=/home/testing/apache-zookeeper-3.8.1-bin/conf/jaas.conf"

    export JVMFLAGS="-Djava.security.auth.login.config=/home/testing/apache-zookeeper-3.8.1-bin/conf/jaas.conf"
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
???-  "Create ZK TLS properties file"
    ```bash
    zookeeper.ssl.client.enable=true
    zookeeper.clientCnxnSocket=org.apache.zookeeper.ClientCnxnSocketNetty
    zookeeper.ssl.keystore.location=/root/certs/localhost.jks
    zookeeper.ssl.keystore.password=7ecETGlHjzs
    zookeeper.ssl.truststore.location=/root/certs/truststore.jks
    zookeeper.ssl.truststore.password=7ecETGlHjzs
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
    # Licensed to the Apache Software Foundation (ASF) under one or more
    # contributor license agreements.  See the NOTICE file distributed with
    # this work for additional information regarding copyright ownership.
    # The ASF licenses this file to You under the Apache License, Version 2.0
    # (the "License"); you may not use this file except in compliance with
    # the License.  You may obtain a copy of the License at
    #
    #    http://www.apache.org/licenses/LICENSE-2.0
    #
    # Unless required by applicable law or agreed to in writing, software
    # distributed under the License is distributed on an "AS IS" BASIS,
    # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    # See the License for the specific language governing permissions and
    # limitations under the License.

    # see kafka.server.KafkaConfig for additional details and defaults

    ############################# Server Basics #############################

    # The id of the broker. This must be set to a unique integer for each broker.
    broker.id=1

    ############################# Socket Server Settings #############################

    # The address the socket server listens on. It will get the value returned from 
    # java.net.InetAddress.getCanonicalHostName() if not configured.
    #   FORMAT:
    #     listeners = listener_name://host_name:port
    #   EXAMPLE:
    #     listeners = PLAINTEXT://your.host.name:9092


    listeners=SASL_SSL://hostname:6667
    listener.security.protocol.map=SASL_SSL:SASL_SSL
    advertised.listeners=SASL_SSL://hostname:6667


    #listeners=SASL_SSL://abcdrrakfk05.abc.com:6667,CLIENT://0.0.0.0:9001,CLIENT_GCP://0.0.0.0:9101
    #listener.security.protocol.map=SASL_SSL:SASL_SSL,CLIENT:SASL_SSL,CLIENT_GCP:SASL_SSL
    #advertised.listeners=SASL_SSL://abcdrrakfk05.abc.com:6667,CLIENT://prod-rrabroker.abc.com:9001,CLIENT_GCP://prod-rrabroker1.abc.com:9101

    # Hostname and port the broker will advertise to producers and consumers. If not set, 
    # it uses the value for "listeners" if configured.  Otherwise, it will use the value
    # returned from java.net.InetAddress.getCanonicalHostName().
    #advertised.listeners=PLAINTEXT://your.host.name:9092

    # Maps listener names to security protocols, the default is for them to be the same. See the config documentation for more details
    #listener.security.protocol.map=PLAINTEXT:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL

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

    # The number of threads that the server uses for receiving requests from the network and sending responses to the network
    num.network.threads=3

    # The number of threads that the server uses for processing requests, which may include disk I/O
    num.io.threads=8

    # The send buffer (SO_SNDBUF) used by the socket server
    socket.send.buffer.bytes=102400

    # The receive buffer (SO_RCVBUF) used by the socket server
    socket.receive.buffer.bytes=102400

    # The maximum size of a request that the socket server will accept (protection against OOM)
    socket.request.max.bytes=104857600


    ############################# Log Basics #############################

    # A comma separated list of directories under which to store log files
    log.dirs=/root/kafka_2.13-3.4.0/kafkadata

    # The default number of log partitions per topic. More partitions allow greater
    # parallelism for consumption, but this will also result in more files across
    # the brokers.
    num.partitions=1

    # The number of threads per data directory to be used for log recovery at startup and flushing at shutdown.
    # This value is recommended to be increased for installations with data dirs located in RAID array.
    num.recovery.threads.per.data.dir=1

    ############################# Internal Topic Settings  #############################
    # The replication factor for the group metadata internal topics "__consumer_offsets" and "__transaction_state"
    # For anything other than development testing, a value greater than 1 is recommended for to ensure availability such as 3.
    offsets.topic.replication.factor=1
    transaction.state.log.replication.factor=1
    transaction.state.log.min.isr=1

    ############################# Log Flush Policy #############################

    # Messages are immediately written to the filesystem but by default we only fsync() to sync
    # the OS cache lazily. The following configurations control the flush of data to disk.
    # There are a few important trade-offs here:
    #    1. Durability: Unflushed data may be lost if you are not using replication.
    #    2. Latency: Very large flush intervals may lead to latency spikes when the flush does occur as there will be a lot of data to flush.
    #    3. Throughput: The flush is generally the most expensive operation, and a small flush interval may lead to excessive seeks.
    # The settings below allow one to configure the flush policy to flush data after a period of time or
    # every N messages (or both). This can be done globally and overridden on a per-topic basis.

    # The number of messages to accept before forcing a flush of data to disk
    #log.flush.interval.messages=10000

    # The maximum amount of time a message can sit in a log before we force a flush
    #log.flush.interval.ms=1000

    ############################# Log Retention Policy #############################

    # The following configurations control the disposal of log segments. The policy can
    # be set to delete segments after a period of time, or after a given size has accumulated.
    # A segment will be deleted whenever *either* of these criteria are met. Deletion always happens
    # from the end of the log.

    # The minimum age of a log file to be eligible for deletion due to age
    log.retention.hours=24

    # A size-based retention policy for logs. Segments are pruned from the log unless the remaining
    # segments drop below log.retention.bytes. Functions independently of log.retention.hours.
    #log.retention.bytes=1073741824

    # The maximum size of a log segment file. When this size is reached a new log segment will be created.
    log.segment.bytes=1073741824

    # The interval at which log segments are checked to see if they can be deleted according
    # to the retention policies
    log.retention.check.interval.ms=300000

    ############################# Zookeeper #############################

    # Zookeeper connection string (see zookeeper docs for details).
    # This is a comma separated host:port pairs, each corresponding to a zk
    # server. e.g. "127.0.0.1:3000,127.0.0.1:3001,127.0.0.1:3002".
    # You can also append an optional chroot string to the urls to specify the
    # root directory for all kafka znodes.
    zookeeper.connect=hostname:12182,hostname2:12182,hostnamedb:12182
    zookeeper.ssl.client.enable=true

    # Timeout in ms for connecting to zookeeper
    zookeeper.connection.timeout.ms=18000 
    zookeeper.clientCnxnSocket=org.apache.zookeeper.ClientCnxnSocketNetty
    zookeeper.ssl.keystore.location=/root/certs/hostname.jks
    zookeeper.ssl.keystore.password=7ecETGlHjzs
    zookeeper.ssl.truststore.location=/root/certs/truststore.jks
    zookeeper.ssl.truststore.password=7ecETGlHjzs

    ############################# Group Coordinator Settings #############################

    # The following configuration specifies the time, in milliseconds, that the GroupCoordinator will delay the initial consumer rebalance.
    # The rebalance will be further delayed by the value of group.initial.rebalance.delay.ms as new members join the group, up to a maximum of max.poll.interval.ms.
    # The default value for this is 3 seconds.
    # We override this to 0 here as it makes for a better out-of-the-box experience for development and testing.
    # However, in production environments the default value of 3 seconds is more suitable as this will help to avoid unnecessary, and potentially expensive, rebalances during application startup.
    group.initial.rebalance.delay.ms=0 
    ############################# CRUISE CONTROL PROPERTIES #############################
    #metric.reporters=com.linkedin.kafka.cruisecontrol.metricsreporter.CruiseControlMetricsReporter
    #cruise.control.metrics.bootstrap.servers=abcdrrakfk05.abc.com:6667
    #cruise.control.metrics.topic.auto.create=true
    #cruise.control.metrics.topic.num.partitions=1
    #cruise.control.metrics.topic.replication.factor=1
    #cruise.control.metrics.reporter.ssl.truststore.location = /data/kafka_certs/truststore.jks
    #cruise.control.metrics.reporter.ssl.truststore.password = 7ecETGlHjzs
    #cruise.control.metrics.reporter.ssl.protocol=TLS
    #cruise.control.metrics.reporter.security.protocol=SASL_SSL
    #cruise.control.metrics.reporter.sasl.mechanism=SCRAM-SHA-512
    #cruise.control.metrics.reporter.sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required username="admin" password="n1e6my1z";

    #####ADDITIONAL SETTINGS AS PER OLD KAFKA CONFIGURATION#############
    auto.create.topics.enable=false
    auto.leader.rebalance.enable=true
    compression.type=producer
    controlled.shutdown.enable=true
    controlled.shutdown.max.retries=3
    controlled.shutdown.retry.backoff.ms=5000
    controller.message.queue.size=10
    controller.socket.timeout.ms=30000
    default.replication.factor=1
    delete.topic.enable=true
    leader.imbalance.check.interval.seconds=300
    leader.imbalance.per.broker.percentage=10
    log.cleanup.interval.mins=10
    log.index.interval.bytes=4096
    log.index.size.max.bytes=10485760
    log.retention.bytes=-1
    log.retention.hours=24
    log.roll.hours=168
    log.segment.bytes=1073741824
    message.max.bytes=5000000
    min.insync.replicas=1
    num.replica.fetchers=1
    offset.metadata.max.bytes=4096
    offsets.commit.required.acks=-1
    offsets.commit.timeout.ms=5000
    offsets.load.buffer.size=5242880
    offsets.retention.check.interval.ms=600000
    offsets.retention.minutes=86400000
    offsets.topic.compression.codec=0
    offsets.topic.num.partitions=50
    offsets.topic.replication.factor=3
    offsets.topic.segment.bytes=104857600
    producer.metrics.enable=false
    producer.purgatory.purge.interval.requests=10000
    queued.max.requests=500
    replica.fetch.max.bytes=5048576
    replica.fetch.min.bytes=1
    replica.fetch.wait.max.ms=500
    replica.high.watermark.checkpoint.interval.ms=5000
    replica.lag.max.messages=4000
    replica.lag.time.max.ms=10000
    replica.socket.receive.buffer.bytes=65536
    replica.socket.timeout.ms=30000
    socket.request.max.bytes=104857600
    zookeeper.session.timeout.ms=30000
    zookeeper.sync.time.ms=2000
    ```

???-  "Create kafka_jaas.conf file for authentication"
    ```bash
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

???-  "Configure KAFKA_OPTS and KAFKA-ENV properties"
    ```bash
    export KAFKA_HOME=/root/kafka_2.13-3.4.0

    export KAFKA_OPTS="-Djava.security.auth.login.config=/root/kafka_2.13-3.4.0/config/kafka_jaas.conf -Dzookeeper.clientCnxnSocket=org.apache.zookeeper.ClientCnxnSocketNetty  -Dzookeeper.client.secure=true  -Dzookeeper.ssl.truststore.location=/root/certs/truststore.jks -Dzookeeper.ssl.truststore.password=7ecETGlHjzs"

    export KAFKA_HEAP_OPTS="-Xmx8G -Xms8G"

    #export JMX_PORT=9999

    #export JMX_PROMETHEUS_PORT=9991

    #export KAFKA_JMX_OPTS="-Dcom.sun.management.jmxremote=true -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -javaagent:/root/certs/jmx_prometheus_javaagent-0.20.0.jar=$JMX_PROMETHEUS_PORT:/root/certs/kafka_broker.yml"
    ```

???-  "Create Admin user for Kafka Server"
    ```bash
    bin/kafka-configs.sh --zk-tls-config-file /home/testing/certs/zk_tls_config.properties --zookeeper zkhost:12182 --alter --add-config 'SCRAM-SHA-512=[password='password']' --entity-type users --entity-name admin
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
