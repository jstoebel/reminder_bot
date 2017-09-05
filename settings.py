# settings.py
import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
TOKEN = os.environ.get('SLACK_TOKEN')
MONGODB_SETTINGS = {
    'db': os.environ.get('MONGODB_URI', 'mongodb://localhost:27017'),
    'name': 'reminder_bot'
}

