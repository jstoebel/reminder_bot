import sys
sys.path.append('.')

from models import Task
from fixtures import task
import test_base
from factories import TaskFactory
import pytest
from mongoengine import ValidationError

from dateparser import parse
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
        '''
        test all attrs that are required
        '''
        t = TaskFactory.build()
        setattr(t, attr, None)

        with pytest.raises(ValidationError) as e:   
            t.save()
        assert e.value.message == f'ValidationError (Task:None) (Field is required: [\'{attr}\'])'

    def test_last_event(self):
        '''
        test that the latest event is the most recent not last in the list
        '''
        t = TaskFactory.create()

        # 2am and 1am
        events = [parse(f'{hour}:00') for hour in range(2,0,-1)]
        t.events = events
        t.save()
        assert t.last_event() == events[0]

    def test_last_event_none(self):
        '''
        returns None when no events present
        '''
        t = TaskFactory.create()
        assert t.last_event() is None

    def test_is_due_no_events(self):
        '''
        should be due when no events present
        '''
        t = TaskFactory.create()
        assert t.is_due()

    def test_is_due(self):
        t = TaskFactory.create()
        last_event = parse(f'{t.frequency} hours ago')
        t.events.append(last_event)
        t.save()
        assert t.is_due()

    def test_not_due(self):
        '''
        not due when an event within the frequency
        '''
        t = TaskFactory.create()
        last_event = parse(f'{t.frequency - 1} hours ago')
        t.events.append(last_event)
        t.save()
        assert not t.is_due()

    def test_report(self):
        '''
        task has an event and is due 
        '''

        t = TaskFactory.create()
        last_event = parse(f'{t.frequency} hours ago')
        t.events.append(last_event)
        t.save()
        assert t.task_report() == f'{t.name}: last done @ {last_event:%m/%d/%Y %H:%M} and :rotating_light: IS DUE'

    def test_report_no_event(self):
        t = TaskFactory.create()
        assert t.task_report() == f'{t.name}: last done never and :rotating_light: IS DUE'

    def test_report_not_due(self):
        t = TaskFactory.create()
        last_event = parse(f'{t.frequency - 1} hours ago')
        t.events.append(last_event)
        t.save()
        assert t.task_report() == f'{t.name}: last done @ {last_event:%m/%d/%Y %H:%M} and is not due'

if __name__ == '__main__':
    unittest.main()