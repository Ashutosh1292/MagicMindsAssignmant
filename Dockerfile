# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install PostgreSQL dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    pkg-config \
    && apt-get clean
RUN apt-get update && apt-get install -y wget && \
    wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz && \
    tar -xzvf dockerize-linux-amd64-v0.6.1.tar.gz && \
    mv dockerize /usr/local/bin/
# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install any dependencies
# RUN pip install mysqlclient
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . /app/

RUN python manage.py collectstatic --noinput

# Apply database migrations
# RUN python manage.py makemigrations
# RUN python manage.py migrate
# Expose the port your Django app will run on
EXPOSE 8000

# Set environment variables for Django
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=product_store_assignment.settings

# RUN python manage.py makemigrations
# RUN python manage.py migrate
# RUN docker-compose exec web python manage.py migrate
# Run the migrations and start the server
CMD ["bash", "-c", "python manage.py collectstatic && python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
