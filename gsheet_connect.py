import gspread
from google.oauth2.service_account import Credentials

credentials_file = 'credentials.json'
# 3. authenticate function to authenticate the api credentials
def authenticate():
    # Define the scope
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    # Load credentials from file
    creds = Credentials.from_service_account_file(credentials_file, scopes=scope)
    # Authorize the client
    client = gspread.authorize(creds)
    return client
