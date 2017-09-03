import sys
sys.path.append('.')

from models import Task

import pytest

@pytest.fixture
def task(name):
    '''
    name(str): name of the task
    '''
    t = Task(name=name, frequency=3, channel='general')
    t.save()
    return t