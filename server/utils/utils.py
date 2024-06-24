# Utils             

# Math Libraries
import uuid
import random
import bcrypt
import hashlib
import pandas as pd

# OS libraries
import os

# Struct libreries
import json

# String libraries
import re
import string
from ast import literal_eval

##################################################################################################

# Extraction of the Funko Pop Dataset
# (download here: https://www.kaggle.com/datasets/victorsoeiro/funko-pop-dataset)
def extract_funko_dataset(filename: str):
    # Read the CSV file
    df = pd.read_csv(filename)
    
    # An empty dict
    data = {}
    
    # Iter on the dataframe
    for index, row in df.iterrows():
        # Get uid of the Funko
        key = f"funko_{row.iloc[0]}"
        
        # Get all the values (transform to dict)
        values = row.iloc[:].to_dict()
        
        # Clean the dataset
        clean_values(values)

        # Add to the data dict the key/values from dataframe
        data[key] = values
    
    # Define JSON filename
    json_file = os.path.join('./source/json/funko.json')
       
    # Convert dict to json and create the json_file
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def clean_values(values: dict):
    
    # Clean the description
    cleanr = re.compile('<.*?>')
    description = values["description"]
    cleantext = re.sub(cleanr, '', description)
    
    # Remove special characters (in description)
    cleantext = ''.join(filter(lambda x: x in string.printable, cleantext))
    values["description"] = cleantext
    
    # Convert strings representing python struct to the respective python struct
    values['interest'] = literal_eval(values['interest'])
    values['license'] = literal_eval(values['license'])
    values['tags'] = literal_eval(values['tags'])
    values['form_factor'] = literal_eval(values['form_factor'])
    values['feature'] = literal_eval(values['feature'])
    values['related'] = literal_eval(values['related'])
    
    # Drop useless attributes
    for attr_to_drop in ["created_at", "published_at", "updated_at", "gid", "handle"]:
        values.pop(attr_to_drop, None)

##################################################################################################

def read_json(json_file):
    if not os.path.exists(json_file):
        print(f"File '{json_file}' not found.")
        return
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print("Error filling collection:", e)
        
    return data

def save_to_json(filename: str, data: dict) -> bool:
    try:
        # Create and open the JSON file
        with open(filename, 'w') as json_file:
            # Add the input dict to the JSON file
            json.dump(data, json_file, indent=4)
        return True
    
    except Exception as e:
        print("Error while saving JSON file:", e)
        return False
    
def append_to_json(filename: str, data: dict) -> bool:
    try:
        # Check if JSON file exist
        if os.path.exists(filename):
            # Open the JSON file
            with open(filename, 'r') as json_file:
                loaded_json = json.load(json_file)
                
            # Append the input dict to the JSON struct
            loaded_json.update(data)
            
            # Overwrite changes
            with open(filename, 'w') as json_file:
                json.dump(loaded_json, json_file, indent=4)
            return True
        else:
            print("The specified JSON file does not exist.")
            return False
        
    except Exception as e:
        print("Error while appending to JSON file:", e)
        return False

##################################################################################################

# Generate Hash
def hash_string(string: str) -> bytes:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(string.encode('utf-8'), salt)
    return hashed

def hash_string_match(string: str, hashed: str) -> bool:
    return bcrypt.checkpw(string.encode('utf-8'), hashed.encode('utf-8'))
    
# Generate UID
def generate_unique_id(length: int, alphanumeric: bool = False):
    if alphanumeric:
        alphanumeric_chars = string.ascii_letters + string.digits
        unique_id = ''.join(random.choice(alphanumeric_chars) for _ in range(length))
    else:
        min_num = 10 ** (length - 1)
        max_num = (10 ** length) - 1
        unique_id = random.randint(min_num, max_num)
    
    return unique_id

##################################################################################################
