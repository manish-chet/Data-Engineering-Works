# FastAPI Kafka Producer API

This project provides a FastAPI-based REST API for publishing messages to Apache Kafka topics. It is containerized with Docker and supports metrics via Prometheus. The API is designed for high availability and scalability, suitable for production environments.

![Steps](fastapi.svg)

## **Features**
- Publish to Kafka: Send JSON messages to any Kafka topic via a REST endpoint.
- Health Check: Simple endpoint to verify service status.
- Prometheus Metrics: Exposes metrics for monitoring.
- Logging: Rotating file logging for API activity and errors.
- Dockerized: Ready for containerized deployment and orchestration.

## **Requirements**
- Python 3.9+
- Kafka cluster
- Docker/Kubernetes for containerized deployment

## Installation (Local Development)
1. Clone the repository
   ```bash
   git clone https://github.com/manish-chet/fastapipythonkafka
   cd fastapipythonkafka
   ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Run the FastAPI app
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 5000 --reload
   ```

## **Docker Usage**
1. Build the Docker image
   ```bash
   docker build -t fastapi-kafka .
   ```
2. Run the container
   ```bash
   docker run -p 5000:5000 fastapi-kafka
   ```
3. Deploy using stack
   ```bash
   docker stack deploy -c docker-compose-stack.yaml fastapi-kafka-stack
   ```

## **Kubernetes Usage**
Deploy using following yamls in kubernetes

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```


## **Configuration**
- Kafka Servers: Update the `bootstrap_servers`, `username`, `password`, and `ssl_cafile` in `main.py` as needed for your Kafka cluster.
- Logging: Logs are written to `/var/log/fastapi_kafka_api.log` (mount a volume if running in Docker/Kubernetes).


## **Publish to Kafka**
- POST `/kafka/publish/{topic_name}`
  - Path Parameter: `topic_name` (string) — Kafka topic to publish to
  - Body: JSON object (arbitrary structure)
  - Response:
    - Success: `{ "status": "success", "message": "Data sent to Kafka topic '{topic_name}'" }`
    - Error: HTTP 400 (empty body), HTTP 413 (message too large), HTTP 500 (server error)

## **Example Request**
```bash
curl -X POST \
  http://localhost:5000/kafka/publish/mytopic \
  -H 'Content-Type: application/json' \
  -d '{"key": "value"}'
```

## Metrics
Prometheus metrics are exposed at `/metrics` (enabled by [prometheus-fastapi-instrumentator](https://github.com/trallard/prometheus-fastapi-instrumentator)).

