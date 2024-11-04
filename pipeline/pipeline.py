import kfp
from kfp import components
from kfp import dsl

def create_outlier_detection_pipeline(
    input_csv: str,
    numeric_columns: list = None,
    limits: list = [0.05, 0.05]
):
    """Create a pipeline for outlier detection"""
    outlier_detection_op = components.load_component_from_file(
        str(Path(__file__).parent / 'component.yaml')
    )
    
    @dsl.pipeline(
        name='Outlier Detection Pipeline',
        description='Pipeline for detecting and handling outliers'
    )
    def pipeline():
        outlier_detection = outlier_detection_op(
            input_csv=input_csv,
            numeric_columns=numeric_columns,
            limits=limits
        )
    
    return pipeline

if __name__ == '__main__':
    kfp.Client().create_run_from_pipeline_func(
        create_outlier_detection_pipeline,
        arguments={
            'input_csv': 'data/input.csv',
            'numeric_columns': ['column1', 'column2']
        }
    )