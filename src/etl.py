"""ETL Pipeline Module

This module handles Extract, Transform, and Load operations for scraped data.
It cleans, validates, and structures the raw scraped data.
"""

import pandas as pd
import json
import logging
from typing import Dict, List, Optional
import re
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataETL:
    """ETL pipeline for processing scraped marketplace data"""
    
    def __init__(self):
        self.raw_data = None
        self.processed_data = None
    
    def extract(self, source: str) -> pd.DataFrame:
        """Extract data from JSON file or dictionary
        
        Args:
            source: Path to JSON file or dictionary
            
        Returns:
            DataFrame with raw extracted data
        """
        logger.info("Starting data extraction...")
        
        if isinstance(source, str):
            # Load from file
            with open(source, 'r') as f:
                data = json.load(f)
        elif isinstance(source, dict):
            data = source
        else:
            raise ValueError("Source must be a file path or dictionary")
        
        # Flatten nested structure
        all_products = []
        for category, products in data.items():
            for product in products:
                product['category'] = category
                all_products.append(product)
        
        self.raw_data = pd.DataFrame(all_products)
        logger.info(f"Extracted {len(self.raw_data)} records")
        
        return self.raw_data
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform and clean the extracted data
        
        Args:
            df: Raw DataFrame
            
        Returns:
            Cleaned and transformed DataFrame
        """
        logger.info("Starting data transformation...")
        
        df_clean = df.copy()
        
        # 1. Handle missing values
        df_clean = self._handle_missing_values(df_clean)
        
        # 2. Clean text fields
        df_clean = self._clean_text_fields(df_clean)
        
        # 3. Parse and standardize prices
        df_clean = self._standardize_prices(df_clean)
        
        # 4. Extract location information
        df_clean = self._parse_locations(df_clean)
        
        # 5. Add derived fields
        df_clean = self._add_derived_fields(df_clean)
        
        # 6. Remove duplicates
        df_clean = self._remove_duplicates(df_clean)
        
        # 7. Data validation
        df_clean = self._validate_data(df_clean)
        
        self.processed_data = df_clean
        logger.info(f"Transformation complete. {len(df_clean)} records after cleaning")
        
        return df_clean
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in the dataset"""
        logger.info("Handling missing values...")
        
        # Fill missing string fields with 'Unknown'
        text_columns = ['product_name', 'company_name', 'location']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].fillna('Unknown')
        
        # Drop rows with missing critical information
        if 'product_name' in df.columns:
            df = df[df['product_name'] != 'Unknown']
        
        return df
    
    def _clean_text_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize text fields"""
        logger.info("Cleaning text fields...")
        
        text_columns = ['product_name', 'company_name', 'location', 'category']
        
        for col in text_columns:
            if col in df.columns:
                # Remove extra whitespace
                df[col] = df[col].str.strip()
                df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
                
                # Remove special characters (keep alphanumeric and basic punctuation)
                df[col] = df[col].str.replace(r'[^\w\s,.-]', '', regex=True)
        
        return df
    
    def _standardize_prices(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize price information"""
        logger.info("Standardizing prices...")
        
        if 'price' in df.columns:
            # Convert to numeric
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            
            # Create price categories
            df['price_category'] = pd.cut(
                df['price'],
                bins=[0, 1000, 10000, 100000, float('inf')],
                labels=['Budget', 'Mid-Range', 'Premium', 'Enterprise'],
                include_lowest=True
            )
        
        return df
    
    def _parse_locations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Parse and standardize location information"""
        logger.info("Parsing locations...")
        
        if 'location' in df.columns:
            # Extract city (usually first part before comma)
            df['city'] = df['location'].str.split(',').str[0].str.strip()
            
            # Extract state (if present)
            df['state'] = df['location'].str.split(',').str[-1].str.strip()
            
            # Identify major cities
            major_cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 
                          'Hyderabad', 'Pune', 'Ahmedabad', 'Surat', 'Jaipur']
            df['is_major_city'] = df['city'].isin(major_cities)
        
        return df
    
    def _add_derived_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add derived analytical fields"""
        logger.info("Adding derived fields...")
        
        # Add timestamp if not present
        if 'timestamp' not in df.columns:
            df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Parse timestamp
        df['scraped_date'] = pd.to_datetime(df['timestamp'], errors='coerce')
        
        # Add product name length (can indicate detail level)
        if 'product_name' in df.columns:
            df['name_length'] = df['product_name'].str.len()
        
        # Flag products with images
        if 'image_url' in df.columns:
            df['has_image'] = df['image_url'].notna()
        
        return df
    
    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate entries"""
        logger.info("Removing duplicates...")
        
        initial_count = len(df)
        
        # Remove exact duplicates
        df = df.drop_duplicates()
        
        # Remove duplicates based on product name and company
        if 'product_name' in df.columns and 'company_name' in df.columns:
            df = df.drop_duplicates(subset=['product_name', 'company_name'], keep='first')
        
        removed = initial_count - len(df)
        if removed > 0:
            logger.info(f"Removed {removed} duplicate records")
        
        return df
    
    def _validate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate data quality"""
        logger.info("Validating data...")
        
        # Remove rows with invalid prices (negative or unrealistic)
        if 'price' in df.columns:
            df = df[(df['price'].isna()) | (df['price'] > 0)]
            df = df[(df['price'].isna()) | (df['price'] < 10000000)]  # Max 1 crore
        
        # Validate URL formats
        if 'product_url' in df.columns:
            df = df[df['product_url'].str.contains('http', na=True)]
        
        return df
    
    def load(self, df: pd.DataFrame, output_path: str, format: str = 'csv'):
        """Load processed data to file
        
        Args:
            df: Processed DataFrame
            output_path: Output file path
            format: Output format ('csv', 'json', 'parquet')
        """
        logger.info(f"Loading data to {output_path}...")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        
        if format == 'csv':
            df.to_csv(output_path, index=False)
        elif format == 'json':
            df.to_json(output_path, orient='records', indent=2)
        elif format == 'parquet':
            df.to_parquet(output_path, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        logger.info(f"Data successfully saved to {output_path}")
    
    def get_data_quality_report(self, df: pd.DataFrame) -> Dict:
        """Generate data quality report
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary with quality metrics
        """
        report = {
            'total_records': len(df),
            'columns': list(df.columns),
            'missing_values': df.isnull().sum().to_dict(),
            'duplicate_count': df.duplicated().sum(),
            'memory_usage': f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB"
        }
        
        # Add column-specific stats
        if 'price' in df.columns:
            report['price_stats'] = {
                'count': df['price'].notna().sum(),
                'mean': float(df['price'].mean()) if df['price'].notna().any() else None,
                'median': float(df['price'].median()) if df['price'].notna().any() else None,
                'min': float(df['price'].min()) if df['price'].notna().any() else None,
                'max': float(df['price'].max()) if df['price'].notna().any() else None
            }
        
        return report
    
    def run_pipeline(self, source: str, output_path: str = 'data/processed_data.csv'):
        """Run complete ETL pipeline
        
        Args:
            source: Input data source
            output_path: Output file path
        """
        logger.info("\n" + "="*60)
        logger.info("Starting ETL Pipeline")
        logger.info("="*60 + "\n")
        
        # Extract
        raw_df = self.extract(source)
        
        # Transform
        processed_df = self.transform(raw_df)
        
        # Load
        self.load(processed_df, output_path)
        
        # Generate quality report
        quality_report = self.get_data_quality_report(processed_df)
        
        logger.info("\n" + "="*60)
        logger.info("ETL Pipeline Complete")
        logger.info("="*60)
        logger.info(f"\nQuality Report:\n{json.dumps(quality_report, indent=2)}")
        
        return processed_df


if __name__ == "__main__":
    # Example usage
    etl = DataETL()
    processed_data = etl.run_pipeline('scraped_data.json', 'data/processed_data.csv')
