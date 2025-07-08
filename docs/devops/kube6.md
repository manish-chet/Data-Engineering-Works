### Persistent Volume and Persistent Volume Claim

The video introduces the concept of Persistent Volumes (PV) and Persistent Volume Claims (PVC) in Kubernetes as a solution for managing storage persistently, especially in a distributed environment.

Understanding the Need for Persistent Storage:
Traditionally, in IT setups, organizations use centralized storage systems where multiple workstations can access and save data. This ensures that data is consistently available regardless of which machine is being used. In Kubernetes, a similar need arises because pods, which contain your applications, are ephemeral.

Limitations of Previous Storage Concepts:
*   EmptyDir: The video revisits the `EmptyDir` concept, explaining that it creates a temporary storage volume that is shared between containers within the *same* pod. However, if the pod itself is deleted, the `EmptyDir` and all its data are also deleted. When a new pod is created, new storage is also created, meaning data from the previous pod is lost.
*   HostPath: Another concept discussed is `HostPath`, where a pod uses a directory directly on the worker node's local file system for storage. The significant problem with `HostPath` is that if a pod is deleted and then recreated on a *different* worker node within the cluster (which is a common occurrence in Kubernetes for load balancing and fault tolerance), the data stored on the original worker node's local machine will not be accessible to the new pod. This means data persistence is not guaranteed across different worker nodes.

Introducing Persistent Volume (PV):
To address the issues of ephemeral storage and data loss across pod recreations or migrations between worker nodes, Kubernetes provides Persistent Volumes (PV). A Persistent Volume is essentially an abstraction of a physical piece of storage that exists independently of a pod or even a specific worker node. It's a common, shared storage that remains available even if pods are deleted or moved. The video illustrates this with an example of an Elastic Block Store (EBS) volume from AWS, which can be connected to multiple worker nodes. If a pod is deleted from one worker node and recreated on another, it can still access the same shared EBS volume, ensuring data consistency. EBS is a block-level storage where data is stored in blocks, and it supports mounting to a single EC2 instance (worker node) at a time.

The analogy used in the video explains that an administrator might acquire a large cloud storage (e.g., 100GB from AWS EBS). From this large pool, smaller, independent "Persistent Volume objects" are created (e.g., 30GB, 20GB, 50GB). These PVs are then made available for consumption by applications.

Persistent Volume Claim (PVC):
Pods do not directly access Persistent Volumes. Instead, they make a Persistent Volume Claim (PVC). A PVC is a request for a specific amount of storage with certain access modes. For example, a pod might request 1GB of storage. When a PVC is made, Kubernetes looks for an available Persistent Volume that matches the requested specifications (size, access mode) and then "binds" that PV to the PVC. Once bound, the pod can use the storage via its PVC. The video also explains that once the storage is used by a pod and its work is done, the data in the Persistent Volume can be "reclaimed" or "recycled" for future use by other pods if the original pod is deleted.

Example YAML for a Persistent Volume (PV):
The video demonstrates creating a PV named `my-pv-for-ebs` from an AWS EBS volume. This YAML specifies the capacity, access modes, reclaim policy, and the ID of the actual EBS volume.
```yaml
# my-persistent-volume.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv-for-ebs # Name of the Persistent Volume
spec:
  capacity:
    storage: 1Gi # Defines the capacity of this PV (1 Gigabyte)
  accessModes:
    - ReadWriteOnce # Indicates that this volume can be mounted as read-write by a single node
  persistentVolumeReclaimPolicy: Recycle # Specifies that the volume can be recycled after its claim is released
  awsElasticBlockStore:
    volumeID: <YOUR_EBS_VOLUME_ID> # The actual ID of your AWS EBS volume
    fsType: ext4 # The file system type on the EBS volume
```
This YAML defines a Persistent Volume named `my-pv-for-ebs` which is a 1GB slice of an existing AWS EBS volume. It's set to be `ReadWriteOnce`, meaning it can be mounted by only one node at a time in read-write mode, and its reclaim policy is `Recycle`, allowing the data to be reused.

Example YAML for a Persistent Volume Claim (PVC):
Next, a PVC is created to request storage from an available PV.
```yaml
# my-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-ebs-vol-claim # Name of the Persistent Volume Claim
spec:
  accessModes:
    - ReadWriteOnce # Must match the access mode of the PV it intends to bind to
  resources:
    requests:
      storage: 1Gi # Requests 1 Gigabyte of storage
```
This `my-ebs-vol-claim` PVC requests 1GB of storage with `ReadWriteOnce` access. Kubernetes will then match this claim to a suitable PV, such as `my-pv-for-ebs`, and bind them.

