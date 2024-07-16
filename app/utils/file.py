import yaml
from fastapi import HTTPException

def read_yaml_file(filepath: str) -> dict:
    try:
        with open(filepath, 'r') as file:
            data = yaml.safe_load(file)
            return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading YAML file: {e}")

