FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy root requirements (if needed for web only)
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir flask python-dotenv livekit-api

# Copy web application
COPY web/ .

EXPOSE 5000

CMD ["python", "app.py"]