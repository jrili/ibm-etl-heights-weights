import glob 
import pandas as pd 
import xml.etree.ElementTree as ET 
from datetime import datetime 

LOG_FILE = "log_file.txt"
TARGET_OUTPUT_FILE = "transformed_data.csv"

############ Logging Methods ############
def log(msg):
    timestamp_format = "%Y-%h-%d-%H:%M:%S"
    now = datetime.now()
    timestamp_str = now.strftime(timestamp_format)

    with open(LOG_FILE, "a") as f:
        log_str = timestamp_str + "," + msg + "\n"
        f.write(log_str)


############ Extract Methods ############

def extract_from_csv(file_to_process):
    log(f"In extract_from_csv(): Extracting from file '{file_to_process}'")
    dataframe = pd.read_csv(file_to_process)
    return dataframe

def extract_from_json(file_to_process):
    log(f"In extract_from_json(): Extracting from file '{file_to_process}'")
    dataframe = pd.read_json(file_to_process, lines=True)
    return dataframe

def extract_from_xml(file_to_process):
    log(f"In extract_from_xml(): Extracting from file '{file_to_process}'")
    rows_list = []
    tree = ET.parse(file_to_process)
    root = tree.getroot()
    for person in root:
        name = person.find("name").text
        height = float(person.find("height").text)
        weight = float(person.find("weight").text)

        rows_list.append([{"name":name, "height":height, "weight":weight}])

    return pd.DataFrame(rows_list)

def extract():
    log("In extract(): started")
    # Initialize list of extracted dataframes
    # to be populated as the script goes through the dataset files
    extracted_dfs_list = []

    # Process all CSV files
    log("In extract(): start processing CSV files")
    for csvfile in glob.glob("source/*.csv"):
        extracted_dfs_list.append(extract_from_csv(csvfile))
    log("In extract(): done processing CSV files")

    # Process all JSON files
    log("In extract(): start processing JSON files")
    for jsonfile in glob.glob("source/*.json"):
        extracted_dfs_list.append(extract_from_json(jsonfile))
    log("In extract(): done processing JSON files")

    # Process all XML files
    log("In extract(): start processing XML files")
    for xmlfile in glob.glob("source/*.xml"):
        extracted_dfs_list.append(extract_from_xml(xmlfile))
    log("In extract(): done processing XML files")

    # Concatenate all dataframes in the extracted_dfs_list
    # into a single DataFrame
    extracted_data = pd.concat(extracted_dfs_list)

    log("In extract(): ended")
    return extracted_data

############ Transform Methods ############
def transform(data):
    log("In transform(): started")
    # Convert all Height values from in. to m
    METERS_PER_INCH = 0.0254
    data['height'] = round(data.height*METERS_PER_INCH, 2)

    # Convert all Weight values from lb to kg
    KG_PER_LB = 0.45359237
    data['weight'] = round(data.weight*KG_PER_LB, 2)

    log("In transform(): ended")
    return data


############ Load Methods ############
def load_data(target_file, transformed_data):
    log(f"In load_data(): Loading data to file '{target_file}'")
    transformed_data.to_csv(target_file)
    log(f"In load_data(): Done loading data to file '{target_file}'")


############ Main ############

log("ETL Job Started")
extracted_data = extract()

transformed_data = transform(extracted_data)

load_data(TARGET_OUTPUT_FILE, transformed_data)

log("ETL Job Ended\n")

