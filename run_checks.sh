#!/bin/bash

echo "Running quality checks..."

echo "1) Running style check..."
ruff check src || exit 1

echo "2) Running tests..."
PYTHONPATH=. pytest -q || exit 1

echo "3) Running full ETL..."
python -m src.etl_job || exit 1

echo "4) Validating outputs..."
if [ ! -d "output/curated" ]; then
    echo "❌ ERROR: Curated output folder missing"
    exit 1
fi

echo "All checks passed ✔"

