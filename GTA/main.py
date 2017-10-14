#!flask/bin/python
import os, json
from flask import Flask, render_template
from flask import request
from random import choice
from string import ascii_uppercase, digits

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def LandingPage():
	return render_template('landing.html')

@app.route('/about', methods=['GET'])
def AboutPage():
	pass

@app.route('/generateCode', methods=['GET'])
def GenCode():
	return ''.join(choice(ascii_uppercase + digits) for i in range(6))

@app.route('/<code>', methods=['GET'])
def RoomPage(code):
	pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
