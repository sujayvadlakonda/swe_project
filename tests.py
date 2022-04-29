from main import *
import unittest

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase
import sqlite3
import datetime

class DefaultTest(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.secret_key = 'TheSecretIngredientToTheSecretIngredientSoup'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.sqlite3'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True

        db = SQLAlchemy(app)

        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class CreateAccountTests(DefaultTest):
    def test_valid_account(self):
        username = 'a'
        password = 'a'
        assert create_account(username, password, password) == 'Account created! Go back to home page to login'

    def test_username_taken(self):
        username = 'a'
        password = 'a'
        create_account(username, password, password)
        assert create_account(username, password, password) == 'Account already exists'

    def test_invalid_repeat_password(self):
        assert create_account('apple', 'a', 'b') == 'Passwords do not match!'


class LoginTests(DefaultTest):
    def test_login_success(self):
        username = 'a'
        password = 'a'
        create_account(username, password, password)
        assert login(username, password) == 'Success!'

    def test_login_wrong_password(self):
        username = 'a'
        password = 'a'
        create_account(username, password, password)
        assert login(username, 'b') == 'Passwords do not match'

    def test_login_no_username(self):
        username = 'Naxadromus'
        password = 'a'
        assert login(username, password) == 'No account with that username found'
        
    
if __name__ == '__main__':
    unittest.main()
