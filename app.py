from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import pymongo
import dns

load_dotenv()
URI = os.getenv('URI')
app = Flask(__name__)

@app.route('/')
def signup():
    return render_template('signup.html');

@app.route('/signup_success')
def signup_success():
    name = request.args.get('name')
    email = request.args.get('email')
    password = request.args.get('password')

    inputs = {
        'name': name,
        'email': email,
        'password': password
    }

    def add_to_db(inputs):
        my_client = pymongo.MongoClient(URI)
        my_db = my_client['VHomes']
        my_col = my_db['users']
        my_col.insert_one(inputs)

    add_to_db(inputs);
    return render_template('signup_success.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_success')
def login_success():
    email = request.args.get('email')
    password = request.args.get('password')

    inputs = {
        'email': email,
        'password': password
    }

    def get_from_db(email, password):
        my_client = pymongo.MongoClient(URI)
        my_db = my_client['VHomes']
        my_col = my_db['users']
        user = my_col.find_one({'email': str(email)}, {'password': str(password)})
        return(user)

    if get_from_db(email, password) == None:
        response = 'incorrect username or password'
    else:
        response = 'logged in as ' + email
    return render_template('login_success.html', response=response)