import sys
sys.path.append('.')
import app as app_file
from mongoengine import connect

class TestBase:
    def setup_method(self, method):
        app_file.app.testing = True
        self.app = app_file.app.test_client()
        self.db_client = connect('reminder_bot_test')

    def teardown_method(self, method):
        self.db_client.drop_database('reminder_bot_test')