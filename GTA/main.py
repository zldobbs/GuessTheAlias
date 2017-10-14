#!flask/bin/python
import os, json
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit

from random import choice
from string import ascii_uppercase, digits, hexdigits

app = Flask(__name__)
# secret key for flask
app.secret_key = 'FF137EE9744FFBEFC1495D3FA08A639FD9F7B57330212F30B470EA2BFB5CCF5B'
socketio = SocketIO(app)

@app.route('/', methods=['GET'])
def LandingPage():
	if 'userID' not in session:
		userID = ''.join(choice(hexdigits) for i in range(16))
		session['userID'] = userID
	return render_template('landing.html')

@app.route('/about', methods=['GET'])
def AboutPage():
	return render_template('about.html')

@app.route('/createRoom', methods=['GET']) # change to createRoom at frontend
def createRoom():
	roomCode = ''.join(choice(ascii_uppercase + digits) for i in range(6))
	return redirect(url_for('.RoomPage', code=roomCode, moderator=True))

@app.route('/joinRoom', methods=['POST']) # change to createRoom at frontend
def joinRoom():
	roomCode = request.form["roomCode"]
	# check for existing room before redirecting
	return redirect(url_for('.RoomPage', code=roomCode, moderator=False))

@app.route('/room', methods=['GET'])
def RoomPage():
	roomCode = request.args['code']
	return render_template('waitingRoom.html', code=roomCode)
	# return roomCode + ' ' + session['userID']

@socketio.on('connect', namespace='/room')
def connected():
    emit('response', {'name': 'Alice'})

@socketio.on('getUserID', namespace='/getUserID')
def GetUserID():
	emit('UserID response', {'userID': session['userID']})




@app.route('/sendHints', methods=['POST'])
def getHints():
	pass

# temp route for testing
@app.route('/testFactForm', methods=['GET'])
def testFactForm():
	return render_template('factForm.html')

# temp route for testing
@app.route('/testWaitingRoom', methods=['GET'])
def testWaitingRoom():
	return render_template('waitingRoom.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
