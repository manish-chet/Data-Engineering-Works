## **Install postgres packages**

## Prerequisites

- 3 VMs (Ensure pre-requisites like SELinux disabled, firewall off, THP disabled, etc.)
- Java 11 or higher
- Enough RAM for data
- Network connectivity


!!!- "Install Postgres and Dependencies"
    ```
    dnf module install postgresql:15/server
    dnf install postgresql-devel
    dnf install -y python3-devel postgresql-devel gcc
    dnf install -y haproxy
    ```

!!!- "Verify Postgres Installation"
    ```
    which postgres
    postgres -V
    systemctl status postgresql
    ```

!!!- "Install Python3 and Required Packages"
    ```
    yum install python3-pip -y
    pip3 install --upgrade pip
    pip install patroni python-etcd psycopg2
    ```

## Patroni Configuration

!!!- "Create Patroni Configuration File (/etc/patroni.yml)"
    ```
      scope: postgres
      namespace: /db/
      name: hostname3
      restapi:
        listen: ServerIP3:8008
        connect_address: ServerIP3:8008
      etcd:
        host: 1ServerIP2:2379
      bootstrap:
        dcs:
      ttl: 30
      loop_wait: 10
      retry_timeout: 10
      maximum_lag_on_failover: 1048576
      postgresql:
      use_pg_rewind: true
        initdb:
      - encoding: UTF8
      - data-checksums
        pg_hba:
      - host replication replicator   127.0.0.1/32 md5
      - host replication replicator   ServerIP1/0   md5
      - host replication replicator   ServerIP2/0   md5
      - host replication replicator   ServerIP3/0   md5
      - host all all   0.0.0.0/0   md5
        users:
      admin:
        password: admin
        options:
        - createrole
        - createdb
      postgresql:
        listen: ServerIP3:5432
        connect_address: ServerIP3:5432
        data_dir: /data1/patroni/
        pgpass: /tmp/pgpass
        authentication:
      replication:
        username:   replicator
        password:   password
      superuser:
        username:   postgres
        password:   password
        parameters:
        unix_socket_directories:  '.'
      tags:
        nofailover:   false
        noloadbalance:   false
        clonefrom:   false
        nosync:   false
    ```

!!!- "Prepare Data Directory for Patroni"
    ```
    mkdir -p /data1/patroni/
    sudo chown postgres:postgres /data1/patroni/
    sudo chmod 700 /data1/patroni/
    ```

!!!- "Create Patroni systemd Service"
    ```
    [Unit]
    Description=Runners to orchestrate a high-availability PostgresSQL
    After=syslog.target network.target
    [Service]
    Type=simple
    User=postgres
    Group=postgres
    ExecStart=/usr/local/bin/patroni /etc/patroni.yml
    KillMode=process
    TimeoutSec=30
    Restart=no
    [Install]
    WantedBy=multi-user.target
    ```

    ```
    systemctl daemon-reload
    # Enable and start the service as needed
    # systemctl enable patroni
    # systemctl start patroni
    ```

## Etcd Setup

!!!- "Download, Setup, and Move etcd Binaries"
    ```
    # Download and extract etcd, then:
    mv etcd etcdctl etcdutl /usr/local/bin/
    vim /etc/default/etcd
    ```

!!!- "Start etcd with Custom Configuration"
    ```
    nohup /usr/local/bin/etcd --name etcd0 \
      --listen-peer-urls="http://ServerIP2:2380,http://ServerIP2:7001" \
      --listen-client-urls="http://ServerIP2:2379,http://ServerIP2:3379" \
      --initial-advertise-peer-urls="http://ServerIP2:2380" \
      --initial-cluster="etcd0=http://ServerIP2:2380" \
      --advertise-client-urls="http://ServerIP2:2379" \
      --initial-cluster-token="hostname2" \
      --initial-cluster-state="new" \
      --enable-v2=true > etcd.log 2>&1 &
    ```

!!!- "Create etcd systemd Service"
      ```
      [Unit]
      Description=etcd key-value store
      After=syslog.target network.target
      [Service]
      Type=simple
      User=etcd
      Group=etcd
      ExecStart=/usr/local/bin/etcd /etc/default/etcd
      KillMode=process
      TimeoutSec=30
      Restart=no
      [Install]
      WantedBy=multi-user.target
      ```

## Patroni Cluster Management

!!!- "Check Patroni Cluster Status"
    ```
    patronictl -c /etc/patroni.yml list
    # Example output:
    # + Cluster: postgres (7467834322212369848) +---------+----+-----------+
    # | Member  | Host | Role   | State   | TL | Lag in MB |
    # +-----------------+--------------+--------+---------+----+-----------+
    # | hostname1 | ServerIP1 | Leader | running |  1 |   |
    # +-----------------+--------------+--------+---------+----+-----------+
    ```
