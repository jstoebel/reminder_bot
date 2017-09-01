import sys
sys.path.append('.')

from models import Task
from fixtures import task
import test_base
from factories import TaskFactory

import json

class TestRemoveTask(test_base.TestBase):
    pass


if __name__ == '__main__':
    unittest.main()