from bson.objectid import ObjectId
from flask import Flask, jsonify, request
from pymongo import MongoClient, ReturnDocument
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)  # enabling CORS for all domain.
CORS(app, resources={r"/tasks/*": {"origins": "*"}})  # Enables CORS for all routes under /tasks with any origin
client = MongoClient("mongodb://localhost:27017/")
db = client.task_manager
tasks = db.tasks

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify(error=str(e)), 500

@app.route('/tasks', methods=['GET', 'POST'])
def manage_tasks():
    if request.method == 'GET':
        all_tasks = list(tasks.find({}, {'_id': 1, 'name': 1}))  # Ensure '_id' and 'name' are included
        # Convert ObjectId to string for JSON serialization
        for task in all_tasks:
            task['_id'] = str(task['_id'])
        return jsonify(all_tasks)
    elif request.method == 'POST':
        task = request.json
        result = tasks.insert_one(task)
        return jsonify({'_id': str(result.inserted_id), 'name': task['name']}), 201


@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        tasks.delete_one({'_id': ObjectId(task_id)})
        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        update_data = request.json
        result = tasks.find_one_and_update(
            {'_id': ObjectId(task_id)},
            {'$set': update_data},
            return_document=ReturnDocument.AFTER
        )
        if result:
            result['_id'] = str(result['_id'])  # Convert ObjectId to string
            return jsonify(result), 200
        else:
            return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    

if __name__ == '__main__':
    app.run(debug=True)
