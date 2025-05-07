# YAML - A Beginner Friendly Guide

## What is YAML?

* **YAML** stands for "YAML Ain't Markup Language".
* It is a **data serialization language**, designed to be **human-readable**.
* Commonly used for **configuration files** in **DevOps tools** like Ansible, Docker Compose, and Kubernetes.
* YAML is **not a programming language**.
* It has better readability than JSON and XML.
* Most programming languages support YAML through libraries.
* File extensions: `.yaml` or `.yml`

---

## Data Serialization

* **Serialization**: Converting data into a format for storage/transmission.
* **Deserialization**: Reconstructing original data from serialized format.
* **YAML** serves as a popular format for this.

**Example**:

```python
# Python serializes data
import yaml

user = {'name': 'Martin', 'age': 30}
with open('user.yaml', 'w') as file:
    yaml.dump(user, file)
```

---

## YAML Structure

### Basic Key-Value Pair

```yaml
name: Martin
```

### Nesting with Indentation

```yaml
work_experience:
  company_one:
    role: Developer
    duration: 2 years
  company_two:
    role: Engineer
    duration: 3 years
```

* **Use spaces** for indentation (no tabs).
* YAML documents can optionally begin with `---`.

---

## YAML vs JSON vs XML

### YAML

```yaml
user:
  name: Alice
  age: 25
```

### JSON

```json
{
  "user": {
    "name": "Alice",
    "age": 25
  }
}
```

### XML

```xml
<user>
  <name>Alice</name>
  <age>25</age>
</user>
```

* YAML uses indentation, JSON uses braces, XML uses tags.

---

## YAML Data Types

### 1. Numbers

```yaml
int_decimal: 10
float_value: 99.88
hex_value: 0x1F
exp_value: 1.414e+3
infinite: .inf
not_a_number: .nan
```

### 2. Booleans

```yaml
bool_true: yes
bool_false: no
```

Python interprets them as `True` and `False`.

### 3. Strings

```yaml
plain: Hello
quoted: "Hello, World!"
single_quoted: 'Hello'
newline_string: "Line1\nLine2"
```

#### Multi-line

```yaml
folded: >-
  This is a folded
  multi-line string.

block: |-
  This is a block
  multi-line string.
```

### 4. Lists (Arrays)

```yaml
colors:
  - red
  - green
  - blue

people:
  - name: John
    age: 30
  - name: Jane
    age: 25

inline_list: [red, green, blue]
```

### 5. Dictionaries (Maps)

```yaml
user:
  name: Mike
  age: 28

inline_dict: {name: Mike, age: 28}
```

### 6. Null

```yaml
middle_name: ~
nickname: null
```

### 7. Sets

```yaml
!!set
? CKAD
? CKA
? CKAD  # Duplicate, will be removed by parser
```

Python will parse as `{ 'CKAD', 'CKA' }`

---

## Comments in YAML

```yaml
# This is a comment
name: John  # Inline comment
```

---

## Advanced Concepts

### Anchors & References

```yaml
defaults: &defaults
  restart_policy: always

service1:
  restart_policy: *defaults

service2:
  restart_policy: *defaults
```

### Extensions (Merges)

```yaml
default_env: &default_env
  APP_NAME: web_service
  ENV: production

service2:
  environment:
    <<: *default_env
    TYPE: database
```

---

## Placeholders and Templating

Used in tools like Helm for Kubernetes:

```yaml
replicas: {{ .Values.replicas }}
image: {{ .Values.image.repository }}
```

**values.yaml**:

```yaml
replicas: 3
image:
  repository: nginx
```

---

## Multiple Documents in One File

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
---
apiVersion: v1
kind: Service
metadata:
  name: my-service
```

---
##  Docker Compose YAML Example

A Docker Compose file helps define and run multi-container Docker applications.

```yaml
version: '3.8'
services:
  web:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html

  app:
    build: .
    environment:
      - APP_ENV=production
    depends_on:
      - db

  db:
    image: postgres:13
    restart: always
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

### Explanation

* **version**: Specifies the version of Docker Compose file format
* **services**: Defines three services: `web`, `app`, and `db`
* **volumes**: Persists PostgreSQL data

---

##  Kubernetes Deployment Example

A YAML configuration for deploying a web application on Kubernetes.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.14.2
          ports:
            - containerPort: 80
```

###  Explanation

* **apiVersion**: The Kubernetes API version
* **kind**: The type of object (Deployment)
* **metadata**: Metadata including the name
* **spec**: Specifications including number of replicas, pod template, and container details

---

## Using PyYAML in Python

### Reading YAML

```python
import yaml

with open('test.yaml') as f:
    data = yaml.safe_load(f)
print(data)
```

### Writing YAML

```python
import yaml

users = [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}]

with open('users.yaml', 'w') as f:
    yaml.dump(users, f)
```

---

## Summary

* YAML is human-readable and widely used in DevOps.
* It supports multiple data types, nesting, and advanced features like anchors.
* Tools like Kubernetes and Docker Compose heavily depend on YAML.
* Python's PyYAML library makes it easy to work with YAML files.

---

