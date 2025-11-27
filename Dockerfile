FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install FreeTDS + ODBC
RUN apt-get update && apt-get install -y \
    freetds-dev \
    freetds-bin \
    tdsodbc \
    unixodbc \
    unixodbc-dev \
    python3-dev \
    build-essential \
    iputils-ping \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Configure FreeTDS driver in ODBC
RUN echo "[FreeTDS]\n\
Description=FreeTDS MSSQL Driver\n\
Driver=/usr/lib/odbc/libtdsodbc.so\n\
Setup=/usr/lib/odbc/libtdsS.so\n\
UsageCount=1" >> /etc/odbcinst.ini

# Add freetds.conf with correct settings for SQL Server 2019
COPY freetds.conf /etc/freetds/freetds.conf

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY sample_data ./sample_data
COPY sql ./sql
COPY output ./output

ENV PYTHONPATH=/app

CMD ["python3", "-m", "src.etl_job"]


