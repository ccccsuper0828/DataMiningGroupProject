import pandas as pd
import s3fs
import boto3
import csv
import sys

# Set CSV field size limit to maximum to handle large fields
csv.field_size_limit(sys.maxsize)

# Hardcoded credentials
aws_access_key_id = ''
aws_secret_access_key = ''

# S3 paths with encoded spaces
s3_url_1 = 's3://ieee-dataport/open/54588/1mayo - agosto 2021.csv'
s3_url_2 = 's3://ieee-dataport/open/54588/2agosto -dic 2021.csv'

try:
    # Configure boto3
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    # Create s3fs filesystem
    s3_filesystem = s3fs.S3FileSystem(
        key=aws_access_key_id,
        secret=aws_secret_access_key,
    )

    # Verify files exist
    if not s3_filesystem.exists(s3_url_1):
        raise FileNotFoundError(f"S3 path does not exist: {s3_url_1}")
    if not s3_filesystem.exists(s3_url_2):
        raise FileNotFoundError(f"S3 path does not exist: {s3_url_2}")

    # Read both CSV files
    print("Reading first CSV (1mayo - agosto 2021)...")
    with s3_filesystem.open(s3_url_1, 'rb') as f:
        df1 = pd.read_csv(f, engine='python', encoding='utf-8', on_bad_lines='skip')

    print("Reading second CSV (2agosto - dic 2021)...")
    with s3_filesystem.open(s3_url_2, 'rb') as f:
        df2 = pd.read_csv(f, engine='python', encoding='utf-8', on_bad_lines='skip')

    # Verify column consistency
    print("Columns in first dataset:", df1.columns.tolist())
    print("Columns in second dataset:", df2.columns.tolist())

    # Merge datasets
    print("Merging datasets...")
    df_merged = pd.concat([df1, df2], ignore_index=True)

    # Display merged dataset preview
    print("Merged dataset preview:")
    print(df_merged.head())

    # Select and convert datetime columns
    if 'fecha_servidor' in df_merged.columns and 'fecha_esp32' in df_merged.columns:
        date_columns_df = df_merged[['fecha_servidor', 'fecha_esp32']].copy()
        date_columns_df['fecha_servidor'] = pd.to_datetime(date_columns_df['fecha_servidor'], errors='coerce')
        date_columns_df['fecha_esp32'] = pd.to_datetime(date_columns_df['fecha_esp32'], errors='coerce')
        print("Datetime columns:")
        print(date_columns_df.head())
    else:
        print("Columns 'fecha_servidor' or 'fecha_esp32' not found")

    # Save merged dataset to local file
    local_file = 'merged_mayo_dic_2021.csv'
    print(f"Saving merged dataset to {local_file}...")
    df_merged.to_csv(local_file, index=False)
    print(f"Dataset successfully saved to {local_file}")

except Exception as e:
    print(f"An error occurred while processing: {e}")
    # Debug: Preview raw content of problematic file
    try:
        with s3_filesystem.open(s3_url_2, 'r', encoding='utf-8', errors='ignore') as f:
            preview = f.read(1000)
            print("Preview of 2agosto - dic 2021.csv (first 1000 characters):")
            print(preview)
            f.seek(0)
            lines = f.readlines(3200000)
            print("Preview near row 3,178,052:")
            print(lines[3178050:3178055])
    except Exception as preview_error:
        print(f"Error previewing file: {preview_error}")