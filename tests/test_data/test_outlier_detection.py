import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from src.outlier_detection.outlier_detection import detect_and_handle_outliers

@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    np.random.seed(42)
    data = {
        'col1': np.random.normal(0, 1, 1000),
        'col2': np.random.normal(0, 1, 1000)
    }
    # Add some outliers
    data['col1'][0] = 100
    data['col2'][0] = -100
    return pd.DataFrame(data)

def test_outlier_detection(sample_data, tmp_path):
    """Test outlier detection and winsorization"""
    # Save sample data
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"
    sample_data.to_csv(input_path, index=False)
    
    # Run outlier detection
    results = detect_and_handle_outliers(
        str(input_path),
        str(output_path),
        numeric_columns=['col1', 'col2']
    )
    
    # Load processed data
    processed_data = pd.read_csv(output_path)
    
    # Check if outliers were handled
    assert processed_data['col1'].max() < sample_data['col1'].max()
    assert processed_data['col2'].min() > sample_data['col2'].min()