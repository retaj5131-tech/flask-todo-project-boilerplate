import helpers
from google import genai
from config import GEMINI_API_KEY
import json

def create_todo(user_input):
    prompt = f"""
    You are an expert Coding Mentor. The user wants to learn or do: "{user_input}". 
    Your goal is to create a professional programming roadmap or task.
    
    Format your response as a JSON object with the following structure:
    {{
        "title": "Mastering {user_input}",
        "description": "A professional step-by-step guide to achieving excellence in {user_input}.",
        "tag": "Programming", 
        "activeCrescents": 3, 
        "volunteersNeeded": 1,
        "summary": [
            "Phase 1: Fundamental Syntax & Setup",
            "Phase 2: Core Concepts & Logic",
            "Phase 3: Building a Mini-Project",
            "Phase 4: Optimization & Best Practices"
        ],
        "date": "Mar 13 2026"
    }}
    
    Note: 'activeCrescents' should be a number from 1 to 5 representing the difficulty level.
    The 'tag' should be a short category (e.g., 'Frontend', 'Backend', 'AI', 'Mobile').
    """

    genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    
   
    import json
    
    clean_response = response.text.replace('```json', '').replace('```', '').strip()
    task_data = json.loads(clean_response)
   
    tasks = helpers.read_db_file()
    
    new_task = {
        "id": len(tasks) + 1,
        "title": task_data.get("title"),
        "description": task_data.get("description"),
        "tag": task_data.get("tag"),
        "completed": False,
        "date": task_data.get("date"),
        "activeCrescents": task_data.get("activeCrescents"),
        "summary": task_data.get("summary"),
        "volunteersNeeded": task_data.get("volunteersNeeded")
    }
    
    tasks.append(new_task)
    helpers.write_db_file(tasks)
    return new_task
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    try:
        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents=prompt.format(description=description, current_time=helpers.get_current_date_formatted()),
        )
        content = response.text
        print("Generated content from Gemini API:", content)
        content = helpers.clean_gemini_response(content)
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

def update_todo(todo_id, update_data):
    task = get_todo_by_id(todo_id)
    
    tasks = helpers.read_db_file()
    tasks.remove(task)

    if "title" in update_data:
        task['title'] = update_data['title']
    if "description" in update_data:
        task['description'] = update_data['description']
    
    # -- add missing fields --
    if "date" in update_data:
        task['date'] = update_data['date']
    if "variant" in update_data:
        task['variant'] = update_data['variant']
    if "volunteersNeeded" in update_data:
        task['volunteersNeeded'] = update_data['volunteersNeeded']
    if "priority" in update_data:
        task['priority'] = update_data['priority']
    if "completed" in update_data:
        task['completed'] = update_data['completed']
    
    tasks.append(task)
    helpers.write_db_file(tasks)

    return task


def delete_todo(todo_id):
    task = get_todo_by_id(todo_id)
    
    tasks = helpers.read_db_file()
    tasks.remove(task)
    helpers.write_db_file(tasks)

    return