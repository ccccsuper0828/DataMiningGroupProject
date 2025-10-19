import pandas as pd
import sys
import os

# Redirect print output to a file
output_file = 'missing_dates_report.txt'
original_stdout = sys.stdout  # Save original stdout

# Checking missing dates
def check_missing_dates(df, column):
    """
    Check for missing values and time gaps in the specified datetime column.
    Returns: NaN/NaT count, list of gaps (start, end, missing seconds).
    """
    df[column] = pd.to_datetime(df[column], errors='coerce')
    nan_count = df[column].isna().sum()
    print(f"Column '{column}' has {nan_count} NaN/NaT missing values.")
    
    df_sorted = df.dropna(subset=[column]).sort_values(by=column).reset_index(drop=True)
    
    gaps = []
    for i in range(1, len(df_sorted)):
        diff = (df_sorted.loc[i, column] - df_sorted.loc[i-1, column]).total_seconds()
        if diff > 1:
            start = df_sorted.loc[i-1, column]
            end = df_sorted.loc[i, column]
            missing_seconds = int(diff - 1)
            gaps.append((start, end, missing_seconds))
    
    if gaps:
        print(f"Column '{column}' has {len(gaps)} time gaps:")
        for start, end, missing in gaps:
            print(f"  From {start} to {end} missing {missing} seconds.")
    else:
        print(f"Column '{column}' time series is continuous, no gaps.")
    
    return nan_count, gaps

# Main function
if __name__ == "__main__":
    # File path
    file_path = '/Users/c0w0ilf/LingnanProject/datamining/dataMiningGroupProject/merged_mayo_dic_2021.csv'
    
    # Open file to redirect print output
    with open(output_file, 'w', encoding='utf-8') as f:
        sys.stdout = f  # Redirect print to file
        
        # Reading CSV
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            print("Dataset loaded successfully.")
            print(f"Total rows: {len(df)}")
            print("First few rows:")
            print(df.head())
        except Exception as e:
            print(f"Error reading CSV: {e}")
            sys.stdout = original_stdout  # Restore stdout
            sys.exit(1)
        
        # Checking required columns
        required_columns = ['fecha_servidor', 'fecha_esp32']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            print(f"Missing columns: {missing_cols}")
            sys.stdout = original_stdout  # Restore stdout
            sys.exit(1)
        
        # Checking missing dates
        print("\nChecking 'fecha_servidor' column...")
        nan1, gaps1 = check_missing_dates(df.copy(), 'fecha_servidor')
        
        print("\nChecking 'fecha_esp32' column...")
        nan2, gaps2 = check_missing_dates(df.copy(), 'fecha_esp32')
        
        # Summary
        print("\nSummary:")
        print(f"Total NaN/NaT missing: fecha_servidor={nan1}, fecha_esp32={nan2}")
        print(f"Total time gaps: fecha_servidor={len(gaps1)}, fecha_esp32={len(gaps2)}")
        
        sys.stdout = original_stdout  # Restore stdout
    
    print(f"Report saved to {output_file}")