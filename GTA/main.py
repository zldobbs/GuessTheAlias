#!flask/bin/python
import os, json
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def LandingPage():
	pass

@app.route('/about', methods=['GET'])
def AboutPage():
	pass

@app.route('/generateCode', methods=['POST'])
def GenCode():
	# return roomcode
	pass

@app.route('/<code>', methods=['GET'])
def RoomPage():
	pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
