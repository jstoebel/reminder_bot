import json
import sys
sys.path.append('.')

from models import Task
import test_base

class TestNewTask(test_base.TestBase):

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
        time_unit = 'hours'
        text = f'name={expected_attrs["name"]} freq={expected_attrs["freq"]}'
        res = self.make_new_task(text, expected_attrs['channel_id'])
        task = Task.objects.first()

        assert res.status == '200 OK'
        expected_response = {'text': f':ok_hand: Got it! I\'ll remind you to {expected_attrs["name"]} every {expected_attrs["freq"]} {time_unit}'}
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
        text = 'task=eat pizza freq=1'
        res = self.make_new_task(text, None)
        assert res.status == '200 OK'
        assert json.loads(res.get_data()) == {'text': 'Please provide a task name and its frequency (in hours). Example: name=eat pizza freq=3'}

if __name__ == '__main__':
    unittest.main()