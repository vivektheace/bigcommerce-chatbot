# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose backend (8000) and frontend (8501) ports
EXPOSE 8000 8501

# Install supervisor to manage multiple processes
RUN apt-get update && apt-get install -y supervisor

# Copy supervisord config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Start both backend and frontend
CMD ["supervisord", "-n"]
