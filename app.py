from flask import Flask, jsonify
from celery_worker.celery_worker import execute_celery_tasks

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase" #needs to be changed

@app.route('/')
def main():
    return 'hello'

@app.route('/data')
def data():
    fetched_data = execute_celery_tasks()
    return {
    'data': fetched_data,
    'message': 'Data requested successfully' 
    }



if __name__ == '__main__':
    app.run(debug=True)
