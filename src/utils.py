"""
Utility functions for DuPont Tedlar Lead Generation.
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional

import yaml

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config(config_path: str) -> Dict:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dict: Configuration data
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Load environment variables for API keys
        for service, key_var in config.get('api_keys', {}).items():
            if isinstance(key_var, str) and key_var.startswith('${') and key_var.endswith('}'):
                env_var = key_var[2:-1]
                config['api_keys'][service] = os.environ.get(env_var, '')
        
        return config
    except Exception as e:
        logger.error(f"Error loading config from {config_path}: {e}")
        # Return empty config if loading fails
        return {}

def save_json(data: Any, output_file: str) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Data to save
        output_file: Path to save the data
    """
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving data to {output_file}: {e}")

def load_json(input_file: str) -> Any:
    """
    Load data from a JSON file.
    
    Args:
        input_file: Path to the JSON file
        
    Returns:
        Any: Loaded data
    """
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        logger.error(f"Error loading data from {input_file}: {e}")
        return []

def validate_data(data: Any, schema_type: str) -> bool:
    """
    Validate data against a schema.
    
    Args:
        data: Data to validate
        schema_type: Type of schema to validate against
        
    Returns:
        bool: Whether the data is valid
    """
    # In a production system, we would use jsonschema to validate data
    # For the prototype, we'll just check that required fields are present
    
    if schema_type == 'company':
        required_fields = ['name', 'website']
    elif schema_type == 'stakeholder':
        required_fields = ['name', 'title', 'linkedin_url']
    elif schema_type == 'event':
        required_fields = ['name', 'date', 'location']
    else:
        logger.warning(f"Unknown schema type: {schema_type}")
        return False
    
    # Check if all required fields are present
    if isinstance(data, dict):
        return all(field in data for field in required_fields)
    elif isinstance(data, list):
        return all(all(field in item for field in required_fields) for item in data)
    else:
        logger.warning(f"Data is not a dict or list: {type(data)}")
        return False