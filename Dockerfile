# Use official NVIDIA CUDA base image with Python 3 support
FROM nvidia/cuda:12.8.0-cudnn-devel-ubuntu22.04

# Set environment variables for non-interactive apt installs
ENV DEBIAN_FRONTEND=noninteractive

# Install Python3, pip, and essential build tools
RUN apt update && \
    apt install -y \
    python3 \
    python3-pip \
    build-essential \
    && apt clean

# Upgrade pip to the latest version
RUN python3 -m pip install --upgrade pip

# Set the working directory in the container
WORKDIR /app

# Copy your Python application into the container
COPY . /app

# Install Python dependencies from requirements.txt (if available)
RUN pip3 install -r requirements.txt

RUN llm install llm-rag

# Command to run the app (replace 'your_app.py' with your actual app script)
CMD ["python3", "your_app.py"]
