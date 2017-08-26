import sys
sys.path.append('.')

from models import Task
from fixtures import task
import test_base
from factories import TaskFactory

import json

class TestTaskStatus(test_base.TestBase):

    def get_status(self, task_name=''):
        '''
        makes a request to /task_status
        task: the task object to query
        returns the response
        '''
        data = {'text': task_name}
        return self.app.post('/task_status', data=data, follow_redirects=True)

    def test_task_status(self):
        t = TaskFactory.create()
        # t = task('dig for gold')
        res = self.get_status(t.name)
        assert res.status == '200 OK'
        assert json.loads(res.get_data()) == {'text': t.task_report()}

    def test_all_tasks_on_no_name_given(self):
        tasks = TaskFactory.create_batch(2)

        expected_report = '\n'.join([t.task_report() for t in tasks])
        expected_response = {'text': f':thinking_face: hmmm...I couldn\'t find that task. Here are all of the tasks\n {expected_report}'}
        res = self.get_status()

        assert json.loads(res.get_data()) == expected_response

    def test_all_tasks_on_bad_name_given(self):
        tasks = TaskFactory.create_batch(2)
        expected_report = '\n'.join([t.task_report() for t in tasks])
        expected_response = {'text': f':thinking_face: hmmm...I couldn\'t find that task. Here are all of the tasks\n {expected_report}'}
        res = self.get_status('bogus')

        assert json.loads(res.get_data()) == expected_response

if __name__ == '__main__':
    unittest.main()