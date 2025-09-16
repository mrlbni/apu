# Use Python 3.12 slim
FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Install system dependencies for pyrogram/tgcrypto
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libssl-dev \
        python3-dev \
        git \
        curl \
        && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py .

# Expose port
EXPOSE 5000

# Start Flask app
CMD ["python", "app.py"]
