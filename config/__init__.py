from pathlib import Path
import yaml

CONFIG_PATH = Path(__file__).parent / "config.yaml"

def get_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)