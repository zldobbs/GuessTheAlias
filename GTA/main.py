#!flask/bin/python
import os, json, eventlet
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room, leave_room

from random import choice
from string import ascii_uppercase, digits, hexdigits

app = Flask(__name__)
# secret key for flask
app.secret_key = 'FF137EE9744FFBEFC1495D3FA08A639FD9F7B57330212F30B470EA2BFB5CCF5B'
socketio = SocketIO(app)





from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlalchemy_gta.db'
db = SQLAlchemy(app)


class Rooms(db.Model):
	roomID = db.Column(db.String(6), primary_key=True)
	roomState = db.Column(db.String(8), nullable=True)
	currentAlias_FK = db.Column(db.String(16), nullable=True)
	roomCreator_FK = db.Column(db.String(16), nullable=False)

	def __repr__(self):
		return '<roomID: %r | Mod: %r>' % (self.roomID, self.roomCreator_FK)

class Teams(db.Model):
	color = db.Column(db.String(13), primary_key=True) 
	rooms_FK = db.Column(db.String(6), primary_key=True)
	Score = db.Column(db.Integer)

	def __repr__(self):
		return '<room: %r | color: %r>' % (self.roomID, self.color)

class Players(db.Model):
	userID = db.Column(db.String(16), primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	hint1 = db.Column(db.Text, nullable=True)
	hint2 = db.Column(db.Text, nullable=True)
	hint3 = db.Column(db.Text, nullable=True)
	hint4 = db.Column(db.Text, nullable=True)
	hint5 = db.Column(db.Text, nullable=True)
	hint6 = db.Column(db.Text, nullable=True)
	readyStatus = db.Column(db.Boolean, nullable=False)
	color_FK = db.Column(db.String(13), nullable=True)
	rooms_FK = db.Column(db.String(6), nullable=False)

	def __repr__(self):
		return '<userID: %r | Name: %r>' % (self.userID, self.name)

db.create_all()





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

	playerEntry = Players(
		userID = session['userID'],
		name = str(data['name']),
		hint1 = '',
		hint2 = '',
		hint3 = '',
		hint4 = '',
		hint5 = '',
		hint6 = '',
		readyStatus = False,
		color_FK = 'red',
		rooms_FK = roomCode
	)
	roomEntry = Rooms(
		roomID = roomCode,
		roomState = 'lobby',
		currentAlias_FK = '',
		roomCreator_FK = session['userID']
	)
	db.session.add(roomEntry)
	db.session.add(playerEntry)
	db.session.commit()

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
		emit('beginGame', room=roomCode)

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
