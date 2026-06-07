import csv
import requests

# 1. Define the Open Data URL from Kaohsiung City Government
url = "https://data.kcg.gov.tw/File/DirectDownload/80bbbbd3-9ee4-4244-98e9-b4c08deda91b"

print("==== Read Result ====")
print(f"URL: {url}")

try:
    # 2. Send a request to fetch the online data
    response = requests.get(url)
    response.raise_for_status() 

    # Get data type and content length
    content_type = response.headers.get("Content-Type", "text/csv")
    content_length = len(response.content)

    print(f"Content-Type: {content_type}")
    print(f"Data Length: {content_length} bytes")
    print("=======================")
    print()

    # 3. Read and decode the CSV data
    decoded_content = response.content.decode("utf-8")
    csv_reader = csv.reader(decoded_content.splitlines())
    rows = list(csv_reader)

    if len(rows) > 0:
        header = rows[0]  # The first row contains the column headers
        data_rows = rows[1:]  # The rest are data rows

        total_rows = len(data_rows)
        total_columns = len(header)

        print(f"Total Rows: {total_rows}, Total Columns: {total_columns}")

        # 4. Check and print the 1st record
        if total_rows > 0:
            print("==== 1st Record ====")
            first_row = data_rows[0]

            # Loop through columns and print as "Column_Name : Value"
            for col_name, value in zip(header, first_row):
                if col_name == "Description" and not value:
                    value = "None"
                print(f"{col_name} : {value}")
        else:
            print("No data found in the CSV file.")
    else:
        print("The CSV file is empty.")

except Exception as e:
    print(f"An error occurred while fetching or reading data: {e}")