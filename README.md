# Outlier Detection Component

A reusable component for outlier detection and winsorization that can be used standalone or as part of a Kubeflow pipeline.

## Setup

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Build Docker image:
```bash
docker-compose build
```

## Usage

### Standalone Usage
```bash
python -m src.outlier_detection.outlier_detection \
    --input-csv path/to/input.csv \
    --output-csv path/to/output.csv \
    --numeric-columns column1 column2 \
    --limits 0.05 0.05
```
### Kubeflow Pipeline Usage

### As Pipeline Component
```python
from pipeline.pipeline import create_outlier_detection_pipeline
pipeline.create_run_from_pipeline_func(create_outlier_detection_pipeline, arguments={})
```

## Testing
```bash

## Docker Run
docker run -v .:/app `
    4d24fe9b2efa `
    --input-csv /app/data/input/axle_clean_data.csv `
    --output-csv /app/data/output/processed_data.csv `
    --numeric-columns humidity temperature vpr_current_val vpr_voltage_val unit1_current_val unit1_voltage_val `
    --limits 0.05 0.95 `
    --method detect
python -m pytest tests/
```
