"""Utility Functions Module

Common utility functions used across the project.
"""

import logging
import json
import os
from typing import Any, Dict
from datetime import datetime


def setup_logging(log_level=logging.INFO, log_file: str = None):
    """Setup logging configuration
    
    Args:
        log_level: Logging level
        log_file: Optional log file path
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    if log_file:
        logging.basicConfig(
            level=log_level,
            format=log_format,
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    else:
        logging.basicConfig(level=log_level, format=log_format)


def save_json(data: Any, filepath: str, indent: int = 2):
    """Save data to JSON file
    
    Args:
        data: Data to save
        filepath: Output file path
        indent: JSON indentation
    """
    os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=indent)


def load_json(filepath: str) -> Any:
    """Load data from JSON file
    
    Args:
        filepath: Input file path
        
    Returns:
        Loaded data
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def create_directory(directory: str):
    """Create directory if it doesn't exist
    
    Args:
        directory: Directory path
    """
    os.makedirs(directory, exist_ok=True)


def get_timestamp() -> str:
    """Get current timestamp string
    
    Returns:
        Formatted timestamp
    """
    return datetime.now().strftime('%Y%m%d_%H%M%S')


def print_separator(char: str = '=', length: int = 60):
    """Print a separator line
    
    Args:
        char: Character to use
        length: Length of separator
    """
    print(char * length)
