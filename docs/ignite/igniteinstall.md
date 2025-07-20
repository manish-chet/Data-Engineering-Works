## **Prerequisites**

- 3 VMs (Ensure pre-requisites like SELinux disabled, firewall off, THP disabled, etc.)
- Java 11 or higher
- Enough RAM for data
- Network connectivity

## **Ignite Installation**

!!!-  "Download tar file from apache ignite"
    ```
    Download ignite 2 bin file from https://ignite.apache.org/download.cgi
    unzip apache-ignite-2.8.1-bin
    ```

!!!-  "Set following properties"
    ```
    export IGNITE_JMX_PORT=9999
    #ignite global index inline size in bytes
    #default is 10
    export IGNITE_MAX_INDEX_PAYLOAD_SIZE=100

    #Set the following in bin/ignite.sh
    JVM_OPTS="$JVM_OPTS -Xms8g -Xmx8g -server -XX:MaxMetaspaceSize=256m -XX:+UseG1GC -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:+ScavengeBeforeFullGC -XX:MaxDirectMemorySize=2048m"
    ```

!!!-  "Setup igniteconfig.xml"
    ```
    Copy the following xml in ignitework directory
    wget https://github.com/manish-chet/BigDataSetupfiles/tree/main/ignite/config
    Change the hosts on specific server
    ```

!!!- "start the node"

    nohup ignite.sh config/igniteconfig.xml > out.log 2>&1  &


!!!- "Check the node using baseline"
    ```
    [ignite@hostname ~]$ control.sh --baseline
    WARNING: An illegal reflective access operation has occurred
    WARNING: Illegal reflective access by org.apache.ignite.internal.util.GridUnsafe$2 (file:/home/ignite/apache-ignite-2.8.1-bin/libs/ignite-core-2.8.1.jar) to field java.nio.Buffer.address
    WARNING: Please consider reporting this to the maintainers of org.apache.ignite.internal.util.GridUnsafe$2
    WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations
    WARNING: All illegal access operations will be denied in a future release
    Control utility [ver. 2.8.1#20200521-sha1:86422096]
    2020 Copyright(C) Apache Software Foundation
    User: ignite
    Time: 2025-05-29T19:11:31.029058
    Command [BASELINE] started
    Arguments: --baseline
    --------------------------------------------------------------------------------
    Cluster state: active
    Current topology version: 3
    Baseline auto adjustment enabled: softTimeout=0
    Baseline auto-adjust are not scheduled
    Current topology version: 3 (Coordinator: ConsistentId=ign01, Order=1)
    Baseline nodes:
    ConsistentId=ign01, State=ONLINE, Order=1
    ConsistentId=ign02, State=ONLINE, Order=3
    ConsistentId=ign03, State=ONLINE, Order=2
    --------------------------------------------------------------------------------
    Number of baseline nodes: 3
    Other nodes not found.
    Command [BASELINE] finished with code: 0
    Control utility has completed execution at: 2025-05-29T19:11:31.295162
    Execution time: 266 ms
    ```