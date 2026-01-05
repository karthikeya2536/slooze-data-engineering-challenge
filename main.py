#!/usr/bin/env python3
"""Main Execution Script

This script orchestrates the complete data engineering pipeline:
1. Web scraping from IndiaMART
2. ETL processing
3. Exploratory Data Analysis
"""

import sys
import os
import logging
import argparse

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from scraper import IndiaMARTScraper
from etl import DataETL
from eda import MarketplaceEDA
from config.settings import SCRAPER_CONFIG, ETL_CONFIG
import utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_scraping(categories=None, max_pages=3):
    """Run web scraping phase
    
    Args:
        categories: List of categories to scrape
        max_pages: Maximum pages per category
    """
    logger.info("\n" + "="*60)
    logger.info("PHASE 1: WEB SCRAPING")
    logger.info("="*60 + "\n")
    
    if categories is None:
        categories = SCRAPER_CONFIG['categories']
    
    scraper = IndiaMARTScraper(
        delay_range=SCRAPER_CONFIG['delay_range']
    )
    
    results = scraper.scrape_multiple_categories(
        categories=categories,
        max_pages_per_category=max_pages
    )
    
    # Save results
    output_file = ETL_CONFIG['raw_data_file']
    utils.save_json(results, output_file)
    
    logger.info(f"\nScraping complete! Data saved to {output_file}")
    return results


def run_etl(input_file=None, output_file=None):
    """Run ETL processing phase
    
    Args:
        input_file: Path to raw data
        output_file: Path for processed data
    """
    logger.info("\n" + "="*60)
    logger.info("PHASE 2: ETL PROCESSING")
    logger.info("="*60 + "\n")
    
    if input_file is None:
        input_file = ETL_CONFIG['raw_data_file']
    if output_file is None:
        output_file = ETL_CONFIG['processed_data_file']
    
    etl = DataETL()
    processed_data = etl.run_pipeline(input_file, output_file)
    
    logger.info(f"\nETL complete! Processed data saved to {output_file}")
    return processed_data


def run_eda(data_file=None):
    """Run exploratory data analysis phase
    
    Args:
        data_file: Path to processed data
    """
    logger.info("\n" + "="*60)
    logger.info("PHASE 3: EXPLORATORY DATA ANALYSIS")
    logger.info("="*60 + "\n")
    
    if data_file is None:
        data_file = ETL_CONFIG['processed_data_file']
    
    eda = MarketplaceEDA(data_file)
    report = eda.run_complete_analysis()
    
    logger.info("\nEDA complete! Results saved to analysis_results/")
    return report


def run_full_pipeline(categories=None, max_pages=3):
    """Run complete data engineering pipeline
    
    Args:
        categories: List of categories to scrape
        max_pages: Maximum pages per category
    """
    logger.info("\n" + "#"*60)
    logger.info("SLOOZE DATA ENGINEERING CHALLENGE")
    logger.info("Full Pipeline Execution")
    logger.info("#"*60 + "\n")
    
    try:
        # Phase 1: Scraping
        run_scraping(categories, max_pages)
        
        # Phase 2: ETL
        run_etl()
        
        # Phase 3: EDA
        run_eda()
        
        logger.info("\n" + "#"*60)
        logger.info("PIPELINE COMPLETE!")
        logger.info("#"*60)
        logger.info("\nGenerated files:")
        logger.info(f"  - Raw data: {ETL_CONFIG['raw_data_file']}")
        logger.info(f"  - Processed data: {ETL_CONFIG['processed_data_file']}")
        logger.info(f"  - Analysis results: analysis_results/")
        logger.info("\nCheck analysis_results/ANALYSIS_REPORT.md for insights!\n")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Slooze Data Engineering Challenge - B2B Marketplace Scraper'
    )
    parser.add_argument(
        '--phase',
        choices=['scrape', 'etl', 'eda', 'full'],
        default='full',
        help='Pipeline phase to run'
    )
    parser.add_argument(
        '--categories',
        nargs='+',
        help='Categories to scrape (space-separated)'
    )
    parser.add_argument(
        '--max-pages',
        type=int,
        default=3,
        help='Maximum pages to scrape per category'
    )
    
    args = parser.parse_args()
    
    if args.phase == 'scrape':
        run_scraping(args.categories, args.max_pages)
    elif args.phase == 'etl':
        run_etl()
    elif args.phase == 'eda':
        run_eda()
    else:
        run_full_pipeline(args.categories, args.max_pages)
