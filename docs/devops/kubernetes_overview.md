# Kubernetes Overview

## What is Kubernetes?

Kubernetes (often abbreviated as K8s) is an open-source container orchestration platform that automates the deployment, scaling, and management of containerized applications. Originally developed by Google, it's now maintained by the Cloud Native Computing Foundation (CNCF).

## Key Concepts

- **Cluster**: A set of machines (nodes) that run containerized applications.
- **Node**: A single machine (physical or virtual) in the cluster.
- **Pod**: The smallest deployable unit, typically containing one or more containers.
- **Deployment**: Defines the desired state for pods and manages updates.
- **Service**: Exposes a set of pods as a network service, allowing stable access.
- **Namespace**: Logical separation within a cluster for organizing resources.

## How Kubernetes Works

1. **User submits a deployment** to Kubernetes (usually via `kubectl` or a YAML file).
2. **Kubernetes Scheduler** places pods on appropriate nodes based on resources.
3. **Kubelet** (running on each node) ensures containers are running in pods.
4. **Controller Manager** continuously monitors and ensures the actual state matches the desired state.
5. **Services and DNS** allow pods to discover and communicate with each other.
6. **Kube Proxy** handles network traffic routing for services.

## Features

- Self-healing (auto-restarts failed containers)
- Horizontal scaling
- Rolling updates and rollbacks
- Secrets and configuration management
- Multi-cloud and hybrid deployments

---

