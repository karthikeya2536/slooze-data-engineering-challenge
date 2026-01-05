"""Exploratory Data Analysis Module

This module performs comprehensive EDA on the processed marketplace data,
generating insights, visualizations, and statistical summaries.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import os
from typing import Dict, List, Optional
import json
from collections import Counter
import warnings

warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set style for better-looking plots
sns.set_style('whitegrid')
sns.set_palette('husl')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


class MarketplaceEDA:
    """Exploratory Data Analysis for marketplace data"""
    
    def __init__(self, data_path: str):
        """Initialize EDA with data path
        
        Args:
            data_path: Path to processed CSV data
        """
        self.data_path = data_path
        self.df = None
        self.insights = {}
        self.output_dir = 'analysis_results'
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_data(self):
        """Load processed data"""
        logger.info(f"Loading data from {self.data_path}...")
        self.df = pd.read_csv(self.data_path)
        logger.info(f"Loaded {len(self.df)} records with {len(self.df.columns)} columns")
        return self.df
    
    def generate_summary_statistics(self) -> Dict:
        """Generate comprehensive summary statistics"""
        logger.info("Generating summary statistics...")
        
        summary = {
            'dataset_overview': {
                'total_records': len(self.df),
                'total_columns': len(self.df.columns),
                'columns': list(self.df.columns),
                'memory_usage_mb': f"{self.df.memory_usage(deep=True).sum() / 1024 / 1024:.2f}"
            },
            'category_distribution': {},
            'price_analysis': {},
            'location_analysis': {},
            'data_quality': {}
        }
        
        # Category distribution
        if 'category' in self.df.columns:
            summary['category_distribution'] = self.df['category'].value_counts().to_dict()
        
        # Price analysis
        if 'price' in self.df.columns:
            price_data = self.df['price'].dropna()
            if len(price_data) > 0:
                summary['price_analysis'] = {
                    'count': int(len(price_data)),
                    'mean': float(price_data.mean()),
                    'median': float(price_data.median()),
                    'std': float(price_data.std()),
                    'min': float(price_data.min()),
                    'max': float(price_data.max()),
                    'q25': float(price_data.quantile(0.25)),
                    'q75': float(price_data.quantile(0.75))
                }
        
        # Location analysis
        if 'city' in self.df.columns:
            summary['location_analysis'] = {
                'unique_cities': int(self.df['city'].nunique()),
                'top_cities': self.df['city'].value_counts().head(10).to_dict()
            }
        
        # Data quality metrics
        summary['data_quality'] = {
            'missing_values': self.df.isnull().sum().to_dict(),
            'completeness_percentage': float((1 - self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100)
        }
        
        self.insights['summary_statistics'] = summary
        
        # Save to JSON
        with open(f'{self.output_dir}/summary_statistics.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info("Summary statistics generated and saved")
        return summary
    
    def analyze_categories(self):
        """Analyze product categories"""
        logger.info("Analyzing product categories...")
        
        if 'category' not in self.df.columns:
            logger.warning("No category column found")
            return
        
        # Category distribution
        plt.figure(figsize=(10, 6))
        category_counts = self.df['category'].value_counts()
        category_counts.plot(kind='bar', color='skyblue')
        plt.title('Product Distribution by Category', fontsize=14, fontweight='bold')
        plt.xlabel('Category')
        plt.ylabel('Number of Products')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/category_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Category-wise price analysis
        if 'price' in self.df.columns:
            plt.figure(figsize=(12, 6))
            self.df.boxplot(column='price', by='category', figsize=(12, 6))
            plt.title('Price Distribution by Category', fontsize=14, fontweight='bold')
            plt.suptitle('')  # Remove default title
            plt.xlabel('Category')
            plt.ylabel('Price (₹)')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig(f'{self.output_dir}/price_by_category.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        logger.info("Category analysis complete")
    
    def analyze_prices(self):
        """Analyze price distributions and patterns"""
        logger.info("Analyzing price data...")
        
        if 'price' not in self.df.columns or self.df['price'].isna().all():
            logger.warning("No valid price data found")
            return
        
        price_data = self.df['price'].dropna()
        
        # Price distribution histogram
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        axes[0].hist(price_data, bins=50, color='lightcoral', edgecolor='black')
        axes[0].set_title('Price Distribution', fontsize=12, fontweight='bold')
        axes[0].set_xlabel('Price (₹)')
        axes[0].set_ylabel('Frequency')
        axes[0].grid(alpha=0.3)
        
        # Log-scale price distribution
        axes[1].hist(price_data, bins=50, color='lightgreen', edgecolor='black')
        axes[1].set_title('Price Distribution (Log Scale)', fontsize=12, fontweight='bold')
        axes[1].set_xlabel('Price (₹)')
        axes[1].set_ylabel('Frequency')
        axes[1].set_yscale('log')
        axes[1].grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/price_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Price category analysis
        if 'price_category' in self.df.columns:
            plt.figure(figsize=(10, 6))
            price_cat_counts = self.df['price_category'].value_counts()
            plt.pie(price_cat_counts.values, labels=price_cat_counts.index, autopct='%1.1f%%', startangle=90)
            plt.title('Products by Price Category', fontsize=14, fontweight='bold')
            plt.axis('equal')
            plt.savefig(f'{self.output_dir}/price_categories.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        logger.info("Price analysis complete")
    
    def analyze_locations(self):
        """Analyze geographical distribution"""
        logger.info("Analyzing location data...")
        
        if 'city' not in self.df.columns:
            logger.warning("No city data found")
            return
        
        # Top cities
        plt.figure(figsize=(12, 6))
        top_cities = self.df['city'].value_counts().head(15)
        top_cities.plot(kind='barh', color='mediumpurple')
        plt.title('Top 15 Cities by Product Listings', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Products')
        plt.ylabel('City')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/top_cities.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Major cities vs others
        if 'is_major_city' in self.df.columns:
            plt.figure(figsize=(8, 8))
            major_city_dist = self.df['is_major_city'].value_counts()
            labels = ['Major Cities', 'Other Cities']
            plt.pie(major_city_dist.values, labels=labels, autopct='%1.1f%%', startangle=90)
            plt.title('Distribution: Major Cities vs Others', fontsize=14, fontweight='bold')
            plt.axis('equal')
            plt.savefig(f'{self.output_dir}/major_cities_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        logger.info("Location analysis complete")
    
    def analyze_suppliers(self):
        """Analyze supplier/company patterns"""
        logger.info("Analyzing supplier data...")
        
        if 'company_name' not in self.df.columns:
            logger.warning("No company data found")
            return
        
        # Top suppliers
        plt.figure(figsize=(12, 6))
        top_suppliers = self.df['company_name'].value_counts().head(15)
        top_suppliers.plot(kind='barh', color='lightseagreen')
        plt.title('Top 15 Suppliers by Product Count', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Products')
        plt.ylabel('Supplier')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/top_suppliers.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Supplier concentration
        total_suppliers = self.df['company_name'].nunique()
        self.insights['supplier_analysis'] = {
            'total_unique_suppliers': int(total_suppliers),
            'avg_products_per_supplier': float(len(self.df) / total_suppliers if total_suppliers > 0 else 0),
            'top_10_suppliers': self.df['company_name'].value_counts().head(10).to_dict()
        }
        
        logger.info("Supplier analysis complete")
    
    def identify_anomalies(self):
        """Identify data anomalies and quality issues"""
        logger.info("Identifying anomalies...")
        
        anomalies = {
            'price_outliers': [],
            'data_quality_issues': {},
            'suspicious_patterns': []
        }
        
        # Price outliers (using IQR method)
        if 'price' in self.df.columns:
            price_data = self.df['price'].dropna()
            if len(price_data) > 0:
                Q1 = price_data.quantile(0.25)
                Q3 = price_data.quantile(0.75)
                IQR = Q3 - Q1
                outliers = self.df[
                    (self.df['price'] < (Q1 - 1.5 * IQR)) | 
                    (self.df['price'] > (Q3 + 1.5 * IQR))
                ]
                anomalies['price_outliers'] = {
                    'count': len(outliers),
                    'percentage': float(len(outliers) / len(self.df) * 100)
                }
        
        # Data quality issues
        anomalies['data_quality_issues'] = {
            'missing_prices': int(self.df['price'].isna().sum()) if 'price' in self.df.columns else 0,
            'missing_locations': int(self.df['location'].isna().sum()) if 'location' in self.df.columns else 0,
            'missing_company': int(self.df['company_name'].isna().sum()) if 'company_name' in self.df.columns else 0
        }
        
        self.insights['anomalies'] = anomalies
        
        with open(f'{self.output_dir}/anomalies.json', 'w') as f:
            json.dump(anomalies, f, indent=2)
        
        logger.info("Anomaly detection complete")
    
    def generate_insights_report(self):
        """Generate comprehensive insights report"""
        logger.info("Generating insights report...")
        
        # Compile key insights
        report = {
            'executive_summary': {
                'total_products': len(self.df),
                'categories_analyzed': int(self.df['category'].nunique()) if 'category' in self.df.columns else 0,
                'unique_suppliers': int(self.df['company_name'].nunique()) if 'company_name' in self.df.columns else 0,
                'unique_locations': int(self.df['city'].nunique()) if 'city' in self.df.columns else 0,
            },
            'key_findings': [],
            'recommendations': []
        }
        
        # Generate key findings
        if 'price' in self.df.columns and self.df['price'].notna().any():
            avg_price = self.df['price'].mean()
            report['key_findings'].append(
                f"Average product price is ₹{avg_price:,.2f}"
            )
        
        if 'category' in self.df.columns:
            top_category = self.df['category'].value_counts().index[0]
            top_category_count = self.df['category'].value_counts().iloc[0]
            report['key_findings'].append(
                f"'{top_category}' is the most listed category with {top_category_count} products"
            )
        
        if 'city' in self.df.columns:
            top_city = self.df['city'].value_counts().index[0]
            report['key_findings'].append(
                f"{top_city} has the highest concentration of suppliers"
            )
        
        # Add recommendations
        report['recommendations'] = [
            "Focus sourcing efforts on top 3 categories for better supplier relationships",
            "Consider geographic diversification to reduce supply chain risks",
            "Investigate price outliers for potential negotiation opportunities",
            "Build partnerships with top suppliers in major cities"
        ]
        
        # Merge all insights
        report.update(self.insights)
        
        # Save report
        with open(f'{self.output_dir}/insights_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        # Generate markdown report
        self._generate_markdown_report(report)
        
        logger.info("Insights report generated")
        return report
    
    def _generate_markdown_report(self, report: Dict):
        """Generate markdown version of the report"""
        md_content = "# IndiaMART Data Analysis Report\n\n"
        md_content += "## Executive Summary\n\n"
        
        for key, value in report.get('executive_summary', {}).items():
            md_content += f"- **{key.replace('_', ' ').title()}**: {value}\n"
        
        md_content += "\n## Key Findings\n\n"
        for finding in report.get('key_findings', []):
            md_content += f"- {finding}\n"
        
        md_content += "\n## Recommendations\n\n"
        for rec in report.get('recommendations', []):
            md_content += f"- {rec}\n"
        
        md_content += "\n## Visualizations\n\n"
        md_content += "Generated visualizations can be found in the `analysis_results/` directory:\n\n"
        md_content += "- Category Distribution\n"
        md_content += "- Price Analysis\n"
        md_content += "- Geographic Distribution\n"
        md_content += "- Supplier Analysis\n"
        
        with open(f'{self.output_dir}/ANALYSIS_REPORT.md', 'w') as f:
            f.write(md_content)
    
    def run_complete_analysis(self):
        """Run complete EDA pipeline"""
        logger.info("\n" + "="*60)
        logger.info("Starting Comprehensive EDA")
        logger.info("="*60 + "\n")
        
        # Load data
        self.load_data()
        
        # Generate analyses
        self.generate_summary_statistics()
        self.analyze_categories()
        self.analyze_prices()
        self.analyze_locations()
        self.analyze_suppliers()
        self.identify_anomalies()
        
        # Generate final report
        report = self.generate_insights_report()
        
        logger.info("\n" + "="*60)
        logger.info("EDA Complete! Results saved to analysis_results/")
        logger.info("="*60 + "\n")
        
        return report


if __name__ == "__main__":
    # Example usage
    eda = MarketplaceEDA('data/processed_data.csv')
    eda.run_complete_analysis()
