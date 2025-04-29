from tabula import read_pdf
import os

URL = "https://assets.accessible-digital-documents.com/uploads/2017/01/sample-tables.pdf"

tabular_data = read_pdf(URL, pages="all", multiple_tables=True)

# Create directories if they don't exist
os.makedirs("csv_files", exist_ok=True)
os.makedirs("excel_files", exist_ok=True)
os.makedirs("json_files", exist_ok=True)

# Print the tables
for i, table in enumerate(tabular_data):
    print(f"Table {i + 1}:")
    print(table)
    print("\n")

# Save the tables to CSV files
for i, table in enumerate(tabular_data):
    file_path = f"csv_files/table_{i + 1}.csv"
    table.to_csv(file_path, index=False)
    print(f"Table {i + 1} saved as {file_path}")

# Save the tables to Excel files
for i, table in enumerate(tabular_data):
    file_path = f"excel_files/table_{i + 1}.xlsx"
    table.to_excel(file_path, index=False)
    print(f"Table {i + 1} saved as {file_path}")

# Save the tables to JSON files
for i, table in enumerate(tabular_data):
    file_path = f"json_files/table_{i + 1}.json"
    table.to_json(file_path, orient="records")
    print(f"Table {i + 1} saved as {file_path}")