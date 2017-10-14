#!flask/bin/python
import os, json
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room, leave_room

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

	print('userID = ' + session['userID']) # remove
	return render_template('landing.html')

@app.route('/about', methods=['GET'])
def AboutPage():
	return render_template('about.html')


@socketio.on('connect', namespace='/room')
def connected():
	emit('response', {'name': 'Alice'})

@socketio.on('join', namespace='/room')
def joinRoom(data):
	roomCode = data['roomCode']
	if roomExists(roomCode):
		join_room(roomCode)
		emit('roomResponse', {'roomCode': roomCode})
	else:
		emit('roomResponse', {'roomCode': 'invalid'})

@socketio.on('create', namespace='/room')
def createRoom(data):
	roomCode = ''.join(choice(ascii_uppercase + digits) for i in range(6))
	join_room(roomCode)
	# save session['userID'] into DB
	emit('roomResponse', {'roomCode': roomCode})

@app.route('/room/<roomCode>', methods=['GET'])
def roomPage(roomCode):
	if roomExists(roomCode):
		if userIsMod(roomCode, session['userID']):
			return render_template('waitingRoomMod.html', code=roomCode)
		return render_template('waitingRoomUser.html', code=roomCode)
	return redirect(url_for('.LandingPage'))

@socketio.on('start', namespace='/room')
def startGame(data):
	roomCode = data['roomCode']
	if userIsMod(roomCode, session['userID']):
		pass
	### emit('roomResponse', {'roomCode': roomCode})

def roomExists(roomCode):
	return True

def userIsMod(roomCode, userID):
	return True

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


if __name__ == "__main__":
		port = int(os.environ.get("PORT", 5000))
		socketio.run(app, host='0.0.0.0', port=port)
