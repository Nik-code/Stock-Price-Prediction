from bs4 import BeautifulSoup
import csv

def parse_html_to_csv(html_file_path, output_csv_path):
    """
    Parses an HTML file containing a table and writes the table data to a CSV file.

    Args:
        html_file_path (str): The file path to the input HTML file.
        output_csv_path (str): The file path to the output CSV file.
    """
    # Open the HTML file and parse it with BeautifulSoup
    with open(html_file_path, 'r', encoding='utf-8') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')

    # Find the first table in the HTML document
    table = soup.find('table')

    # Get the table headers
    headers = [th.text.strip() for th in table.find('tr').find_all('th')]

    # Get the table rows
    rows = [
        [td.text.strip() for td in tr.find_all('td')]
        for tr in table.find_all('tr')[1:]
    ]

    # Write the data to a CSV file
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        writer.writerows(rows)

def main():
    """
    Main function to convert HTML table data to CSV.
    """
    html_file_path = 'company_list.html'  # Replace with your HTML file path
    output_csv_path = 'company_list.csv'  # Replace with your desired CSV file path

    parse_html_to_csv(html_file_path, output_csv_path)
    print(f"Data successfully written to {output_csv_path}")

if __name__ == "__main__":
    main()