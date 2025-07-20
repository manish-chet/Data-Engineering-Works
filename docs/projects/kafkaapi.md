# FastAPI Kafka Producer API



A production-ready **FastAPI-based REST API** for publishing JSON messages to **Apache Kafka** topics. Designed for high availability, containerized with Docker, and includes Prometheus metrics support for observability.


![Steps](fastapi.svg)

## **Features**

- **REST to Kafka**: Publish JSON data to Kafka via POST endpoint.
- **Health Check**: `/health` endpoint for service monitoring.
- **Prometheus Metrics**: Available at `/metrics`.
- **Logging**: Rotating file logs stored at `/var/log/fastapi_kafka_api.log`.
- **Containerized**: Docker & Docker Compose support for fast deployment.

!!! Tip "Tip"
    
    For better understanding, you should clone the repo `fastapipythonkafka`
    ```bash
    git clone https://github.com/manish-chet/fastapipythonkafka
    ```

!!! Note "Note"

    If you're looking for the full FastAPI + Kafka implementation, see main.py


## **Docker Usage**

Build and run the container
```bash
docker build -t fastapi-kafka .
docker run -p 5000:5000 fastapi-kafka
```

With Docker Compose use fast-api.yaml and kafka-docker.yaml to spin up FastAPI with Kafka locally:
```bash
docker-compose -f kafka-docker.yaml -f fast-api.yaml up -d
```


## **Kubernetes Usage**

**Deployment.yaml**: 3 replicas with environment variables for Kafka.

**Service.yaml**: LoadBalancer (or NodePort for local) to expose FastAPI.

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```




## **Publish to Kafka**

```bash
curl -X POST \
  http://localhost:5000/kafka/publish/mytopic \
  -H 'Content-Type: application/json' \
  -d '{"key": "value"}'
```

- **Request**

    Path Param: topic_name – Kafka topic to publish to

    Body: JSON object (arbitrary schema)

- **Responses**

    200 OK: Successfully published

    400: Empty body

    413: Message exceeds 10MB

    500: Internal server error

## **Screenshots of local deployment**


![Steps](docker.svg)

![Steps](postman.svg)

![Steps](ui.svg)


## **Metrics**
Prometheus metrics are exposed at `/metrics` (enabled by [prometheus-fastapi-instrumentator](https://github.com/trallard/prometheus-fastapi-instrumentator)).

