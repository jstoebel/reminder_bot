import sys
sys.path.append('.')

from models import Task
from fixtures import task
import test_base
from factories import TaskFactory

import dateparser
import json

class TestNewEvent(test_base.TestBase):

    def setup_method(self, method):
        super(TestNewEvent, self).setup_method(method)
        self.task = TaskFactory.create()

    def new_event(self, text):
        '''
        makes a request to /task_status
        task: the task object to query
        returns the response
        '''
        data = {'text': text}
        return self.app.post('/new_event', data=data, follow_redirects=True)

    def test_add_new_event(self):
        '''
        test adding a new event successfully
        '''
        expected_time = dateparser.parse('12:00')
        text = f'task={self.task.name} time={expected_time:%H:%M}'
        res = self.new_event(text)
        assert res.status == '200 OK'
        expected_response = f':pencil: got it! I added an event for {self.task.name} at {expected_time:%m/%d/%Y %H:%M}'
        assert json.loads(res.get_data()) == {'text': expected_response}
        assert len(Task.objects) == 1
        assert len(Task.objects[0].events) == 1 
        assert Task.objects[0].events[0] == expected_time

    def test_fails_with_no_input(self):
        '''
        when no input is given
        '''
        res = self.new_event('')
        assert res.status == '200 OK'
        expected_response = 'Please provide an event and the time it happened. Example: task=eat pizza time=12:00'
        assert json.loads(res.get_data()) == {'text': expected_response}

    def test_fails_with_no_date(self):
        '''
        when no date is given
        '''
        text = f'task={self.task.name}'
        res = self.new_event(text)
        assert res.status == '200 OK'
        expected_response = 'Please provide an event and the time it happened. Example: task=eat pizza time=12:00'
        assert json.loads(res.get_data()) == {'text': expected_response}

    def test_fails_with_no_task(self):
        '''
        no task name is given
        '''
        text = f'time=12:00'
        res = self.new_event(text)
        assert res.status == '200 OK'
        expected_response = 'Please provide an event and the time it happened. Example: task=eat pizza time=12:00'
        assert json.loads(res.get_data()) == {'text': expected_response}

    def test_fails_with_bad_time(self):
        '''
        badly formatted time given
        '''
        text = f'task={self.task.name} time=bad time'
        res = self.new_event(text)
        assert res.status == '200 OK'
        expected_response = ':thinking_face: I didn\'t understand that time. Please correct it and try again.'
        assert json.loads(res.get_data()) == {'text': expected_response}

    def test_fails_with_bad_task(self):
        '''
        non existant task given
        '''
        text = f'task=bad task time=12:00'
        res = self.new_event(text)
        assert res.status == '200 OK'
        expected_response = ':thinking_face: hmmm...I couldn\'t find that task.'
        assert json.loads(res.get_data()) == {'text': expected_response}

if __name__ == '__main__':
    unittest.main()