# 🚀 Slooze Data Engineering Challenge

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Status](https://img.shields.io/badge/Status-Complete-success.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**End-to-end data engineering solution for B2B marketplace data collection and analysis from IndiaMART**

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Results](#results)
- [Technical Approach](#technical-approach)

## 🎯 Overview

This project implements a comprehensive data engineering solution that:

1. **Scrapes product data** from IndiaMART B2B marketplace
2. **Processes and cleans** the data through an ETL pipeline
3. **Analyzes and visualizes** insights through exploratory data analysis

The solution is designed with modularity, scalability, and code quality in mind, following best practices for production-grade data engineering systems.

## ✨ Features

### Part A: Data Collection

- **Robust Web Scraping**: Custom scraper with rate limiting and retry logic
- **Anti-Blocking Mechanisms**: Random delays, user-agent rotation, session management
- **Multiple Categories**: Support for scraping various product categories
- **Error Handling**: Comprehensive error handling and logging
- **Data Validation**: Real-time data validation during scraping

### Part B: ETL Pipeline

- **Data Cleaning**: Handle missing values, duplicates, and inconsistencies
- **Data Transformation**: Standardize formats, extract features, create derived fields
- **Data Quality Checks**: Automated quality validation and reporting
- **Multiple Output Formats**: CSV, JSON, Parquet support
- **Scalable Architecture**: Modular design for easy extension

### Part C: Exploratory Data Analysis

- **Statistical Analysis**: Comprehensive summary statistics and distributions
- **Visualizations**: Publication-quality charts and graphs
- **Geographic Analysis**: Location-based supplier patterns
- **Price Analysis**: Price distributions, outliers, and trends
- **Anomaly Detection**: Identify data quality issues and suspicious patterns
- **Insights Report**: Automated generation of analysis reports

## 📁 Project Structure

```
slooze-data-engineering-challenge/
│
├── src/
│   ├── scraper.py          # Web scraping module
│   ├── etl.py              # ETL pipeline
│   ├── eda.py              # Exploratory data analysis
│   └── utils.py            # Utility functions
│
├── config/
│   └── settings.py         # Configuration settings
│
├── data/
│   ├── raw/                # Raw scraped data
│   ├── processed/          # Processed data
│   └── scraped_data.json   # Raw JSON output
│
├── analysis_results/
│   ├── visualizations/     # Generated charts
│   ├── insights_report.json
│   └── ANALYSIS_REPORT.md  # Human-readable report
│
├── main.py                 # Main execution script
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── SETUP.md               # Detailed setup instructions
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Quick Start

```bash
# Clone the repository
git clone https://github.com/karthikeya2536/slooze-data-engineering-challenge.git
cd slooze-data-engineering-challenge

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

### Run Complete Pipeline

```bash
python main.py
```

This executes all three phases:
1. Data scraping from IndiaMART
2. ETL processing and cleaning
3. Exploratory data analysis with visualizations

### Run Individual Phases

```bash
# Only scraping
python main.py --phase scrape --max-pages 5

# Only ETL
python main.py --phase etl

# Only EDA
python main.py --phase eda
```

### Custom Categories

```bash
# Scrape specific categories
python main.py --phase scrape --categories "industrial machinery" "electronics" "textiles"
```

### Using Individual Modules

```python
# Scraping
from src.scraper import IndiaMARTScraper

scraper = IndiaMARTScraper()
products = scraper.search_products("industrial machinery", max_pages=3)

# ETL
from src.etl import DataETL

etl = DataETL()
processed_data = etl.run_pipeline('data/scraped_data.json')

# EDA
from src.eda import MarketplaceEDA

eda = MarketplaceEDA('data/processed_data.csv')
report = eda.run_complete_analysis()
```

## 🏗️ Architecture

### Scraping Strategy

- **Rate Limiting**: 2-5 second delays between requests to avoid blocking
- **Retry Logic**: Automatic retries with exponential backoff
- **Session Management**: Persistent sessions with proper headers
- **Data Extraction**: BeautifulSoup for HTML parsing with fallback selectors

### ETL Design

```
Extract → Transform → Load
   ↓          ↓          ↓
 JSON    Cleaning    CSV/JSON
         Validation
         Enrichment
```

**Transformation Steps:**
1. Missing value handling
2. Text normalization
3. Price standardization
4. Location parsing
5. Duplicate removal
6. Data validation
7. Feature engineering

### EDA Approach

1. **Descriptive Statistics**: Mean, median, mode, quartiles
2. **Distribution Analysis**: Histograms, box plots, density plots
3. **Categorical Analysis**: Frequency distributions, pie charts
4. **Geographic Analysis**: Regional patterns, city-wise breakdowns
5. **Correlation Analysis**: Relationships between variables
6. **Anomaly Detection**: Outliers, data quality issues

## 📊 Results

After running the complete pipeline, you'll find:

### Generated Files

- `data/scraped_data.json` - Raw scraped data
- `data/processed_data.csv` - Cleaned and processed data
- `analysis_results/ANALYSIS_REPORT.md` - Comprehensive insights report
- `analysis_results/insights_report.json` - Machine-readable insights
- `analysis_results/*.png` - Visualization charts

### Sample Insights

- Product distribution across categories
- Price range analysis and outliers
- Top suppliers and their market share
- Geographic concentration of suppliers
- Data quality metrics and completeness

## 🔧 Technical Approach

### Code Quality

- **Modular Design**: Separate modules for each concern
- **Type Hints**: Python type annotations for better code clarity
- **Documentation**: Comprehensive docstrings and comments
- **Error Handling**: Try-except blocks with proper logging
- **Logging**: Structured logging throughout the pipeline

### Best Practices

- ✅ Virtual environment for dependency isolation
- ✅ Configuration management through settings file
- ✅ Separation of concerns (scraping, ETL, analysis)
- ✅ Comprehensive error handling and logging
- ✅ Data validation at each stage
- ✅ Reproducible results with proper data versioning
- ✅ Clean code principles (DRY, SOLID)

### Performance Considerations

- Efficient data structures (pandas DataFrames)
- Batch processing where applicable
- Memory-efficient operations
- Optimized web requests with session reuse

## 📈 Scalability

The solution can be extended to:

- **Multiple Marketplaces**: Add scrapers for Alibaba, TradeIndia, etc.
- **Distributed Scraping**: Use Celery or Scrapy for parallel scraping
- **Database Integration**: Store data in PostgreSQL, MongoDB, etc.
- **Cloud Deployment**: Deploy on AWS, GCP, or Azure
- **Automated Scheduling**: Use Apache Airflow for scheduled runs
- **Real-time Processing**: Stream processing with Kafka/Flink

## 🔍 Data Quality

The pipeline includes multiple quality checks:

- **Completeness**: Track missing values
- **Validity**: Validate data types and formats
- **Consistency**: Ensure data consistency across fields
- **Uniqueness**: Remove duplicates
- **Accuracy**: Identify outliers and anomalies

## 🤝 Contributing

This is a take-home challenge project. For questions or feedback:

📧 Email: careers@slooze.xyz

## 📝 License

© Slooze. All Rights Reserved.

This material is provided for evaluation purposes only.

## 👨‍💻 Author

**Karthik**
- GitHub: [@karthikeya2536](https://github.com/karthikeya2536)

---

## 📚 Additional Documentation

For detailed setup instructions, see [SETUP.md](SETUP.md)

For technical documentation, refer to inline code comments and docstrings.

## 🎓 Learning Outcomes

This project demonstrates:

1. Web scraping with Python (requests, BeautifulSoup)
2. ETL pipeline design and implementation
3. Data cleaning and transformation with pandas
4. Exploratory data analysis
5. Data visualization with matplotlib/seaborn
6. Code organization and best practices
7. Production-ready error handling and logging

---

**Built with ❤️ for Slooze Data Engineering Challenge**
