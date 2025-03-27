import streamlit as st
from config.mongo_config import MongoConfig

mongo_uri = st.secrets["MONGO_URI"]  # Store the MongoDB URI in Streamlit Secrets
db_name = st.secrets["db_name"]
collection_name = st.secrets["collection_name"]
mongo_config = MongoConfig(mongo_uri, db_name, collection_name)
credentials_doc = mongo_config.fetch_config({"name": "google_drive_credentials"})



st.write("MongoDB URI:", mongo_uri)
st.write("Google Credentials JSON:", credentials_doc)