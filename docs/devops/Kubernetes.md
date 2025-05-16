# Kubernetes Overview

Kubernetes is an open source container management tool which automates container deployment, container scaling and load balancing.  
It schedules, runs and manages isolated containers which are running on VM/Physical/Cloud machines.  
All top providers support Kubernetes.

---

## History

Google developed an internal system called **'borg'** to deploy and manage thousands of Google applications on their cluster.  
In 2014, Google introduced **Kubernetes**, an open source platform written in **'golang'**, and later donated it to **CNCF**.

---

## Online Platform for K8s to Learn

- Kubernetes Playground  
- Play with K8s  
- Play with Kubernetes Classroom

---

## Cloud Based K8s Services

1. GKE - Google Kubernetes Services  
2. ALS - Azure Kubernetes Services  
3. EKS - Elastic Kubernetes Services

---

## Problems with Scaling up the Containers

1. Containers cannot communicate with each other  
2. Auto scaling and load balancing was not possible  
3. Container had to be managed carefully

---

## Features of K8s

1. Orchestration (Clustering of any number of containers running on different networks)  
2. Autoscaling  
3. Auto healing  
4. Load balancing  
5. Platform independent (Cloud/VM/Physical)  
6. Fault tolerance (Node/Pod failure)  
7. Rollback (Going back to previous version)  
8. Health monitoring of containers  
9. Batch execution (One time, sequential and parallel)

---

## K8s vs Docker Swarm

| Features                            | Kubernetes                                                                      | Docker Swarm                                                     |
|-------------------------------------|----------------------------------------------------------------------------------|------------------------------------------------------------------|
| Installation and cluster configuration | Complicated and time consuming                                                  | Fast and Easy                                                    |
| Supports                            | K8s can work with almost all container types                                    | Fast and Easy                                                    |
| GUI                                 | GUI available                                                                    | GUI not available                                                |
| Data Volume                         | Only shared with containers in same pod                                         | Can be shared with any other container                          |
| Updates and rollback                | Process scheduling to maintain services while updating                          | Progressive updates and service with health monitoring throughout the update |
| Autoscaling                         | Support vertical and horizontal scaling                                         | No support for autoscaling                                      |
| Logging and monitoring              | Inbuilt tool for monitoring                                                     | 3rd Party tools like Splunk, Portainer                          |

