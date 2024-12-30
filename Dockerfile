FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install PostgreSQL dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    pkg-config \
    && apt-get clean
    
RUN apt-get update && apt-get install -y wget default-jre && apt-get install -y gcc default-jre libmariadb-dev pkg-config &&\
    wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz && \
    tar -xzvf dockerize-linux-amd64-v0.6.1.tar.gz && \
    mv dockerize /usr/local/bin/
    


# Set JAVA_HOME
# ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
# ENV PATH="$JAVA_HOME/bin:$PATH"


COPY requirements.txt /app/

# RUN pip install mysqlclient
RUN pip install --no-cache-dir -r requirements.txt


COPY . /app/

RUN python manage.py collectstatic --noinput


EXPOSE 8000

# Set environment variables for Django
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=product_store_assignment.settings

RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app

# Switch to the new user
USER appuser
CMD ["bash", "-c", "python manage.py collectstatic && python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
