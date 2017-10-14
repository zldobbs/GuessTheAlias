#!flask/bin/python
import os, json
<<<<<<< HEAD
from flask import Flask, render_template
from flask import request
from random import choice
from string import ascii_uppercase, digits
=======
from flask import Flask
from flask import request
>>>>>>> Views

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def LandingPage():
<<<<<<< HEAD
	return render_template('LandingPage.html')
=======
	pass
>>>>>>> Views

@app.route('/about', methods=['GET'])
def AboutPage():
	pass

<<<<<<< HEAD
@app.route('/generateCode', methods=['GET'])
def GenCode():
	return ''.join(choice(ascii_uppercase + digits) for i in range(6))


@app.route('/<code>', methods=['GET'])
def RoomPage(code):
=======
@app.route('/generateCode', methods=['POST'])
def GenCode():
	# return roomcode
	pass

@app.route('/<code>', methods=['GET'])
def RoomPage():
>>>>>>> Views
	pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
