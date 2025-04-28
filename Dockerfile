# Use slim lightweight official Python 3.11 imagebuild
FROM python:3.11-slim

# Install system packages needed for Streamlit frontend, image processing, and Supervisor
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    supervisor \
    && apt-get clean

# Install uv (faster pip alternative)
RUN pip install uv

# Set working directory inside container
WORKDIR /app

# First copy requirements file and install dependencies (layer cache optimization)
COPY requirements.txt .

# Install dependencies with uv
RUN uv pip install --system -r requirements.txt

# Now copy the full project
COPY . .

# Expose necessary ports: FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Copy supervisord config to manage multiple services
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Start both backend and frontend using Supervisor
CMD ["supervisord", "-n"]
