import os.path
from datetime import datetime
import pandas as pd
import json
import argparse

ALLOWED_SECTIONS = ['Primary Specialty', 'Account Subtype', 'Specialty 1']


def read_excel(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f'Could not find Excel file at specific directory: "{file_path}". '
                                f'File either does not exist or is in another location. \nClosing...')

    df = pd.read_excel(file_path)
    return df.iloc[:, 0].tolist()  # Assuming the specialties are in the first column


def update_values(json_data, filter_type, section_name, specialties, log_file):
    # Locate the correct section to update
    filters_section = None
    if isinstance(json_data, dict):
        filters_section = json_data.get(filter_type)
    elif isinstance(json_data, list):
        for item in json_data:
            if isinstance(item, dict) and filter_type in item:
                filters_section = item[filter_type]
                break

    if not filters_section:
        raise ValueError(f"{filter_type} not found in JSON data.")

    for section in filters_section:
        if section["name"] == section_name:
            current_values = {item["value"] for item in section["values"]}
            for specialty in specialties:
                if specialty not in current_values:
                    section["values"].append({"text": specialty, "value": specialty})
                    log_file.write(f"Added key '{specialty}' in {section_name} for {filter_type}\n")
            section["values"].sort(key=lambda x: x["text"])
    return json_data


def main(excel_path, json_path, update_account_filters, update_contact_filters, section_name):
    # Read doctor specialties from Excel file
    specialties = read_excel(excel_path)

    if not os.path.exists(json_path):
        raise FileNotFoundError(f'Could not find JSON file at specific directory: "{json_path}". '
                                f'File either does not exist or is in another location. \nClosing...')

    # Read JSON data
    with open(json_path, 'r') as f:
        json_data = json.load(f)

    # Open log file for writing
    with open("log.txt", "a", encoding='utf-8') as log_file:
        log_file.write(f"\nUpdate Log - {datetime.now()}\n")
        log_file.write(f"Excel File: {excel_path}\n")
        log_file.write(f"JSON Config File: {json_path}\n")

        for section in section_name.split(','):

            section = section.strip()

            if section not in ALLOWED_SECTIONS:
                print(f'Warning: {section} is not an allowed section name. Skipping...')
                continue

            # Update customAccountFilters if specified
            if update_account_filters:
                json_data = update_values(json_data, "customAccountFilters", section, specialties, log_file)

            # Update customContactFilters if specified
            if update_contact_filters:
                json_data = update_values(json_data, "customContactFilters", section, specialties, log_file)

    # Write updated JSON data back to file
    with open(json_path, 'w') as f:
        json.dump(json_data, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update a JSON config file with specialties from an Excel file")
    parser.add_argument("excel_path", type=str, help="Path to the Excel file containing the specialties")
    parser.add_argument("json_path", type=str, help="Path to the JSON config file")
    parser.add_argument("-a", action="store_true", help="Update customAccountFilters")
    parser.add_argument("-c", action="store_true", help="Update customContactFilters")
    parser.add_argument("section_name", type=str, help="One or more section names to update, separated by commas")

    args = parser.parse_args()
    main(args.excel_path, args.json_path, args.a, args.c, args.section_name)
