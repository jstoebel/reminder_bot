import os
import re

from flask import Flask, jsonify, request
from mongoengine import connect, DoesNotExist
from models import Task
import json

app_config = json.loads(open('app.json').read())
app = Flask(app_config['name'])
connect(app_config['name'])

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
        regex = 'name=(?P<name>.*)freq=(?P<freq>.*)qty=(?P<freq>.*)units=(?P<units>.*)'
        match = re.search(, text)
        name, freq_str = match.group('name').strip(), match.group('freq')
        frequency = int(freq_str)
        attrs = {'name': name, 'frequency': frequency}
    except (ValueError, AttributeError) as err:
        print(err)
        error_msg = 'Please provide a task name and its frequency (in hours). Example: name=eat pizza freq=3'
        return jsonify({'text': error_msg})

    try:
        # save to database
        task = Task(**attrs)
        task.save()
        time_unit = 'hours' if frequency > 1 else 'hour'
        return jsonify({'text': f':ok_hand: Got it! I\'ll remind you to {name} every {frequency} {time_unit}'})
    except:
        return jsonify({'text': ':thinking_face: hmm... something went wrong. Can you try again later?'})

@app.route('/task_status', methods=['POST'])
def task_status():
    task_name = request.form['text']
    try:
        task = Task.objects.get(name=task_name)
        return jsonify({'text': f'found a task! {task.name}'})
    except DoesNotExist:
        return jsonify({'text': ':thinking_face: hmmm...I couldn\'t find that task.'})

# @app.route('/new_event')
# def new_event():
#     pass

# # routes:   
#     # new task :task_name
#     # new event :task_name
#     # :task_name status
#     # help
# if re.search(r'^new task', msg_txt):
#     # add new task
#     pass
# elif re.search(r'^new event', msg_txt):
#     # add new event
#     pass
# elif 'status' in msg_txt:
#     # get status of a task
#     pass
# else:
#     # help!
# pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port, debug=True)