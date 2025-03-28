from pymongo import MongoClient

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://55brains:d9Lhrig3kDnvTwDu@resumeanalyzer.z5cc9.mongodb.net/?retryWrites=true&w=majority")
db = client["google_drive_app"]
collection = db["credentials"]

# Fetch the credentials document
document = collection.find_one({"name": "google_drive_credentials"})
credentials = document["data"]  # Already a dictionary

# Use the credentials
print("Client ID:", credentials["web"]["client_id"])
print("Client Secret:", credentials["web"]["client_secret"])