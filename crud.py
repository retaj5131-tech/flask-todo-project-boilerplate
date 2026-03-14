import helpers
from google import genai
from config import GEMINI_API_KEY
import json

def create_todo(description):
    prompt = helpers.get_prompt(description)  
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    try:
        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents=prompt
        )
        content = helpers.clean_gemini_response(response.text)
        new_todo = json.loads(content)
    except Exception as e:
        return {'error': f'Failed to generate todo: {str(e)}'}

    new_todo['id'] = helpers.get_next_id()
    new_todo['completed'] = False

    tasks = helpers.read_db_file()
    tasks.append(new_todo)
    helpers.write_db_file(tasks)

    return new_todo

def get_todo_by_id(todo_id):
    tasks = helpers.read_db_file()
    for task in tasks:
        if task['id'] == todo_id:
            return task
    return None

def update_todo(todo_id, update_data):
    task = get_todo_by_id(todo_id)
    if not task:
        return {"error": "Task not found"}

    tasks = helpers.read_db_file()
    tasks.remove(task)

    for field in ["title", "description", "summary", "date", "variant", "volunteersNeeded", "priority", "completed"]:
        if field in update_data:
            task[field] = update_data[field]

    tasks.append(task)
    helpers.write_db_file(tasks)
    return task

def delete_todo(todo_id):
    task = get_todo_by_id(todo_id)
    if not task:
        return {"error": "Task not found"}

    tasks = helpers.read_db_file()
    tasks.remove(task)
    helpers.write_db_file(tasks)
    return {"message": "Delete process success"}