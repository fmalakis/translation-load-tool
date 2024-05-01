import pandas as pd
import json
import os
import argparse
from datetime import datetime


def update_json(excel_path, json_path):

    if not os.path.exists(excel_path):
        print(f'Requested Excel file could not be found at the specified directory: "{excel_path}"\nClosing...')
        exit()

    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_path)

    # Load the existing JSON data (create an empty dictionary if the file doesn't exist)
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
    else:
        print(f'Requested JSON file could not be found at the specified directory: "{json_path}"\nClosing...')
        exit()

    # Default log file name, generated in the same directory as the JSON file
    log_path = os.path.join(os.path.dirname(json_path), 'log.txt')

    with open(log_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"\nUpdate Log - {datetime.now()}\n")
        log_file.write(f"Excel File: {excel_path}\n")
        log_file.write(f"JSON File: {json_path}\n")

        # Counter for changed records
        records_changed = 0

        # Update JSON data with key-value pairs from the Excel file
        for index, row in df.iterrows():
            key = row['translation key']
            value = row['translation value']

            # Log changes if the value is updated
            if json_data.get(key) != value:
                old_value = json_data.get(key, 'N/A')
                json_data[key] = value
                log_file.write(f"Updated key '{key}': '{old_value}' -> '{value}'\n")
                records_changed += 1

        # Save the updated JSON data back to the file
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)

        # Log the total records changed
        log_file.write(f"Total Records Changed: {records_changed}\n")

    print(f"Updated {json_path} with data from {excel_path}")
    print(f"Log written to {log_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update JSON file with data from an Excel file.')
    parser.add_argument('excel_path', type=str, help='Path to the Excel file.')
    parser.add_argument('json_path', type=str, help='Path to the JSON file.')

    args = parser.parse_args()

    # Call the function to update the JSON file
    update_json(args.excel_path, args.json_path)
