FROM python:3.12-slim

# Install system dependencies required by GeoPandas and PostGIS
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    libpq-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir gdal==3.10.3

WORKDIR /app

COPY ../app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ../app/ .

ENV DB_HOST=localhost \
    DB_PORT=5432 \
    DB_NAME=asterra_db \
    DB_USER=asterra_user \
    DB_PASSWORD=localstack_pass \
    S3_ENDPOINT=http://localhost:4566 \
    AWS_REGION=us-east-1

EXPOSE 5000

CMD ["python", "main.py"]
