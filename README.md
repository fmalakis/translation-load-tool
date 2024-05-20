# **JSON/CSV Load Utilities**

This repository includes tools that were made to facilitate faster changes in application translations, localization
and configuration. It includes two scripts: 'translation_load.py' which takes an Excel file as input and performs changes
to a target JSON or CSV file and 'specialties_load.py' which takes an Excel file as input and applies changes to a
specific part of the target JSON file.

# **Pre-requisites and dependencies**

- Python 3.11
- Pandas
- openpyxl
- Make sure Python is added to your path variables

# **Expected file format**

- **For 'translation_load.py':**
  - A .xlsx file with 2 columns: _translation keys_ and _translation values_
  - A .json or .csv file which will be modified by the script based on the key and value columns
- **For 'specialties_load.py':**
  - A .xlsx file with a single column containing all the new values you wish to add to the target JSON file
  - A .json file in which the values of the .xlsx will be inserted

<img width="293" alt="image" src="https://github.com/fmalakis/translation-load-tool/assets/61471928/17cf7cba-c3d8-4122-9d17-155b156d5ca7">



# **How to run**

Install all the required dependencies as outlined above and save the script(s) to a location of your choosing. Make sure
that the format of the .xlsx file is exactly as underlined above, depending on which script you choose to use.

## Running 'translation_load.py'
To run this script, navigate to the dir it is saved in and run:
```commandline
python translation_load.py "<path/to/your/excel.xlsx>" "<path/to/your/json_file.json>"
```
**Make sure that the path files are wrapped in quotes!**

The script will then check if these two files exist and will initiate the replacement procedure.
By default, the script will check and see if, for a given xlsx key, the same key exists inside the JSON and if it does,
it will replace the JSON value for that key with the value for the same key in the xlsx, otherwise, it will append it as
a new key-value pair.

Once the script is finished, a detailed log file (_log.txt_) will be generated in the same directory as the script, which
will contain all the changes made during a run. The script will re-use this file if it already exists, appending
multiple runs to it.

## Running 'specialties_load.py'

To run this script, navigate to the dir it is saved in and run:
```commandline
python specialties_load.py [-a] [-c] "<path/to/your/excel.xlsx>" "<path/to/your/json_file.json>" <section_names>
```

```
positional arguments:
  excel_path    Path to the Excel file containing the specialties
  json_path     Path to the JSON config file
  section_name  One or more section names to update, separated by commas

options:
  -h, --help    show this help message and exit
  -a            Update customAccountFilters
  -c            Update customContactFilters
```

By default, the script will insert the new values at the specified points and will also sort the array before writing it
back to the JSON file. The script will also generate a detailed log file (_log.txt_) which will contain all the changes
made during a run. The script will re-use this file, if it already exists, appending multiple runs to it.