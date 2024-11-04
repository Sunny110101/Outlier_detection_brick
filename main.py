from src.outlier_detection.outlier_detection import detect_and_handle_outliers
import argparse

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

def main():
    args = parse_arguments()
    
    try:
        results = detect_and_handle_outliers(
            args.input_csv,
            args.output_csv,
            args.numeric_columns,
            tuple(args.limits),
            args.method
        )
        print(f"\nProcessing completed successfully!")
        print(f"Processed data saved to: {results.output_csv}")
        print(f"Report saved to: {results.outlier_report}")
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise

if __name__ == '__main__':
    main()