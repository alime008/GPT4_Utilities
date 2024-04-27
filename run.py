import os, sys
from openai import OpenAI
from dotenv import load_dotenv
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
# Load the .env file
load_dotenv()

# Path to the service account key file
KEY_FILE_PATH = 'GSheets_API_KEY.json'

# Google Sheet details
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
RANGE_NAME = 'Sheet1'  # Adjust the range as necessary

def SheetsExtract(KEY_FILE_PATH, SPREADSHEET_ID, RANGE_NAME):
    results = []
    creds = service_account.Credentials.from_service_account_file(
        KEY_FILE_PATH,
        scopes=[os.getenv("ROLE")])

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values[1:]:
            results += row
    return results

if __name__ == '__main__':
    print(SheetsExtract(KEY_FILE_PATH, SPREADSHEET_ID, RANGE_NAME))