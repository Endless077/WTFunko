# Main
# Own Modules
#from utils import *
from pymongo import MongoClient
from server.mongo import *
import datetime

import csv
import ast

import csv
import ast
from collections import defaultdict

import csv
import ast
from collections import defaultdict


def read_csv_file(file_path):
    """Read the CSV file and return the data as a list of dictionaries."""
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        data = list(csv_reader)
    return data


def count_interests(data):
    """Count the occurrences of each interest."""
    interest_counts = defaultdict(int)
    for row in data:
        interests = row['interest']
        interests_list = ast.literal_eval(interests)
        for interest in interests_list:
            interest_counts[interest] += 1
    return interest_counts


def sort_interests(interest_counts):
    """Sort the interests by count in descending order."""
    return sorted(interest_counts.items(), key=lambda x: x[1], reverse=True)


def print_interests(interests):
    """Print the count of each interest in sorted order."""
    for interest, count in interests:
        print(f"{interest}: {count}")


def count_and_sort_interests(file_path):
    """Count and sort interests from a CSV file."""
    data = read_csv_file(file_path)
    interest_counts = count_interests(data)
    sorted_interests = sort_interests(interest_counts)
    print_interests(sorted_interests)


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


def main():
    client = MongoClient("mongodb://localhost:27017/")
    db = connect(client, "WTFunko")
    # Connect database.
    # Check if Mongo already has the collection inserted.
    # Read the JSON file for funko pops.
    # Change the dictionaries to a list of dictionaries for MongoDB.
    # Change UID so that it's _id for mongo.
    funko_pops_json_path = './source/json/products.json'
    funko_pops_json = read_json(funko_pops_json_path)
    data = list(funko_pops_json.values())
    # MongoDB recognize "_id" for unique identifiers, while the data uses uid.
    for d in data:
        d['_id'] = d.pop('uid')
    funko_pops = db["funko_pops"]
    result = funko_pops.insert_many(data)
    print(f"Data inserted into collection with ids: '{result.inserted_ids}'")
    
    client.close()


if __name__ == "__main__":
    main()