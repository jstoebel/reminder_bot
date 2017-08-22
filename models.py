from mongoengine import Document, StringField, IntField, DateTimeField, ListField, ReferenceField
import datetime

class Task(Document):
    '''
    fields:
        name(str): the name of the task (required)
        frequency(int): the frequency of the task in hours (required)
        channel(string): the channel where the task was created

    '''
    name = StringField(required=True, unique=True)
    frequency = IntField(required=True)
    channel = StringField(required=True)
    events = ListField(DateTimeField(default=datetime.datetime.now))

    def last_event(self):
        '''
        returns them most recent event
        if no events return None
        '''
        if self.events:
            self.events.sort()
            return self.events[-1]

    def task_report(self):
        '''
        return string reporting on the tasks last events
        example: f'{self.name}: last done @ {last_event:%m/%d/%Y %H:%M:%S}'
        or 
        f'{self.name}: last done never'
        '''

        latest_event = self.last_event()

        if self.is_due():
            due_alert = ':rotating_light: IS DUE'
        else:
            due_alert = 'is not due'

        if latest_event is not None:
            return f'{self.name}: last done @ {latest_event:%m/%d/%Y %H:%M} and {due_alert}'
        else:
            return f'{self.name}: last done never and {due_alert}'

    def is_due(self):
        '''
        returns if this task is now due
        '''

        last_done = self.last_event()
        if last_done is None:
            return True
        hours_since_last_event = (datetime.datetime.now() - last_done).seconds / 3600
        return hours_since_last_event >= self.frequency
