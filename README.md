# ETL Project: Heights and Weights
_Instructions and dataset taken from IBM's [Python Project for Data Engineering](https://www.coursera.org/learn/python-project-for-data-engineering) from Coursera_

# Links
|     Item       |   Link   |
| -------------- | ---------|
|Course Link | [IBM: Python Project for Data Engineering (Coursera)](https://www.coursera.org/learn/python-project-for-data-engineering) |
| Dataset (multiple formats) | https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0221EN-SkillsNetwork/labs/module%206/Lab%20-%20Extract%20Transform%20Load/data/source.zip |
| Author's Course Completion Certificate|[Certificate](https://www.coursera.org/account/accomplishments/verify/TFH7N05KO7D3) |

# Prerequisite Steps
## 1.  Gather the data files
```
wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0221EN-SkillsNetwork/labs/module%206/Lab%20-%20Extract%20Transform%20Load/data/source.zip
```

## 2. Unzip the downloaded file into a directory named `source`
```
unzip source.zip -d source
```

## 3. Import required libraries

# Project Tasks

## 1. Extraction
Develop functions to extract from different file formats:
- `extract_from_csv()`
- `extract_from_json()`
- `extract_from_xml()`

## 2. Transformation
Ensure all values taken from different sources are in the same units:
- Heights must be in meters (m)
- Weights must be in kilograms (kg)

## 3. Loading
Store the extracted and transformed data into a single CSV file

## 4. Logging
Create a `log_progress()` function that writes the following to a log file:
- event details
- current date and time at time of event

# How to execute:
_(Tested in Python 3.13)_
```
python etl_code.py
```

# Acknowledgements
## Course Instructors
- Ramesh Sannareddy
- Joseph Santarcangelo
- Abhishek Gagneja
## Course Offered By
* [IBM Skills Network](https://www.coursera.org/partners/ibm-skills-network)
