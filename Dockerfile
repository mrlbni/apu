# Use official Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Set environment variables (optional defaults, can override when running)
ENV PORT=5000

# Expose the port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
