import os, sys
from openai import OpenAI
import openai
from dotenv import load_dotenv
import json
import gspread
from google.oauth2 import service_account
from googleapiclient.discovery import build
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
# Load the .env file
load_dotenv()

# Path to the service account key file
KEY_FILE_PATH = 'GSheets_API_KEY.json'

# Google Sheet details
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
RANGE_NAME = 'Sheet1'  # Adjust the range as necessary

client = OpenAI()

from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

def add_quote_to_image(image_url, quote, font_path='Andale Mono.ttf', font_size=20):
    """
    Adds a quote to an image from a given URL and displays it.

    Parameters:
        image_url (str): The URL of the image.
        quote (str): The quote to add to the image.
        font_path (str): Path to the .ttf font file.
        font_size (int): Size of the font.

    Returns:
        None: The function will display the image with the quote.
    """
    # Load the image from the URL
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    # Prepare to draw on the image
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        # Fallback to the default font if the provided one fails to load
        print('error')
        font = ImageFont.load_default()

    # Define text position (modify these as needed)
    text_x = 100
    text_y = 512

    # Add text to image
    draw.text((text_x, text_y), quote, font=font, fill=(0, 0, 0))  # Change fill color if needed

    # Display the image
    image.show()

    # Uncomment the next line to save the image
    # image.save('output_image.png')

# Example usage:
add_quote_to_image('https://oaidalleapiprodscus.blob.core.windows.net/private/org-0LK88hpKXIIiSfqYe0MitzHa/user-zLYRlwhJwLEaz5vxZQfVl27R/img-GiE6f0tlHxnKKJfdeu1r0EaP.png?st=2024-04-28T21%3A27%3A55Z&se=2024-04-28T23%3A27%3A55Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-04-28T19%3A46%3A25Z&ske=2024-04-29T19%3A46%3A25Z&sks=b&skv=2021-08-06&sig=gQrUpNsNNU18S/lE1P89ZykEcRvQGbqOgFlPKgYg1K8%3D', "Impossible is not a declaration. It's a dare. - David Beckham")
