import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to the service account key file
KEY_FILE_PATH = 'GSheets_API_KEY.json'

# Google Sheet details
SPREADSHEET_ID = '1GpjLWxqW5Bs5_L-LORkg8Oo23QrXDF1oPjDT8uF8Ocs'
RANGE_NAME = 'Sheet1'  # Adjust the range as necessary

def SheetsExtract():
    creds = service_account.Credentials.from_service_account_file(
        KEY_FILE_PATH,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values[1:]:
            print(row[0])

if __name__ == '__main__':
    SheetsExtract()


    
