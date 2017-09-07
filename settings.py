# settings.py
import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
TOKEN = os.environ.get('SLACK_TOKEN')
MONGODB_SETTINGS = {
    'host': os.environ.get('MONGODB_URI'),
    'db': 'reminder_bot'
}

