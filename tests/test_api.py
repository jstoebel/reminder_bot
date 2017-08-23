import sys
sys.path.append('.')
import app as app_file
from mongoengine import connect

from models import Task

import os
import unittest
import tempfile
import json

class ApiTestCase(unittest.TestCase):
    def setup_method(self, method):
        app_file.app.testing = True
        self.app = app_file.app.test_client()
        self.db_client = connect('reminder_bot_test')

    def teardown_method(self, method):
        self.db_client.drop_database('reminder_bot_test')

    def make_new_task(self, text, channel_id):
        '''
        makes a request to /new_task
        text(str): the text value in the request body
        channel_id(str): the channel_id in the request body
        returns the response
        '''
        data = {'text': text, 'channel_id': channel_id}
        res = self.app.post('/new_task', data=data, follow_redirects=True)
        return res
        
    def test_new_task(self):
        expected_attrs = {'name': 'dig for gold', 'freq': '3', 'channel_id': 'general'}
        text = f'name={expected_attrs["name"]} freq={expected_attrs["freq"]}'
        res = self.make_new_task(text, expected_attrs['channel_id'])
        task = Task.objects.first()

        assert res.status == '200 OK'
        expected_response = {'text': ':thinking_face: hmm... something went wrong. Can you try again later?'}
        assert json.loads(res.get_data()) == expected_response
        assert task.name == expected_attrs['name']
        assert task.frequency == int(expected_attrs['freq'])
        assert task.channel == expected_attrs['channel_id']

    def test_new_task_missing_name(self):
        text = 'freq=3'
        res = self.make_new_task(text, 'general')
        assert res.status == '200 OK'
        assert json.loads(res.get_data()) == {'text': 'Please provide a task name and its frequency (in hours). Example: name=eat pizza freq=3'}

    def test_new_task_missing_freq(self):
        text = 'task=eat pizza'
        res = self.make_new_task(text, 'general')
        assert res.status == '200 OK'
        assert json.loads(res.get_data()) == {'text': 'Please provide a task name and its frequency (in hours). Example: name=eat pizza freq=3'}

    def test_new_task_bad_freq(self):
        text = 'task=eat pizza freq=spam'
        res = self.make_new_task(text, 'general')
        assert res.status == '200 OK'
        assert json.loads(res.get_data()) == {'text': 'Please provide a task name and its frequency (in hours). Example: name=eat pizza freq=3'}

    def test_new_task_missing_channel(self):
        pass
    

    # def test_remove_task(self):
    #     data = {'text': 'feed ari'}
    #     self.app.post('/remove_task', data=data, follow_redirects=True)

if __name__ == '__main__':
    unittest.main()