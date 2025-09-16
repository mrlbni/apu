# Use Python 3.12 slim
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set workdir
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py .

# Expose port
EXPOSE 5000

# Start Flask app
CMD ["python", "app.py"]
