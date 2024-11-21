# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /back-end

# Copy the requirements.txt file into the container
COPY back-end/requirements.txt ./requirements.txt

# Upgrade pip
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY back-end/ ./ 

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run migrations and then start the server
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]