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
python -m pytest tests/
```