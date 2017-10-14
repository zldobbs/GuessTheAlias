#!flask/bin/python
import os, json
from flask import Flask, render_template, request, redirect, url_for, session
from random import choice
from string import ascii_uppercase, digits, hexdigits

app = Flask(__name__)
app.secret_key = 'FF137EE9744FFBEFC1495D3FA08A639FD9F7B57330212F30B470EA2BFB5CCF5B'

@app.route('/', methods=['GET', 'POST'])
def LandingPage():
	if 'userID' not in session:
		userID = ''.join(choice(hexdigits) for i in range(16))
		session['userID'] = userID
	return render_template('landing.html')

@app.route('/about', methods=['GET'])
def AboutPage():
	return render_template('about.html')

@app.route('/generateCode', methods=['GET'])
def GenCode():
	roomCode = ''.join(choice(ascii_uppercase + digits) for i in range(6))
	return redirect(url_for('.RoomPage', code=roomCode))

@app.route('/room', methods=['GET'])
def RoomPage():
	roomCode = request.args['code']
	return roomCode + ' ' + session['userID']

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
