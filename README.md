# **Translation Load Tool**

This tool was made to facilitate faster changes in application translations and localization.
It receives a path to an Excel and a path to a JSON or CSV file and applies the values of the Excel file to the JSON for the
matching keys, if they exist. It also includes logging functionally.

# **Pre-requisites and dependencies**

- Python 3.11
- Pandas
- openpyxl
- Make sure Python is added to your path variables

# **Expected file format**

- A .xlsx file with 2 columns: _translation keys_ and _translation values_
- A .json or .csv file which will be modified by the script based on the key and value columns

<img width="293" alt="image" src="https://github.com/fmalakis/translation-load-tool/assets/61471928/17cf7cba-c3d8-4122-9d17-155b156d5ca7">



# **How to run**

Install all the required dependencies as outlined above and save the script to a location of your choosing. Make sure
that the format of the .xlsx file is exactly as underlined above.

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