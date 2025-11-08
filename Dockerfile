FROM python:3.11-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends         build-essential         ca-certificates         && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY etl ./etl

# Default command (can be overridden by docker-compose)
CMD ["python", "-m", "etl.main"]
