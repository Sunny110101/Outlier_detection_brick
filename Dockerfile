# Use slim python image for smaller size
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire project directory
COPY . /app/

# Create necessary directories if they don't exist
RUN mkdir -p /app/data/input /app/data/output

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

# Set Python path and environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Default command
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]