from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import json

load_dotenv()
app = Flask(__name__)

MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client['user_database']

users_collection = db['users']
todo_collection = db['todo_items']


@app.route('/')
def index():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = {
            "name": request.form['name'],
            "age": int(request.form['age']),
            "city": request.form['city']
        }
        users_collection.insert_one(data)
        return redirect(url_for('success'))
    except Exception:
        return render_template('form.html', error="An error occurred while submitting the data. Please try again.")


@app.route('/success')
def success():
    return "Data submitted successfully!"


@app.route('/todo')
def todo():
    return render_template('todo.html')


@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    try:
        item = {
            "itemName": request.form['itemName'],
            "itemDescription": request.form['itemDescription']
        }
        todo_collection.insert_one(item)
        return "To-Do item added successfully!"
    except Exception:
        return "Error while adding To-Do item", 500


@app.route('/api')
def api():
    with open('data.json') as f:
        data = json.load(f)
    return data


if __name__ == '__main__':
    app.run(debug=True)
