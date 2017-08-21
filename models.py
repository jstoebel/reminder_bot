from mongoengine import Document, StringField, IntField, DateTimeField, ListField, ReferenceField
import datetime

class Event(Document):
    '''
    fields:
        date_modified(datetime): the timestamp of this event

    '''
    date_modified = DateTimeField(default=datetime.datetime.now)
    
class Task(Document):
    '''
    fields:
        name(str): the name of the task (required)
        frequency(int): the frequency of the task in hours (required)
        quantity(int, optional): the quantity required in each cycle
        units(string, optional): the name the unit (example, ounces)
    '''
    name = StringField(required=True, unique=True)
    frequency = IntField(required=True)
    quantity = IntField()
    units = StringField()
    events = ListField(ReferenceField(Event))