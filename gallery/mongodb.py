
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def insert_record(data):
    uri = ""

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        image_data = client["Gallery"]
        img_collection = image_data['Image_data']
        print(data)
        img_collection.insert_one(data)
        print("Data added succesfully")

    except Exception as e:
        print(e)