# ETL Technical Test – Data Engineer
This project implements a reproducible ETL pipeline using **Python + Pandas**, delivering a complete **raw** and **curated** data processing workflow, following all mandatory requirements from the technical test.

The solution runs:

- ✅ Locally (Python)  
- ✅ Inside Docker (MSSQL + ETL)  

# Project Structure

etl-test/
├─ README.md
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
│
├─ src/
│  ├─ etl_job.py
│  ├─ api_client.py
│  ├─ transforms.py
│  ├─ db.py
|  ├─ mssql_client.py 
│  └─ utils.py
│
├─ sample_data/
│  ├─ api_orders.json
│
├─ output/
│  ├─ raw/
│  └─ curated/
│
├─ sql/
|  ├─ init.sql
│  └─ redshift-ddl.sql
│
├─ tests/
│  └─ test_transforms.py
│
└─ docs/
   └─ design_notes.md

# How to Run the Project Locally

## 1. Create a virtual environment
Linux/Mac:
```
python3 -m venv venv
source venv/bin/activate
```

Windows:
```
python -m venv venv
venv\Scripts\activate
```

## 2. Install dependencies
```
pip install -r requirements.txt
```

## 3. Run the ETL
Full load:
```
python -m src.etl_job
```

Incremental load:
```
python -m src.etl_job --since "2025-01-01T00:00:00Z"
```

Outputs:
output/raw/
output/curated/date=YYYY-MM-DD/

# Run the Project Using Docker (Optional)

Build:
```
docker-compose build
```

Run ETL:
```
docker-compose run --rm app python -m src.etl_job
```

Incremental:
```
docker-compose run --rm app python -m src.etl_job --since "2025-01-01T00:00:00Z"
```

# Run Tests
```
pytest -q
```

# SQL – Warehouse Tables
DDL located at:
sql/redshift-ddl.sql

Includes:
- dim_user  
- dim_product  
- fact_order  

# Documentation
See docs/design_notes.md

# Notes
- No credentials in repo.
- ETL is idempotent.
- Docker optional.
