# Snapshot of Event Stream

This microservice captures a snapshot of an event stream based on defined criteria, enriches it with additional data from another source, and saves a combined, structured snapshot. So assume the event stream looks like this:
```
{
  "machine_id": "1",
  "event_type": "login",
  "ip": "192.168.0.1",
  "timestamp": "2025-06-13T14:25:30Z"
}
```

### 🔍 Taking a Snapshot

Prior is known that *machine_id = 1* is the **target** machine. If this user logs in or out, this must be captured. e.g.:
```python
if event_type == "login" or event_type == "logout" and machine_id == "1":
    # do
```
 After this filter, *machine_id* is correlated with potential matches in isolated databases,e.g., postgres and mysql. For now these are mock. 

Finally, the results are combined and saved in snapshots.


## Setup Infra

make sure the requirements are shared among pub and sub
```bash
cd pub_sub
cp requirements.txt pub/requirements.txt
cp requirements.txt sub/requirements.txt
```

Start the infra
```bash
docker compose up --build
```
this starts zookeeper, kafka and publisher and subscriber.

### Start Kafka & create topic:
```
docker exec -it kafka kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic message_topic
```
### List topics:
```
docker exec -it kafka kafka-topics --list --bootstrap-server kafka:9092
```
### Produce messages:
```
docker exec -it kafka kafka-console-producer --topic message_topic --bootstrap-server localhost:9092
```
### Consume messages:
```
docker exec -it kafka kafka-console-consumer --topic message_topic --bootstrap-server localhost:9092 --from-beginning
```

## Use Fastapi

### send a message
```
curl -X POST "http://localhost:8000/produce?message=HelloKafka"
```
### use stream.py to send multiple messages
```
python stream.py
```

### consume the messages
```
curl http://localhost:8001/messages
curl http://localhost:8001/snapshots
```

