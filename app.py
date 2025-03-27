import os
import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from pymongo import MongoClient
from config.mongo_config import MongoConfig

# Define the scope for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Function to connect to MongoDB Atlas and retrieve credentials
def get_credentials_from_mongodb():
    # Fetch configuration from MongoDB
    mongo_uri = st.secrets["MONGO_URI"]  # Store the MongoDB URI in Streamlit Secrets
    db_name = st.secrets["db_name"]
    collection_name = st.secrets["collection_name"]
    mongo_config = MongoConfig(mongo_uri, db_name, collection_name)
    credentials_doc = mongo_config.fetch_config({"name": "google_drive_credentials"})
    
    # Retrieve the credentials document
    #credentials_doc = collection.find_one()
    if not credentials_doc:
        raise ValueError("Credentials not found in MongoDB Atlas.")
    
    return credentials_doc["data"]

# Function to authenticate and get the Google Drive service
def get_drive_service():
    creds = None
    # Check if token.pickle file exists (stores user credentials)
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = Credentials.from_authorized_user_file('token.pickle', SCOPES)
    
    # If no valid credentials are available, prompt the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Fetch credentials from MongoDB Atlas
            credentials_json = get_credentials_from_mongodb()
            
            # Write the credentials to a temporary file
            with open("temp_credentials.json", "w") as temp_file:
                temp_file.write(credentials_json)
            
            flow = InstalledAppFlow.from_client_secrets_file("temp_credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
            
            # Clean up the temporary file
            os.remove("temp_credentials.json")
        
        # Save the credentials for future use
        with open('token.pickle', 'wb') as token:
            token.write(creds.to_json())
    
    # Build the Google Drive service
    service = build('drive', 'v3', credentials=creds)
    return service

# Function to list files in a specific folder
def list_files_in_folder(service, folder_id):
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    return files

# Streamlit App
def main():
    st.title("Google Drive Folder Reader")
    
    # Get the folder ID from the user
    folder_id = st.text_input("Enter the Google Drive Folder ID:")
    
    if folder_id:
        try:
            # Authenticate and connect to Google Drive
            service = get_drive_service()
            
            # List files in the specified folder
            files = list_files_in_folder(service, folder_id)
            
            if files:
                st.write(f"Files in folder with ID `{folder_id}`:")
                for file in files:
                    st.write(f"- {file['name']} (ID: {file['id']})")
            else:
                st.write("No files found in the specified folder.")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()