# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /code

# Install system dependencies for building and Python package dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /code
COPY . /code/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt --verbose

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables to avoid pyc files and buffer issues
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
