FROM python:3.11-slim

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY src ./src
COPY sample_data ./sample_data
COPY sql ./sql
COPY output ./output

# Copy quality check script
COPY run_checks.sh .
RUN chmod +x run_checks.sh

ENV PYTHONPATH=/app

CMD ["python3", "-m", "src.etl_job"]


