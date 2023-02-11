import os

from dotenv import load_dotenv

load_dotenv()

FACEBOOK_EMAIL = os.getenv("FACEBOOK_EMAIL")
FACEBOOK_PASSWORD = os.getenv("FACEBOOK_PASSWORD")
