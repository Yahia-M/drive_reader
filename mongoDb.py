from pymongo import MongoClient
import json

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://55brains:d9Lhrig3kDnvTwDu@resumeanalyzer.z5cc9.mongodb.net/?retryWrites=true&w=majority")
db = client["google_drive_app"]
collection = db["credentials"]

# Read the credentials.json file and parse it into a Python dictionary
with open("Credentials-web.json", "r") as file:
    credentials_data = json.load(file)  # Parse the JSON file into a dictionary

# Insert the credentials into the collection
collection.insert_one({"name": "google_drive_credentials", "data": credentials_data})
print("Credentials uploaded to MongoDB Atlas.")