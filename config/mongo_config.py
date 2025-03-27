from pymongo import MongoClient

class MongoConfig:
    def __init__(self, mongo_uri, db_name, collection_name):
        """
        Initialize the MongoDB configuration class.
        
        Args:
            mongo_uri (str): MongoDB connection string.
            db_name (str): Name of the database.
            collection_name (str): Name of the collection.
        """
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def fetch_config(self, query):
        """
        Fetch the configuration document from MongoDB.
        
        Returns:
            dict: Configuration data as a dictionary.
        """
    def fetch_config(self, query):
        config = self.collection.find_one(query)
        if not config:
            raise ValueError("Configuration not found in MongoDB.")
        return config