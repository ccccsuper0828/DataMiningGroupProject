import pandas as pd
import numpy as np
from ydata_profiling import ProfileReport
import os
import csv

def load_dataset(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset file not found: {file_path}")
    
    df = pd.read_csv(file_path, quoting=csv.QUOTE_NONE)
    print(f"Dataset loaded successfully. Shape: {df.shape}")
    return df

def check_data_quality(df):

    quality_report = {}
    
    # 1. Missing values
    missing_counts = df.isnull().sum()
    missing_percentage = (missing_counts / len(df)) * 100
    quality_report['missing_values'] = pd.DataFrame({
        'Column': missing_counts.index,
        'Missing Count': missing_counts.values,
        'Missing Percentage': missing_percentage.values
    })
    print("\n=== MISSING VALUES ===")
    print(quality_report['missing_values'])
    
    # 2. Duplicates
    duplicates_count = df.duplicated().sum()
    quality_report['duplicates_count'] = duplicates_count
    print(f"\nDuplicates count: {duplicates_count}")
    
    # 3. Data types
    quality_report['data_types'] = df.dtypes
    print("\n=== DATA TYPES ===")
    print(quality_report['data_types'])
    
    # 4. Basic statistics for numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    if len(numerical_cols) > 0:
        quality_report['numerical_stats'] = df[numerical_cols].describe()
        print("\n=== NUMERICAL STATISTICS ===")
        print(quality_report['numerical_stats'])
    
    # 5. Unique values for categorical columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        unique_counts = {col: df[col].nunique() for col in categorical_cols}
        quality_report['categorical_unique'] = unique_counts
        print("\n=== CATEGORICAL UNIQUE COUNTS ===")
        for col, count in unique_counts.items():
            print(f"{col}: {count}")
    
    # 6. Outliers detection 
    outliers_report = {}
    for col in numerical_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
        outliers_report[col] = {
            'outlier_count': len(outliers),
            'percentage': (len(outliers) / len(df)) * 100
        }
    quality_report['outliers'] = outliers_report
    print("\n=== OUTLIERS (IQR Method) ===")
    for col, info in outliers_report.items():
        print(f"{col}: {info['outlier_count']} ({info['percentage']:.2f}%)")
    
    return quality_report

def generate_profile_report(df, output_file="dataset_profile_report.html"):
  
    profile = ProfileReport(df, title="Dataset Profiling Report")
    profile.to_file(output_file)
    print(f"\nProfiling report generated: {output_file}")
    return output_file

def main(file_path):
    df = load_dataset(file_path)
    quality_report = check_data_quality(df)
    report_path = generate_profile_report(df)
    
    print(f"\nPipeline completed. Quality checks printed above, full report at: {report_path}")

# Example usage
if __name__ == "__main__":
    # Replace 'your_dataset.csv' with the actual path to your CSV file
    dataset_file = '/Users/c0w0ilf/LingnanProject/datamining/dataMiningGroupProject/merged_mayo_dic_2021.csv'
    main(dataset_file)