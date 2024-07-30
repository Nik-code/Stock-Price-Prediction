import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# File paths
input_file_path = "names.csv"  # Replace with the actual input file path
output_file_path = "data.csv"  # Replace with the desired output file path

# Read input data
data = pd.read_csv(input_file_path, sep=",")

def fetch_stock_data(security_code):
    """
    Fetch stock data for a given security code from Yahoo Finance.

    Args:
        security_code (str): The security code for which to fetch stock data.

    Returns:
        pd.DataFrame: The stock data as a pandas DataFrame, or None if fetching fails.
    """
    security_code = security_code + ".BO"
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365 * 10)

    try:
        stock_data = yf.download(security_code, start=start_date, end=end_date)
        return stock_data
    except Exception as e:
        logging.error(f"Failed to fetch data for {security_code}: {e}")
        return None

def main():
    """
    Main function to process stock data and save it to a CSV file.
    """
    all_stock_data = []

    for index, row in data.iterrows():
        security_code = str(row['Security Code'])
        stock_data = fetch_stock_data(security_code)

        if stock_data is not None:
            stock_data['Security Code'] = security_code  # Add a "Security Code" column
            all_stock_data.append(stock_data)
        else:
            logging.warning(f"No data available for {security_code}. Skipping...")

        # Print progress
        logging.info(f"Processed {index + 1} out of {len(data)} rows")

    # Concatenate all stock data into a single DataFrame
    final_stock_data = pd.concat(all_stock_data)

    # Convert 'Security Code' to string for proper matching
    final_stock_data['Security Code'] = final_stock_data['Security Code'].astype(str)
    data['Security Code'] = data['Security Code'].astype(str)

    # Merge with the names data using 'Security Code' as the key
    merged_data = final_stock_data.merge(data, on='Security Code', how='left')

    # Save the final stock data to a new CSV file
    merged_data.to_csv(output_file_path, index=False)
    logging.info(f"Final stock data saved to {output_file_path}")
    logging.info(merged_data.head())

if __name__ == "__main__":
    main()
