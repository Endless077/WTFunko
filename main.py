# Main
import pymongo

# Own Modules
#from utils import *
from server.mongoDB import *

import csv
import ast

import csv
import ast
from collections import defaultdict

import csv
import ast
from collections import defaultdict

def count_and_sort_interests(file_path):
    interest_counts = defaultdict(int)
    
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            interests = row['interest']
            # Convert the string representation of list to an actual list
            interests_list = ast.literal_eval(interests)
            # Update the count for each interest
            for interest in interests_list:
                interest_counts[interest] += 1
    
    # Sort the interests by count in descending order
    sorted_interests = sorted(interest_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Print the count of each interest in sorted order
    for interest, count in sorted_interests:
        print(f"{interest}: {count}")




def main():
    #myclient = pymongo.MongoClient("mongodb://localhost:27017/")
     #mydb = myclient["mydatabase"]
    # Path to the CSV file
# Path to the CSV file
    file_path = './source/data.csv'
    count_and_sort_interests(file_path)

    
if __name__ == "__main__":
    main()