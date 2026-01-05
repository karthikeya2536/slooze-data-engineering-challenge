"""Configuration Settings

Central configuration for the data engineering pipeline.
"""

import os

# Project structure
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
ANALYSIS_DIR = os.path.join(BASE_DIR, 'analysis_results')

# Scraper settings
SCRAPER_CONFIG = {
    'delay_range': (2, 5),  # Seconds between requests
    'max_retries': 3,
    'timeout': 15,
    'max_pages_per_category': 3,
    'categories': [
        'industrial machinery',
        'electronics components',
        'textile machinery',
        'packaging machines',
        'construction equipment'
    ]
}

# ETL settings
ETL_CONFIG = {
    'input_format': 'json',
    'output_format': 'csv',
    'raw_data_file': os.path.join(DATA_DIR, 'scraped_data.json'),
    'processed_data_file': os.path.join(DATA_DIR, 'processed_data.csv'),
}

# EDA settings
EDA_CONFIG = {
    'figure_size': (12, 6),
    'dpi': 300,
    'style': 'whitegrid'
}

# Logging settings
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}

# Create necessary directories
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, ANALYSIS_DIR]:
    os.makedirs(directory, exist_ok=True)
