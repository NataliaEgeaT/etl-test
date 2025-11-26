FROM python:3.11-slim

# System dependencies for pyodbc
RUN apt-get update && \
    apt-get install -y unixodbc unixodbc-dev curl gnupg && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY sample_data ./sample_data
COPY sql ./sql
COPY output ./output

ENV PYTHONPATH=/app

CMD ["python", "-m", "src.etl_job"]
