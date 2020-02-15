from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from celery import uuid


from celery_worker.celery_worker import execute_celery_tasks

import time

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase" #needs to be changed
app.config['SECRET_KEY'] = 'secret!'
app.config['CELERY_BROKER_URL'] = 'amqp://dan_celery:dan_celery@localhost/dan_celery'
app.config['CELERY_RESULT_BACKEND'] = 'amqp://dan_celery:dan_celery@localhost/dan_celery'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app, resources={r"/data/*": {"origins": "*"}})

@app.route('/')
def main():
    return 'hello'

# Example: https://blog.miguelgrinberg.com/post/using-celery-with-flask
# backend needs to be changed from rpc to a more persistent backend like redis
# https://celery.readthedocs.io/en/latest/getting-started/first-steps-with-celery.html#keeping-results

@app.route('/data')
def data():
    task_id = uuid()
    task = execute_celery_tasks.AsyncResult(task_id)
    import pdb; pdb.set_trace()
    current_loop = 0
    percent = 0
    while task.state == 'PENDING':
        if task.info is None:
            percent = 0
        else:
            percent = task.info.get('percent')
        socketio.emit('ready', { 'percentage': percent })

    return {
        'data': 'Complete',
        'message': 'Data requested successfully'
    }

if __name__ == '__main__':
    socketio.run(app, debug=True)
