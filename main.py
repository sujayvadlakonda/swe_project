from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = 'TheSecretIngredientToTheSecretIngredientSoup'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
active_username = False


class Account(db.Model):
    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))

    
    def __init__(self, username, password):
        self.username = username
        self.password = password

    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(100))
    date = db.Column(db.Date)


def create_account(username, password, repeat_password):
    # Ensure an account with the same username does not already exist
    existing_account = Account.query.filter_by(username=username).first()
    if existing_account:
        return 'Account already exists'

    if password != repeat_password:
        return 'Passwords do not match!'
    
    account = Account(username, password)
    db.session.add(account)
    db.session.commit()
    return 'Account created! Go back to home page to login'

    
@app.route('/')
def index():
    return render_template('index.html', active_username=active_username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        account = Account.query.filter_by(username=username).first()
        if not account:
            msg = 'No account with that username found'
        elif account.password != password:
            msg = 'Passwords do not match'
        else:
            global active_username
            active_username = username
            print('Active Username: ' + active_username)
            return redirect('/')
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    global active_username
    active_username = False
    return redirect('/')


@app.route('/create_account', methods=['GET', 'POST'])
def create_account_endpoint():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repeat_password = request.form['repeat_password']
        msg = create_account(username, password, repeat_password)
        
    return render_template('create_account.html', msg=msg)

def sortEvent(event):
    return event.date

@app.route('/events')
def events():
    if not active_username:
        return 'Need to be logged in!'

    events = Event.query.filter_by(username=active_username).all()
    if events is not None:
        events.sort(key=sortEvent)
    return render_template('events.html', events=events)


@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if not active_username:
        return 'Need to be logged in!'
    msg = ''
    if request.method == 'POST':
        name = request.form['name']
        username = active_username
        input_date = request.form['date']
        date = ''
        try:
            date = datetime.datetime.strptime(input_date, '%Y-%m-%d')
        except ValueError:
            return 'Invalid Date!'

        event = Event(name=name, username=username, date=date)
        db.session.add(event)
        db.session.commit()
        msg = 'Event successfully added'
    return render_template('add_event.html', msg=msg)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
    db.session.commit()
