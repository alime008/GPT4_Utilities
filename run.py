import os, sys
from openai import OpenAI
import openai
from dotenv import load_dotenv
import json
import gspread
from google.oauth2 import service_account
from googleapiclient.discovery import build
# Load the .env file
load_dotenv()

# Path to the service account key file
KEY_FILE_PATH = 'GSheets_API_KEY.json'

# Google Sheet details
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
RANGE_NAME = 'Sheet1'  # Adjust the range as necessary

client = OpenAI()


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

# Example usage
prompt = "david beckham"
image_url = GenerateImage(prompt)

#if __name__ == '__main__':
 #   (GenerateImage('test'))