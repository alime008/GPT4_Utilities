from instabot import Bot
from dotenv import load_dotenv
import os
from ensta import Mobile

# Load the .env file
load_dotenv()

bot = Bot()

try:
    bot.login(username=os.getenv("IG_USERNAME"), password=os.getenv("IG_PASSWORD"))

    # Perform actions
except Exception as e:
    print(f"An error occurred: {e}")
    bot.logout()



# mobile = Mobile(identifier="legendquotesai@gmail.com", password=os.getenv("IG_PASSWORD"))

# profile = mobile.profile("leomessi")

# print(profile.full_name)
# print(profile.biography)
# print(profile.profile_pic_url)


# from ensta import Guest

# guest = Guest()
# profile = guest.profile("leomessi")

# print(profile.biography)