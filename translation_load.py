import pandas as pd
import json
import os
import argparse
from datetime import datetime


def update_json(excel_path, json_path, script_path, is_verbose, is_logging):

    if not os.path.exists(excel_path):
        raise FileNotFoundError(f'Requested Excel file could not be found at the specified directory: "{excel_path}'
                                f'"\nClosing...')

    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_path)

    # Load the existing JSON data
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
    else:
        raise FileNotFoundError(f'Requested JSON file could not be found at the specified directory: "{json_path}"'
                                f'\nClosing...')

    # Default log file name, generated in the same directory as the JSON file
    log_path = os.path.join(script_path, 'log.txt')

    with open(log_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"\nUpdate Log - {datetime.now()}\n")
        log_file.write(f"Excel File: {excel_path}\n")
        log_file.write(f"JSON File: {json_path}\n")

        if is_verbose:
            print(f"Excel File: {excel_path}")
            print(f"JSON File: {json_path}")

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
                if is_verbose:
                    print(f"Updated key '{key}': '{old_value}' -> '{value}'")
                records_changed += 1

        # Save the updated JSON data back to the file
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)

        # Log the total records changed
        log_file.write(f"Total Records Changed: {records_changed}\n")
        if is_verbose:
            print(f"Total Records Changed: {records_changed}")

    print(f"Updated {json_path} with data from {excel_path}")
    print(f"Log written to {log_path}")


def update_csv(excel_path, translation_path, script_path, is_verbose, is_logging):

    if not os.path.exists(excel_path):
        raise FileNotFoundError(f'Requested Excel file could not be found at the specified directory: "{excel_path}"'
                                f'\nClosing...')

    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_path)

    # Ensure expected columns are present
    expected_columns = ['translation key', 'translation value']
    if not set(expected_columns).issubset(df.columns):
        raise KeyError(f"Expected columns: {expected_columns}. Found columns: {df.columns.tolist()}")

    if os.path.exists(translation_path):
        existing_df = pd.read_csv(translation_path, header=None, names=expected_columns)
    else:
        raise FileNotFoundError(f'Requested CSV file could not be found at the specified directory: "{translation_path}"'
                                f'\nClosing...')

        # Log file name
    log_path = os.path.join(script_path, 'log.txt')

    # Open or create the log file to track changes
    with open(log_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"\nUpdate Log - {datetime.now()}\n")
        log_file.write(f"Excel File: {excel_path}\n")
        log_file.write(f"Translation File: {translation_path}\n")

        # Counter for changed records
        records_changed = 0

        # Update CSV data with key-value pairs from the Excel file
        for _, row in df.iterrows():
            key = row['translation key']
            value = row['translation value']

            # Find the row with the same key
            key_rows = existing_df[existing_df['translation key'] == key]

            if not key_rows.empty:
                # Update existing key
                old_value = key_rows.iloc[0]['translation value']

                if old_value != value:
                    existing_df.loc[key_rows.index, 'translation value'] = value
                    log_file.write(f"Updated key '{key}': '{old_value}' -> '{value}'\n")
                    if is_logging:
                        print(f"Updated key '{key}': '{old_value}' -> '{value}'")
                    records_changed += 1
            else:
                # If key doesn't exist, add it
                new_row = pd.DataFrame([{'translation key': key, 'translation value': value}])
                existing_df = pd.concat([existing_df, new_row], ignore_index=True)
                log_file.write(f"Added key '{key}': '{value}'\n")
                if is_verbose:
                    print(f"Added key '{key}': '{value}'")
                records_changed += 1

        # Save the updated CSV data back to the file
        existing_df.to_csv(translation_path, index=False, header=False)

        # Log the total records changed
        log_file.write(f"Total Records Changed: {records_changed}\n")
        if is_verbose:
            print(f"Total Records Changed: {records_changed}")

    print(f"Updated {translation_path} with data from {excel_path}")
    print(f"Log written to {log_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update a JSON/CSV file with data from an Excel file.')
    parser.add_argument('excel_path', type=str, help='Path to the Excel file.')
    parser.add_argument('translation_path', type=str, help='Path to the JSON or CSV file.')
    parser.add_argument('-v', action='store_true', help='Verbose execution of script actions')
    parser.add_argument('-l', action='store_true', help='Log changes to a log file')

    args = parser.parse_args()

    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.realpath(__file__))

    file_ext = os.path.splitext(args.translation_path)[1].lower()

    if file_ext == ".json":
        # Call the function to update the JSON file
        update_json(args.excel_path, args.translation_path, script_dir, args.v, args.l)
    elif file_ext == ".csv":
        # Call the function to update the CSV file
        update_csv(args.excel_path, args.translation_path, script_dir, args.v, args.l)
    else:
        raise NotImplementedError("Only JSON and CSV files are supported as valid translation file extensions.")
