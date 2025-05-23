## Install postgres packages
???- "Install Postgres and Dependencies"
    ```bash
    dnf module install postgresql:15/server
    dnf install postgresql-devel
    dnf install -y python3-devel postgresql-devel gcc
    dnf install -y haproxy
    ```

???- "Verify Postgres Installation"
    ```bash
    which postgres
    postgres -V
    systemctl status postgresql
    ```

???- "Install Python3 and Required Packages"
    ```bash
    yum install python3-pip -y
    pip3 install --upgrade pip
    pip install patroni python-etcd psycopg2
    ```

## Patroni Configuration

???- "Create Patroni Configuration File (/etc/patroni.yml)"
    ```yaml
    scope: postgres
    namespace: /db/
    name: hostname3
    restapi:
      listen: IP.IP.IP.208:8008
      connect_address: IP.IP.IP.208:8008
    etcd:
      host: 1IP.IP.IP.207:2379
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
        - host replication replicator   IP.IP.IP.206/0   md5
        - host replication replicator   IP.IP.IP.207/0   md5
        - host replication replicator   IP.IP.IP.208/0   md5
        - host all all   0.0.0.0/0   md5
      users:
        admin:
           password: admin
           options:
           - createrole
           - createdb
    postgresql:
       listen: IP.IP.IP.208:5432
       connect_address: IP.IP.IP.208:5432
       data_dir:     /data1/patroni/
       pgpass:     /tmp/pgpass
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

???- "Prepare Data Directory for Patroni"
    ```bash
    mkdir -p /data1/patroni/
    sudo chown postgres:postgres /data1/patroni/
    sudo chmod 700 /data1/patroni/
    ```

???- "Create Patroni systemd Service"
    ```ini
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
    ```bash
    systemctl daemon-reload
    # Enable and start the service as needed
    # systemctl enable patroni
    # systemctl start patroni
    ```

## Etcd Setup

???- "Download, Setup, and Move etcd Binaries"
    ```bash
    # Download and extract etcd, then:
    mv etcd etcdctl etcdutl /usr/local/bin/
    vim /etc/default/etcd
    ```

???- "Start etcd with Custom Configuration"
    ```bash
    nohup /usr/local/bin/etcd --name etcd0 \
      --listen-peer-urls="http://IP.IP.IP.207:2380,http://IP.IP.IP.207:7001" \
      --listen-client-urls="http://IP.IP.IP.207:2379,http://IP.IP.IP.207:3379" \
      --initial-advertise-peer-urls="http://IP.IP.IP.207:2380" \
      --initial-cluster="etcd0=http://IP.IP.IP.207:2380" \
      --advertise-client-urls="http://IP.IP.IP.207:2379" \
      --initial-cluster-token="hostname2" \
      --initial-cluster-state="new" \
      --enable-v2=true > etcd.log 2>&1 &
    ```

???- "Create etcd systemd Service"
    ```ini
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

???- "Check Patroni Cluster Status"
    ```bash
    patronictl -c /etc/patroni.yml list
    # Example output:
    # + Cluster: postgres (7467834322212369848) +---------+----+-----------+
    # | Member          | Host         | Role   | State   | TL | Lag in MB |
    # +-----------------+--------------+--------+---------+----+-----------+
    # | hostname1 | IP.IP.IP.206 | Leader | running |  1 |           |
    # +-----------------+--------------+--------+---------+----+-----------+
    ```
