import os, sys
from openai import OpenAI
from dotenv import load_dotenv
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build 
import gspread
#from oauth2client.service_account import ServiceAccountCredentials

def SheetsUpdate(KEY_FILE_PATH, SPREADSHEET_ID, RANGE_NAME, CELL, value_to_insert):
    
    creds = service_account.Credentials.from_service_account_file(
        KEY_FILE_PATH,
        scopes=[os.getenv("ROLE")])
    client = gspread.authorize(creds)

    # Open the spreadsheet and select the range to update
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(RANGE_NAME)
    sheet.update(range_name=CELL, values=value_to_insert)


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


def GPTPrompt(prompt):
  # Now you can use os.getenv to get your environment variable
  api_key = os.getenv("OPENAI_API_KEY")
  #print("API Key:", api_key)
  client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
  print('in function prompt',prompt)
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a sophisticated scholar who loves quotes and teaching others."},
      {"role": "user", "content": prompt}
    ],
    max_tokens = 200)

  return (completion.choices[0].message.content)

if __name__ == '__main__':
    # Load the .env file
    load_dotenv()

    # Path to the service account key file
    KEY_FILE_PATH = 'GSheets_API_KEY.json'

    # Google Sheet details
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    RANGE_NAME = 'Sheet1'  # Adjust the range as necessary

    prompt = SheetsExtract(KEY_FILE_PATH,SPREADSHEET_ID,RANGE_NAME)
    print('extracted prompt:', prompt)
    for i,v in enumerate(prompt):
        value_to_insert = GPTPrompt(v)
        CELL = 'B' + str(i+2)
        SheetsUpdate(KEY_FILE_PATH, SPREADSHEET_ID, RANGE_NAME, CELL, [[value_to_insert]])
        


