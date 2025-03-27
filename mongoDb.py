from pymongo import MongoClient

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority")
db = client["google_drive_app"]
collection = db["credentials"]

# Read the credentials.json file and insert it into MongoDB
with open("Credentials-web.json", "r") as file:
    credentials_data = file.read()

# Insert the credentials into the collection
collection.insert_one({"name": "google_drive_credentials", "data": credentials_data})
print("Credentials uploaded to MongoDB Atlas.")