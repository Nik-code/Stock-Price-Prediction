import pandas as pd
import mysql.connector
import requests

def csv_to_mysql(csv_file_path, db_config, table_name):
    """
    Inserts data from a CSV file into a MySQL table.

    Args:
        csv_file_path (str): The file path to the CSV file.
        db_config (dict): A dictionary containing database configuration.
        table_name (str): The name of the table to insert data into.
    """
    # Connect to the MySQL database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Read data from the CSV file
    data = pd.read_csv(csv_file_path)

    # Insert data into the table
    for i, row in data.iterrows():
        columns = ', '.join(row.index)
        placeholders = ', '.join(['%s'] * len(row))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(row))

    # Commit the transaction and close the connection
    connection.commit()
    cursor.close()
    connection.close()

def delete_table(table_name, db_config):
    """
    Deletes a specified table from the MySQL database.

    Args:
        table_name (str): The name of the table to delete.
        db_config (dict): A dictionary containing database configuration.
    """
    # Connect to the MySQL database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Drop the table if it exists
    sql = f"DROP TABLE IF EXISTS {table_name}"
    cursor.execute(sql)

    # Commit the transaction and close the connection
    connection.commit()
    cursor.close()
    connection.close()

def update_data(api_endpoint, db_config, table_name):
    """
    Fetches data from an API and inserts it into a MySQL table.

    Args:
        api_endpoint (str): The API endpoint to fetch data from.
        db_config (dict): A dictionary containing database configuration.
        table_name (str): The name of the table to insert data into.
    """
    # Fetch data from the API
    response = requests.get(api_endpoint)
    data = response.json()

    # Connect to the MySQL database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Insert data into the table
    for item in data:
        columns = ', '.join(item.keys())
        placeholders = ', '.join(['%s'] * len(item))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(item.values()))

    # Commit the transaction and close the connection
    connection.commit()
    cursor.close()
    connection.close()

def main():
    """
    Main function to demonstrate the usage of the other functions.
    """
    # Define database configuration
    db_config = {
        'user': 'your_username',
        'password': 'your_password',
        'host': 'your_host',
        'database': 'your_database'
    }

    # Example usage of the functions
    csv_file_path = 'path_to_your_csv_file'
    table_name = 'your_table_name'
    api_endpoint = 'your_api_endpoint'

    # Insert CSV data into the MySQL table
    csv_to_mysql(csv_file_path, db_config, table_name)

    # Delete the specified table from the MySQL database
    delete_table(table_name, db_config)

    # Fetch data from the API and insert it into the MySQL table
    update_data(api_endpoint, db_config, table_name)

if __name__ == "__main__":
    main()
