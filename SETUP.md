# 🔧 Detailed Setup Instructions

This guide provides step-by-step instructions for setting up and running the Slooze Data Engineering Challenge.

## Prerequisites

### System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: At least 500MB free space

### Software Requirements

1. **Python 3.8+**
   ```bash
   # Check Python version
   python --version
   # or
   python3 --version
   ```

2. **pip** (Python package manager)
   ```bash
   # Check pip version
   pip --version
   ```

3. **Git**
   ```bash
   # Check git version
   git --version
   ```

## Installation Steps

### 1. Clone the Repository

```bash
# Using HTTPS
git clone https://github.com/karthikeya2536/slooze-data-engineering-challenge.git

# Or using SSH
git clone git@github.com:karthikeya2536/slooze-data-engineering-challenge.git

# Navigate to project directory
cd slooze-data-engineering-challenge
```

### 2. Create Virtual Environment

**Why use a virtual environment?**
- Isolates project dependencies
- Prevents version conflicts
- Makes the project portable

#### On Linux/macOS:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

#### On Windows:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your command prompt
```

### 3. Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

### 4. Verify Installation

```bash
# Test imports
python -c "import requests, bs4, pandas, matplotlib, seaborn; print('All dependencies installed successfully!')"
```

## Running the Project

### Option 1: Full Pipeline (Recommended)

```bash
# Run complete pipeline: Scraping + ETL + EDA
python main.py
```

**Expected Output:**
- Console logs showing progress
- `data/scraped_data.json` - Raw data
- `data/processed_data.csv` - Cleaned data
- `analysis_results/` directory with visualizations and reports

**Estimated Time**: 10-20 minutes (depends on network speed and pages scraped)

### Option 2: Individual Phases

#### Phase 1: Scraping Only

```bash
# Scrape with default settings
python main.py --phase scrape

# Scrape with custom parameters
python main.py --phase scrape --max-pages 5 --categories "electronics" "machinery"
```

#### Phase 2: ETL Only

```bash
# Process existing raw data
python main.py --phase etl
```

**Prerequisites**: `data/scraped_data.json` must exist

#### Phase 3: EDA Only

```bash
# Analyze existing processed data
python main.py --phase eda
```

**Prerequisites**: `data/processed_data.csv` must exist

### Option 3: Using Python Scripts Directly

```python
# In Python interactive shell or Jupyter notebook

# Scraping
from src.scraper import IndiaMARTScraper
scraper = IndiaMARTScraper()
results = scraper.search_products("industrial machinery", max_pages=2)

# ETL
from src.etl import DataETL
etl = DataETL()
df = etl.run_pipeline('data/scraped_data.json')

# EDA
from src.eda import MarketplaceEDA
eda = MarketplaceEDA('data/processed_data.csv')
report = eda.run_complete_analysis()
```

## Configuration

### Customizing Settings

Edit `config/settings.py` to customize:

```python
# Number of pages to scrape per category
max_pages_per_category = 5

# Delay between requests (seconds)
delay_range = (2, 5)

# Categories to scrape
categories = [
    'your_category_1',
    'your_category_2',
    # Add more categories
]
```

## Troubleshooting

### Common Issues

#### Issue 1: Module Not Found Error

```
ModuleNotFoundError: No module named 'requests'
```

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### Issue 2: Permission Denied

```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash
# On Linux/macOS
sudo chmod +x main.py

# Or run with python explicitly
python main.py
```

#### Issue 3: Network/Scraping Errors

```
Error: Failed to fetch URL after retries
```

**Possible Causes:**
- No internet connection
- Website blocking requests
- Rate limiting

**Solutions:**
- Check internet connection
- Increase delay between requests in `config/settings.py`
- Try with fewer pages: `--max-pages 1`
- Use VPN if IP is blocked

#### Issue 4: Memory Error

```
MemoryError: Unable to allocate array
```

**Solution:**
- Reduce number of pages to scrape
- Process data in smaller batches
- Close other applications

### Getting Help

 If you encounter issues:

1. Check the console logs for error messages
2. Verify all prerequisites are installed
3. Ensure virtual environment is activated
4. Check `requirements.txt` versions match your environment

## Project Output

After successful execution, you should have:

```
slooze-data-engineering-challenge/
├── data/
│   ├── scraped_data.json          # Raw scraped data
│   └── processed_data.csv         # Cleaned data
│
├── analysis_results/
│   ├── category_distribution.png
│   ├── price_distribution.png
│   ├── top_cities.png
│   ├── top_suppliers.png
│   ├── insights_report.json
│   ├── summary_statistics.json
│   └── ANALYSIS_REPORT.md         # Main report
```

## Next Steps

1. **Review Results**: Check `analysis_results/ANALYSIS_REPORT.md`
2. **Explore Data**: Open `data/processed_data.csv` in Excel or pandas
3. **Customize**: Modify categories and parameters
4. **Extend**: Add new features or analysis

## Development Workflow

### Making Changes

```bash
# Create a new branch
git checkout -b feature/my-new-feature

# Make your changes
# ...

# Test your changes
python main.py

# Commit changes
git add .
git commit -m "Add: description of changes"

# Push to GitHub
git push origin feature/my-new-feature
```

## Performance Tips

1. **Start Small**: Test with 1-2 pages first
2. **Monitor Resources**: Watch CPU and memory usage
3. **Adjust Delays**: Balance speed vs. blocking risk
4. **Use Caching**: Save intermediate results
5. **Parallel Processing**: For large-scale scraping

## Best Practices

1. **Always use virtual environment**
2. **Keep dependencies updated** (but test after updates)
3. **Version control your changes** with git
4. **Backup data** before reprocessing
5. **Document custom changes** in code comments
6. **Test incrementally** after each change

---

## Additional Resources

- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Web Scraping Best Practices](https://www.scraperapi.com/blog/web-scraping-best-practices/)

---

**Ready to run?** Execute:
```bash
python main.py
```

And watch the magic happen! ✨
