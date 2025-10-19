import pandas as pd
import sys
import os
import math

def split_csv(file_path, num_parts=10, output_dir=None):
    """
    Split a large CSV file into num_parts smaller CSV files, preserving order and headers.
    :param file_path: Path to the input CSV file.
    :param num_parts: Number of parts to split into (default: 10).
    :param output_dir: Directory to save output files (default: same as input file).
    """
    # Set output directory to input file's directory if not specified
    if output_dir is None:
        output_dir = os.path.dirname(file_path)
    
    try:
        # Get total number of rows (excluding header)
        print("Counting total rows...")
        total_rows = sum(1 for _ in open(file_path, encoding='utf-8')) - 1  # Subtract header
        print(f"Total rows (excluding header): {total_rows}")
        
        # Calculate rows per part (ceiling to ensure all rows are included)
        rows_per_part = math.ceil(total_rows / num_parts)
        print(f"Rows per part: {rows_per_part}")
        
        # Read header
        df_header = pd.read_csv(file_path, encoding='utf-8', nrows=0)
        header = df_header.columns.tolist()
        print(f"Header: {header}")
        
        # Read and split CSV in chunks
        chunk_size = 10000  # Adjust based on memory constraints
        current_part = 1
        current_rows = 0
        part_data = []
        
        # Use iterator to read chunks
        reader = pd.read_csv(file_path, encoding='utf-8', chunksize=chunk_size)
        
        for chunk in reader:
            part_data.append(chunk)
            current_rows += len(chunk)
            
            # If enough rows for a part, save it
            while current_rows >= rows_per_part and current_part <= num_parts:
                # Concatenate collected chunks for the current part
                df_part = pd.concat(part_data, ignore_index=True)
                
                # Take the first rows_per_part rows
                df_save = df_part.iloc[:rows_per_part]
                
                # Save to CSV
                output_file = os.path.join(output_dir, f"part_{current_part}.csv")
                df_save.to_csv(output_file, index=False, encoding='utf-8')
                print(f"Saved {output_file} with {len(df_save)} rows")
                
                # Remove saved rows from part_data
                df_part = df_part.iloc[rows_per_part:]
                current_rows -= rows_per_part
                part_data = [df_part] if not df_part.empty else []
                current_part += 1
        
        # Save any remaining rows as the last part
        if current_rows > 0 and current_part <= num_parts:
            df_part = pd.concat(part_data, ignore_index=True)
            output_file = os.path.join(output_dir, f"part_{current_part}.csv")
            df_part.to_csv(output_file, index=False, encoding='utf-8')
            print(f"Saved {output_file} with {len(df_part)} rows")
        
        print(f"Split completed: {current_part - 1} parts created")

    except Exception as e:
        print(f"Error processing CSV: {e}")
        sys.exit(1)

# Main function
if __name__ == "__main__":
    # Input file path
    file_path = '/Users/c0w0ilf/LingnanProject/datamining/dataMiningGroupProject/merged_mayo_dic_2021.csv'
    
    # Verify file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)
    
    # Split the CSV
    split_csv(file_path, num_parts=10)
