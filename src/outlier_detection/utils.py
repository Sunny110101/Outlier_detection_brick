import yaml
import logging
from pathlib import Path
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)

def setup_logging():
    """Setup logging configuration"""
    config = load_config()
    logging.basicConfig(
        level=config["outlier_detection"]["logging"]["level"],
        format=config["outlier_detection"]["logging"]["format"]
    )