import os
import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Define the scope for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

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
            # Create the OAuth flow in headless mode
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            
            # Run the flow in console mode (no browser)
            creds = flow.run_console()
        
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