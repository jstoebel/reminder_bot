import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from slackclient import SlackClient
from models import Task
import settings

client = SlackClient(settings.TOKEN)

def check_all_tasks():

    try:
        for task in Task.objects:
            print('checking task...')
            if True: #t.is_due():
                print(f'responding with {task.task_report()} on channel {task.channel}')
                client.api_call(
                    "chat.postMessage",
                    channel=task.channel,
                    text=task.task_report(),
                )
    except NameError as err:
        print(err)

# def check_task():
#     pass


# def print_date_time():
#     print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=check_all_tasks,
    trigger=IntervalTrigger(seconds=10),
    id='checking tasks',
    name='check task status every 5 seconds',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())