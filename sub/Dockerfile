FROM python:3.11-slim

WORKDIR /app

# RUN pip install confluent-kafka fastapi uvicorn pydantic requests
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
        
