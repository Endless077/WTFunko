# Main
import pymongo

# Own Modules
from utils import *
from server.mongoDB import *

def main():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    
if __name__ == "__main__":
    main()