import glob 
import pandas as pd 
import xml.etree.ElementTree as ET 
from datetime import datetime 

log_file = "log_file.txt"
target_file = "transformed_data.csv"

############ Logging Methods ############
def log(msg):
    timestamp_format = "%Y-%h-%d-%H:%M:%S"
    now = datetime.now()
    timestamp_str = now.strftime(timestamp_format)

    with open(log_file, "a") as f:
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
    dataframe = pd.DataFrame(columns=["name", "height", "weight"])
    tree = ET.parse(file_to_process)
    root = tree.getroot()
    for person in root:
        name = person.find("name").text
        height = float(person.find("height").text)
        weight = float(person.find("weight").text)

        current_dataframe = pd.DataFrame([{"name":name, "height":height, "weight":weight}])

        # To avoid FutureWarning, avoid using concat() with an empty dataframe
        if dataframe.empty:
            dataframe = current_dataframe.copy()
        else:
            dataframe = pd.concat([dataframe, current_dataframe])

    return dataframe

def extract():
    log("In extract(): started")
    # Create empty data frame with the corresponding headers
    extracted_data = pd.DataFrame(columns=["name", "height", "weight"])

    # Process all CSV files
    log("In extract(): start processing CSV files")
    for csvfile in glob.glob("source/*.csv"):
        current_dataframe = extract_from_csv(csvfile)

        # To avoid FutureWarning, avoid using concat() with an empty dataframe
        if extracted_data.empty:
            extracted_data = current_dataframe.copy()
        else:
            extracted_data = pd.concat([extracted_data, current_dataframe],
                ignore_index=True)
    log("In extract(): done processing CSV files")

    # Process all JSON files
    log("In extract(): start processing JSON files")
    for jsonfile in glob.glob("source/*.json"):
        current_dataframe = extract_from_json(jsonfile)

        # To avoid FutureWarning, avoid using concat() with an empty dataframe
        if extracted_data.empty:
            extracted_data = current_dataframe.copy()
        else:
            extracted_data = pd.concat([extracted_data, current_dataframe],
                ignore_index=True)
    log("In extract(): done processing JSON files")

    # Process all XML files
    log("In extract(): start processing XML files")
    for xmlfile in glob.glob("source/*.xml"):
        current_dataframe = extract_from_xml(xmlfile)

        # To avoid FutureWarning, avoid using concat() with an empty dataframe
        if extracted_data.empty:
            extracted_data = current_dataframe.copy()
        else:
            extracted_data = pd.concat([extracted_data, current_dataframe],
                ignore_index=True)
    log("In extract(): done processing XML files")

    log("In extract(): ended")
    return extracted_data

############ Transform Methods ############
def transform(data):
    log("In transform(): started")
    # Convert all Height values from in. to m
    #   NOTE: 1 in. = 0.0254 m
    data['height'] = round(data.height*0.0254, 2)

    # Convert all Weight values from lb to kg
    #   NOTE: 1 lb =  0.45359237 kg
    data['weight'] = round(data.weight*0.45359237, 2)

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

load_data(target_file, transformed_data)

log("ETL Job Ended\n")

