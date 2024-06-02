# Utils             

# Math Libraries
import random
import hashlib
import pandas as pd

# OS libraries
import os
import sys
from datetime import datetime as dt

# Struct libreries
import json
import csv

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

##################################################################################################

# Current date time
def current_datetime() -> dt:
    return dt.now().strftime("%Y-%m-%d %H:%M:%S")

# Generate hash string
def hash_string(string: str) -> str:
    return hashlib.sha256(string.encode()).hexdigest()


##################################################################################################

# Generate user random id
def generate_random_id() -> str:
    return ''.join(random.choices(string.digits, k=6))

# Generate random order id
def generate_order_id() -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# Generate random funko id
def generate_funko_id() -> str:
     return ''.join(random.choices(string.digits, k=13))

# Setup a new user
def new_user(username: str, password: str, nome: str, cognome: str) -> dict:
    user_id = generate_random_id(username)
    
    hashed_password = hash_string(password)
    return {
        f"{username}_{user_id}":{
            "ID": user_id,
            "Name": nome,
            "Surname": cognome,
            "Username": username,
            "Password": hashed_password
        }
    }

# Setup a new order
def new_order(user: dict, funkos: list[tuple], status: str) -> dict:
    order_id = generate_order_id()
    
    current_date = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    total = sum(funko["price"] * quantity for funko, quantity in funkos)
    return {
        f"#{order_id}":{
            "Order ID": order_id,
            "User": user,
            "Products": funkos,
            "Total": total,
            "Date": current_date,
            "Status": status
        }
    }

# Setup a new funko
def new_funko(title, product_type: str, price: float,
              interest: list[str], license: list[str], tags: list[str],
              vendor: str, form_factor: list[str], feature: list[str],
              related: list[str], description: str, img: str) -> dict:
    funko_id = generate_funko_id()
    return {
        f"funko_{funko_id}":{
            "uid": funko_id,
            "title": title,
            "product_type": product_type,
            "price": price,
            "interest": interest,
            "license": license,
            "tags": tags,
            "vendor": vendor,
            "form_factor": form_factor,
            "feature": feature,
            "related": related,
            "description": description,
            "img": img
        }
    }