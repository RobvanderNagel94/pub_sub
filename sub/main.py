from confluent_kafka import Consumer
from fastapi import FastAPI
import threading
import json

postgres_mock_db = {
    "machine-1": {
        "user": "asia",
        "department": "engineering",
        "os": "linux",
        "location": "Singapore",
        "created_at": "2024-01-10T09:12:34Z"
    },
    "machine-2": {
        "user": "europe",
        "department": "research",
        "os": "linux",
        "location": "Germany",
        "created_at": "2024-03-15T14:22:01Z"
    },
    "machine-3": {
        "user": "afrika",
        "department": "it",
        "os": "windows",
        "location": "Nigeria",
        "created_at": "2023-11-05T18:45:12Z"
    },
    "machine-4": {
        "user": "australia",
        "department": "finance",
        "os": "macOS",
        "location": "Australia",
        "created_at": "2024-06-01T07:00:00Z"
    },
}

mysql_mock_db = {
    "machine-1": {
        "user_type": "offensive",
        "risk_level": "high",
        "patched": False,
        "last_patch_date": "2023-12-20",
        "access_level": "admin"
    },
    "machine-2": {
        "user_type": "defensive",
        "risk_level": "medium",
        "patched": True,
        "last_patch_date": "2024-04-01",
        "access_level": "standard"
    },
    "machine-3": {
        "user_type": "defensive",
        "risk_level": "low",
        "patched": True,
        "last_patch_date": "2024-05-10",
        "access_level": "standard"
    },
    "machine-4": {
        "user_type": "defensive",
        "risk_level": "medium",
        "patched": False,
        "last_patch_date": "2024-02-15",
        "access_level": "elevated"
    },
}

app = FastAPI()

conf = {
    'bootstrap.servers': 'kafka:29092',
    'group.id': 'test-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['message_topic'])

messages = []
snapshots = []

def snapshot(message_value:str):
    try:
        message_dict = json.loads(message_value)
    except json.JSONDecodeError:
        print("Invalid JSON")
        return
    
    if message_dict['machine_id'] == "machine-1":
        if message_dict['event_type'] == "login" or message_dict['event_type'] == "logout":
            print("Taking snapshot...")
            try:
                ps_data = postgres_mock_db.get(message_dict['machine_id'])
                msql_data = mysql_mock_db.get(message_dict['machine_id'])
                if ps_data is None or msql_data is None:
                    print(f"No data found for machine_id: {message_dict['machine_id']}")
                    snapshots.append([
                        message_dict['machine_id'],
                        message_dict['event_type'],
                        message_dict['ip'],
                        message_dict['timestamp'],
                        ])
                else:
                    snapshots.append([
                        message_dict['machine_id'],
                        message_dict['event_type'],
                        message_dict['ip'],
                        message_dict['timestamp'],
                        ps_data,
                        msql_data
                    ])
            except Exception as e:
                print(f"Error occurred: {e}")
                # conc = {**ps_data, **msql_data}  # Merge data from both mock databases
                # postgres_mock_db[message_dict['machine_id']] = message_dict  # Simulate saving to Postgres
                # mysql_mock_db[message_dict['machine_id']] = msql_data  # Simulate saving to MySQL           

            
def consume_loop():
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        value = msg.value().decode('utf-8')
        messages.append(value)
        print(f"Consumed: {value}")
        
        # logic to snapshot messages
        snapshot(value)

@app.get("/messages")
def get_messages():
    return {"messages": messages}

@app.get("/snapshots")
def get_snapshots():
    return {"snapshots": snapshots}

@app.get("/postgres")
def get_postgres():
    return {"postgres": postgres_mock_db}

@app.get("/mysql")
def get_mysql():
    return {"mysql": mysql_mock_db}

# Start Kafka consumer thread
threading.Thread(target=consume_loop, daemon=True).start()
