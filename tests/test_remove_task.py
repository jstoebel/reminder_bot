import sys
sys.path.append('.')

from models import Task
from fixtures import task
import test_base
from factories import TaskFactory

import json

class TestRemoveTask(test_base.TestBase):
    def setup_method(self, method):
        '''
        setup for test and create a new task
        '''
        super(TestRemoveTask, self).setup_method(method)
        self.task = TaskFactory.create()

    def remove_task(self, task_name):
        '''
        remove a task
        task_name(str) name of task to remove
        '''

        data = {'text': task_name}
        return self.app.post('/remove_task', data=data, follow_redirects=True)

    def test_remove_successfully(self):
        res = self.remove_task(self.task.name)
        expected_data = {'text': f':boom: remove task {self.task.name}'}
        assert res.status == '200 OK'
        assert json.loads(res.get_data()) == expected_data
        assert len(Task.objects) == 0

    def test_bad_task(self):
        bad_task_name = 'bad task'
        res = self.remove_task(bad_task_name)
        expected_data = {'text': f':thinking_face: could not find task {bad_task_name}.'}
        assert res.status == '200 OK'
        assert json.loads(res.get_data()) == expected_data
        assert len(Task.objects) == 1

    def test_no_task(self):
        bad_task_name = ''
        res = self.remove_task(bad_task_name)
        expected_data = {'text': f':thinking_face: could not find task {bad_task_name}.'}
        assert res.status == '200 OK'
        assert json.loads(res.get_data()) == expected_data
        assert len(Task.objects) == 1

if __name__ == '__main__':
    unittest.main()