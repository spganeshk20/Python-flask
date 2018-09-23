"""
script name   : app.py
Functionality : Simple hello world flask application
Created on    : 23 SEP 2018
"""
__author__ = 'Ganesh'

# Global Imports
from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello'


if __name__ == '__main__':
    app.run(port=5000, debug=True)


