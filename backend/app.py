import os
from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import chatgpt_helper, sheets_helper, telegram_bot

app = Flask(__name__, static_folder='../frontend_build', static_url_path='')

tasks = []

@app.before_first_request
def load_tasks():
    global tasks
    tasks = sheets_helper.load_tasks()

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/tasks', methods=['GET','POST'])
def api_tasks():
    global tasks
    if request.method == 'GET':
        return jsonify(tasks)
    data = request.get_json()
    new_task = {
        'id': len(tasks)+1,
        'title': data.get('title'),
        'description': data.get('description',''),
        'dueDate': data.get('dueDate',''),
        'completed': False,
        'frozen': False
    }
    tasks.append(new_task)
    sheets_helper.append_task(new_task)
    return jsonify(new_task)

@app.route('/api/achievements')
def api_achievements():
    return jsonify(sheets_helper.load_achievements())

@app.route('/api/plan')
def api_plan():
    return jsonify(chatgpt_helper.generate_day_plan(tasks))

@app.route('/api/ai_suggest', methods=['POST'])
def api_ai_suggest():
    prompt = request.get_json().get('prompt','')
    return jsonify({'suggestions': chatgpt_helper.suggest_tasks(prompt)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT',5000)))
