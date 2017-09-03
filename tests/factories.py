import mongoengine
import factory
import sys
sys.path.append('.')
from models import Task

class TaskFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = Task

    name = factory.Sequence(lambda n: f'task{n}')
    frequency = 3
    channel = 'general'