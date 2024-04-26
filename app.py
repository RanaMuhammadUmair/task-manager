from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)  # enabling CORS for all domain.
client = MongoClient("mongodb://localhost:27017/")
db = client.task_manager
tasks = db.tasks

@app.route('/tasks', methods=['GET', 'POST'])
def manage_tasks():
    if request.method == 'GET':
        all_tasks = list(tasks.find({}, {'_id': 0}))
        return jsonify(all_tasks)
    elif request.method == 'POST':
        task = request.json
        tasks.insert_one(task)
        return jsonify({'message': 'Task added successfully!'}), 201

if __name__ == '__main__':
    app.run(debug=True)
