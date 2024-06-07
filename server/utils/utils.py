# Utils             

# Math Libraries
import random
import bcrypt
import pandas as pd

# OS libraries
import os

# Struct libreries
import json

# Time libreries
from datetime import datetime as dt

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

# Generate hash string
def hash_string(string: str) -> bytes:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(string.encode(), salt)
    return hashed

def hash_string_match(string: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(string.encode(), hashed)

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
def new_user(username: str, email: str, password: str) -> dict:
    user_id = generate_random_id(username)
    
    hashed_password = hash_string(password)
    return {
        f"{username}_{user_id}":{
            "_id": user_id,
            "username": username,
            "email": email,
            "password": hashed_password
        }
    }

# Setup a new order
def new_order(user: dict, products: list[tuple], status: str) -> dict:
    order_id = generate_order_id()
    
    current_date = dt.now().isoformat()
    total = sum(funko["price"] * quantity for funko, quantity in products)
    return {
        f"#{order_id}":{
            "_id": order_id,
            "user": user,
            "products": products,
            "total": total,
            "date": current_date,
            "status": status
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
            "_id": funko_id,
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

##################################################################################################