import subprocess
import random
import time
import pydantic

# curl -X POST "http://localhost:8000/produce?message=HelloKafka"
# curl http://localhost:8001/messages

import random
import time
import pydantic
import requests

class Event(pydantic.BaseModel):
    machine_id: str
    event_type: str
    ip: str
    timestamp: str

machine_ids = [f"machine-{i+1}" for i in range(100)]
event_types = ['login', 'exec', 'bin/zsh', 'bin/fish', "chmod", "sudo", "logout", "mkdir", "rmdir"]
ips = [f"127.{random.randint(1, 9)}.{random.randint(1, 9)}.{random.randint(1, 255)}" for _ in range(10)]

def stream():
    cnt = 0
    while cnt < 1000:
        cnt += 1
        event = Event(
            machine_id=random.choice(machine_ids),
            event_type=random.choice(event_types),
            ip=random.choice(ips),
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )
        response = requests.post("http://localhost:8000/produce", params={"message": event.json()})
        print(response.json())
        #time.sleep(0.1)  # optional rate limit

if __name__ == "__main__":
    stream()
