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
        for i,row in enumerate(values[1:]):
            try:
              if row[2] != '1':
                  print('C' + str(i+1))
                  results.append(row[0])
                  SheetsUpdate(KEY_FILE_PATH, SPREADSHEET_ID, RANGE_NAME, CELL=('C' + str(i+2)), value_to_insert=[['1']])
            except Exception as e:
              # This block catches any other exceptions
              print(f"An error occurred: Please Enter a Value 0 in Column C. {str(e)}")
    return results

def GPTPrompt(prompt):
  # Now you can use os.getenv to get your environment variable
  api_key = os.getenv("OPENAI_API_KEY")
  #print("API Key:", api_key)
  client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
  print('in function prompt',prompt)
  completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
      {"role": "system", "content": "You are a sophisticated scholar who loves quotes and teaching others."},
      {"role": "user", "content": prompt}
    ],
    max_tokens = 200)

  return (completion.choices[0].message.content)


def GenerateImage(prompt):

    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    try:
        # Call the API to generate an image based on the prompt
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        # Print response for debugging
        print("Response:", response)

        # Accessing the generated image URL
        image_url = response.data[0].url  # Adjust based on the actual response structure
        print('Generated Image URL:', image_url)
        return image_url
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def EmptyCellInCol(KEY_FILE_PATH, SPREADSHEET_ID, SHEET_NAME, COL):
    # Set scopes and load credentials
    scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    creds = service_account.Credentials.from_service_account_file(
        KEY_FILE_PATH, scopes=scopes)
    service = build('sheets', 'v4', credentials=creds)

    # Specify the range for column B (adjust SHEET_NAME as necessary)
    RANGE_NAME = f'{SHEET_NAME}!A'+':'+COL

    # Read the current values in column B
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    print(result)

    # Find empty cells in column B
    empty_cells = []
    max_row = 0
    for i, row in enumerate(values, start=1):  # Start indexing from 1 (row numbers in Sheets)
        print('i:',i,'row:',row)
        if len(row)>max_row:
            max_row = len(row)
        if len(row)!=max_row:  # If the row is empty
            empty_cells.append(f"{COL}{i}")
    return empty_cells

def ImagePromptExtract(prompt):
   return prompt.split('-')[1]

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

    prompt_empty_cell = EmptyCellInCol(KEY_FILE_PATH, SPREADSHEET_ID, RANGE_NAME, 'B')
    image_empty_cell = EmptyCellInCol(KEY_FILE_PATH, SPREADSHEET_ID, RANGE_NAME, 'D')


    for prompt, prompt_cell,image_cell in zip(prompt, prompt_empty_cell,image_empty_cell):
      QuotePrompt = GPTPrompt(prompt)  # Assume GPTPrompt returns a string or value to insert
      print('value_to_insert:', QuotePrompt)
      Hero = ImagePromptExtract(QuotePrompt)
      print('Hero:', Hero)
      ImagePrompt = GenerateImage(Hero)
      SheetsUpdate(KEY_FILE_PATH, SPREADSHEET_ID, RANGE_NAME, prompt_cell, [[QuotePrompt]])
      SheetsUpdate(KEY_FILE_PATH, SPREADSHEET_ID, RANGE_NAME, image_cell, [[ImagePrompt]])
    
    # for prompt, cell in zip(prompt, image_empty_cell):
    #   value_to_insert = ImagePrompt(prompt)  # Assume GPTPrompt returns a string or value to insert
    #   print('image_url:', value_to_insert)
    #   SheetsUpdate(KEY_FILE_PATH, SPREADSHEET_ID, RANGE_NAME, cell, [[value_to_insert]])



  