Example YAML for a Deployment using PVC:
Finally, a Deployment that utilizes this PVC is created, showing how a pod accesses the persistent storage.
```yaml
# my-nginx-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-nginx-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx-container
          image: nginx
          ports:
            - containerPort: 80
          volumeMounts:
            - name: my-ebs-volume # Name of the volume to mount
              mountPath: /usr/share/nginx/html # Path inside the container where the volume will be mounted
      volumes:
        - name: my-ebs-volume # Definition of the volume
          persistentVolumeClaim:
            claimName: my-ebs-vol-claim # Reference to the PVC that provides the storage
```
In this Deployment, an Nginx container is defined, and a `volumeMount` is created to attach the `my-ebs-volume` to `/usr/share/nginx/html` inside the container. The `my-ebs-volume` itself is defined to use the `my-ebs-vol-claim` PVC. This setup ensures that any data written to `/usr/share/nginx/html` within the Nginx container is stored on the persistent EBS volume, maintaining data integrity even if the Nginx pod is deleted and recreated on a different worker node.

### LivenessProbe

The video then transitions to the concept of LivenessProbe, explaining its crucial role in ensuring the continuous availability and health of applications running within Kubernetes.

The Shortcoming of Basic Kubernetes Monitoring:
Kubernetes inherently monitors if a pod is running and if the containers within that pod are running. It performs basic checks, such as sending a ping or running a simple test command, and if a response is received, it assumes the pod and container are healthy. However, this basic check does not guarantee that the application *inside* the container is actually functioning correctly. For instance, a web server might be running, but the specific application it hosts could be frozen, stuck in a loop, or unable to serve requests. In such a scenario, Kubernetes would still consider the container "running," even though the application is effectively dead.

Purpose of LivenessProbe:
LivenessProbe addresses this limitation by actively checking the health of the application itself, inside the container. It ensures that the application is not just running, but is also responsive and performing its intended function.

How LivenessProbe Works:
A LivenessProbe is configured to execute a specific command, make an HTTP GET request, or check a TCP socket at predefined intervals.
*   Success: If the probe's check (e.g., a command) executes successfully and returns an exit code of 0, the application is considered healthy.
*   Failure: If the check returns a non-zero exit code, times out, or fails to connect, it indicates that the application is unhealthy or stuck.
*   Action on Failure: If the LivenessProbe fails a specified number of times consecutively (defined by `failureThreshold`), Kubernetes will terminate the unhealthy container. Once terminated, Kubernetes will then create a new container to replace it, aiming to bring the application back to a healthy state. This mechanism helps maintain the reliability and availability of your services, especially when combined with load balancers, as it ensures that only healthy application instances are serving traffic.

Example YAML for LivenessProbe:
The video provides a YAML example for a Deployment that includes a LivenessProbe.
```yaml
# my-liveness-probe-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-liveness-probe-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-container
          image: busybox
          command: ["/bin/sh", "-c", "echo 'Hello from LivenessProbe' > /tmp/healthy; sleep 300"] # Command to run on container startup
          livenessProbe:
            exec:
              command: ["cat", "/tmp/healthy"] # The command to execute for the probe
            initialDelaySeconds: 5 # Initial delay before the first probe is performed (in seconds)
            periodSeconds: 5 # How often the probe is performed (in seconds)
            timeoutSeconds: 1 # Timeout for the probe command (in seconds)
            failureThreshold: 3 # Number of consecutive failures before Kubernetes restarts the container
```
Explanation of LivenessProbe Parameters:
*   The container uses `busybox` and is configured to create a file `/tmp/healthy` immediately upon startup, then sleeps for 300 seconds. This setup simulates an application that is initially healthy.
*   The `livenessProbe` is defined using an `exec` action, meaning it will run a command to check the application's health. The command chosen is `cat /tmp/healthy`, which attempts to read the content of the `healthy` file. If the file exists and is readable, `cat` will return a 0 exit code (success); otherwise, it will return a non-zero exit code (failure).
*   `initialDelaySeconds: 5`: This parameter tells Kubernetes to wait for 5 seconds after the container starts before executing the first LivenessProbe check. This is important to give the application sufficient time to initialize and become ready to serve requests before being probed.
*   `periodSeconds: 5`: After the initial delay, the probe will run the `cat /tmp/healthy` command every 5 seconds.
*   `timeoutSeconds: 1`: If the `cat /tmp/healthy` command does not complete and return an output within 1 second, the probe will consider it a failure.
*   `failureThreshold: 3`: This specifies that if the probe fails 3 consecutive times, Kubernetes will consider the container unhealthy, terminate it, and then recreate a new one. This prevents transient issues from immediately causing a container restart.

