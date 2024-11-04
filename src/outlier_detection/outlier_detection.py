import pandas as pd
import numpy as np
from typing import NamedTuple, List, Optional, Tuple
import argparse
import logging
from pathlib import Path
from .utils import setup_logging, load_config

def winsorize_column(series: pd.Series, limits: Tuple[float, float]) -> pd.Series:
    """
    Winsorize a single column using specified limits.
    """
    lower_limit = series.quantile(limits[0])
    upper_limit = series.quantile(1 - limits[1])
    return pd.Series([
        min(max(x, lower_limit), upper_limit) for x in series
    ], index=series.index)

def detect_and_handle_outliers(
    input_csv_path: str,
    output_csv_path: str,
    numeric_columns: Optional[List[str]] = None,
    limits: Tuple[float, float] = (0.05, 0.05),
    method: str = 'winsorize'
) -> NamedTuple('Outputs', [
    ('output_csv', str),
    ('outlier_report', str)
]):
    """
    Detect and handle outliers in the specified numeric columns of a dataset.
    """
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Processing file: {input_csv_path}")
        
        # Read the input CSV
        df = pd.read_csv(input_csv_path)
        
        # If no columns specified, use all numeric columns
        if numeric_columns is None:
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            logger.info(f"No columns specified. Using all numeric columns: {numeric_columns}")
        
        # Validate columns exist
        for col in numeric_columns:
            if col not in df.columns:
                raise ValueError(f"Column {col} not found in dataset")
        
        # Initialize report
        report_data = []
        
        # Process each column
        for column in numeric_columns:
            logger.info(f"Processing column: {column}")
            original_data = df[column]
            
            # Calculate outlier statistics
            Q1 = original_data.quantile(0.25)
            Q3 = original_data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers_count = len(original_data[(original_data < lower_bound) | 
                                             (original_data > upper_bound)])
            
            # Handle outliers using winsorization
            if method == 'winsorize':
                df[column] = winsorize_column(original_data, limits)
            
            # Add to report
            report_data.append({
                'column': column,
                'outliers_count': outliers_count,
                'outliers_percentage': (outliers_count / len(df)) * 100,
                'original_mean': original_data.mean(),
                'processed_mean': df[column].mean(),
                'original_std': original_data.std(),
                'processed_std': df[column].std(),
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            })
        
        # Create output directory if it doesn't exist
        output_path = Path(output_csv_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save processed data
        df.to_csv(output_csv_path, index=False)
        logger.info(f"Processed data saved to: {output_csv_path}")
        
        # Create report
        report_df = pd.DataFrame(report_data)
        report_path = str(output_path.parent / f"{output_path.stem}_report.csv")
        report_df.to_csv(report_path, index=False)
        logger.info(f"Report saved to: {report_path}")
        
        from collections import namedtuple
        output = namedtuple('Outputs', ['output_csv', 'outlier_report'])
        return output(output_csv_path, report_path)
    
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Outlier Detection and Winsorization')
    parser.add_argument('--input-csv', type=str, required=True,
                      help='Path to input CSV file')
    parser.add_argument('--output-csv', type=str, required=True,
                      help='Path to save processed CSV file')
    parser.add_argument('--numeric-columns', type=str, nargs='*',
                      help='List of numeric column names to process')
    parser.add_argument('--limits', type=float, nargs=2, default=[0.05, 0.05],
                      help='Lower and upper limits for winsorization')
    parser.add_argument('--method', type=str, default='winsorize',
                      help='Method to handle outliers')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    detect_and_handle_outliers(
        args.input_csv,
        args.output_csv,
        args.numeric_columns,
        tuple(args.limits),
        args.method
    )