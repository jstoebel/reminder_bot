import os
import re

from flask import Flask, jsonify, request
from mongoengine import connect, DoesNotExist
from models import Task
import json
import dateparser

app_config = json.loads(open('app.json').read())
app = Flask(app_config['name'])

@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'worked!'})

@app.route('/new_task', methods=['POST'])
def new_task():
    '''
    create a new task
        expected format: /new_task name=eat pizza freq=1
        name(str): the name of the task
        freq(str): the frequency of the task in hours. must be a number
        quantity(int, optional): the quantity required in each cycle
        units(string, optional): the name the unit (example, ounces)
    '''
    try:
        # try to set the attributes
        text = request.form['text']
        regex = 'name=(?P<name>.*)freq=(?P<freq>.*)'
        match = re.search(regex, text)
        name, freq_str = match.group('name').strip(), match.group('freq')
        frequency = int(freq_str)
        attrs = {'name': name, 'frequency': frequency, 'channel': request.form['channel_id']}
    except (ValueError, AttributeError) as err:
        error_msg = 'Please provide a task name and its frequency (in hours). Example: name=eat pizza freq=3'
        return jsonify({'text': error_msg})
    try:
        # save to database
        task = Task(**attrs)
        task.save()
        time_unit = 'hours' if frequency > 1 else 'hour'
        return jsonify(
            {
                'text': f':ok_hand: Got it! I\'ll remind you to {name} every {frequency} {time_unit}'
            }
        )
    except:
        return jsonify({'text': ':thinking_face: hmm... something went wrong. Can you try again later?'})

@app.route('/task_status', methods=['POST'])
def task_status():
    task_name = request.form['text']
    try:
        if not task_name:
            raise DoesNotExist # don't bother with db lookup if no value given
        task = Task.objects.get(name=task_name)
        return jsonify({'text': task.task_report()})
    except DoesNotExist:
        # couldn't find that task. get all tasks
        all_tasks = '\n'.join([t.task_report() for t in Task.objects])
        return jsonify({'text': f':thinking_face: hmmm...I couldn\'t find that task. Here are all of the tasks\n {all_tasks}'})

@app.route('/new_event', methods=['POST'])
def new_event():
    '''
    create a new event for a task.
    expected format:
        task(str): the name of the task
        time(str): the time of the task 
    '''

    try:
        # try to set the attributes
        text = request.form['text']
        regex = 'task=(?P<task>.*)time=(?P<time>.*)'
        match = re.search(regex, text)
        task_name, time_str = match.group('task').strip(), match.group('time')
        time = dateparser.parse(time_str)
        # if user entered an invalid time, reject
        if time_str is not None and time is None:
            return jsonify({'text': ':thinking_face: I didn\'t understand that time. Please correct it and try again.'})
    except (ValueError, AttributeError) as err:
        error_msg = 'Please provide an event and the time it happened. Example: task=eat pizza time=12:00'
        return jsonify({'text': error_msg})

    # pull the task from the database
    try:
        task = Task.objects.get(name=task_name)
    except DoesNotExist:
        return jsonify({'text': ':thinking_face: hmmm...I couldn\'t find that task.'})

    # create the event and add it
    task.events.append(time)
    task.save()
    return jsonify({'text': f':pencil: got it! I added an event for {task.name} at {time:%m/%d/%Y %H:%M}'})

@app.route('/remove_task', methods=['POST'])
def remove_task():
    '''
    remove an event
    '''
    task_name = request.form['text']
    try:
        task = Task.objects.get(name=task_name)
        task.delete()
        return jsonify({'text': f':boom: remove task {task.name}'})
    except DoesNotExist:
        return jsonify({'text': f':thinking_face: could not find task {task_name}.'})

if __name__ == '__main__':
    import schedule
    connect(app_config['name'])
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)