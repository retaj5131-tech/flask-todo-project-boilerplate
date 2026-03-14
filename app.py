from flask import Flask, jsonify, request
from flask_cors import CORS

import config
import crud
import helpers

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
CORS(app)



@app.route('/')
def index():
    return "Hello from Flask!"

@app.route("/todos", methods=["GET"])
def get_todos_route():
    tasks = helpers.read_db_file()
    return jsonify(tasks)

@app.route("/todos", methods=["POST"])
def create_todo_route():
    data = request.get_json()
    if 'description' not in data:
        return jsonify({"error": "description required"}), 400

    new_task = crud.create_todo(data['description'])
    if 'error' in new_task:
        return jsonify(new_task), 500
    
    return jsonify(new_task), 200

@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo_route(todo_id):
    task = crud.get_todo_by_id(todo_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200

@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo_route(todo_id):
    update_data = request.get_json()
    updated_task = crud.update_todo(todo_id, update_data)
    if 'error' in updated_task:
        return jsonify(updated_task), 404
    return jsonify(updated_task), 200

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo_route(todo_id):
    result = crud.delete_todo(todo_id)
    if 'error' in result:
        return jsonify(result), 404
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)