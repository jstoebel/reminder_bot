import sys
sys.path.append('.')

from models import Task
from fixtures import task
import test_base
from factories import TaskFactory
import pytest
from mongoengine import ValidationError

import dateparser
import json

class TestTask(test_base.TestBase):

    # def setup_method(self, method):
    #     super(TestNewEvent, self).setup_method(method)
    #     self.task = TaskFactory.create()

    test_data = [
        ('name'),
        ('frequency'),
        ('channel') 
    ]

    @pytest.mark.parametrize("attr", test_data)
    def test_required_attrs(self, attr):
        t = TaskFactory.build()
        setattr(t, attr, None)

        with pytest.raises(ValidationError) as e:   
            t.save()
        assert e.value.message == f'ValidationError (Task:None) (Field is required: [\'{attr}\'])'

    def test_last_event(self):
        t = TaskFactory.create()

        # 2am and 1am
        events = [dateparser.parse(f'{hour}:00') for hour in range(2,0,-1)]
        t.events = events
        t.save()
        assert t.last_event() == events[0]


        # for hour in range(2,1,-1):
        #     event = dateparser.parse(f'{hour}:00')
        #     t.events.append(event)
        # t.events.append(dateparser.parse('10:00am'))
        # t.events.append

    def test_last_event_none(self):
        pass

    def test_task_report(self):
        pass


if __name__ == '__main__':
    unittest.main()