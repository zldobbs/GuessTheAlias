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

@app.route('/room', methods=['GET', 'POST'])
def RoomPage():
	if request.method == 'POST':
		if request.form['action'] == 'create':
			roomCode = ''.join(choice(ascii_uppercase + digits) for i in range(6))
			creator = session['userID']
			return render_template('waitingRoomMod.html', code=roomCode)

		if request.form['action'] == 'join':
			roomCode = request.form["roomCode"]
			if roomExists(roomCode):
				return render_template('waitingRoomUser.html', code=roomCode)
			return redirect(url_for('.LandingPage'))

		if request.form['action'] == 'start':
			return render_template('factForm.html', code=roomCode)

		return 'Error: Incorrect action'

	if request.method == 'GET':
		#check DB if user is room mod
		if roomExists(roomCode):
			return render_template('waitingRoomUser.html', code=request.args['code'])
		return redirect(url_for('.LandingPage'))

def roomExists(roomCode):
	return True

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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
