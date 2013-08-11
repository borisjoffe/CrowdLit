#!/usr/bin/env python
import sys
import os
import re
import urllib
import urlparse
import urllib2
from flask import Flask, render_template, url_for, request, redirect, session

import streetlight_form
import sms
import users
import history
from utils import *
 
app = Flask(__name__)
if os.getlogin() == "boris":
	app.debug = True	# local account - debug
else:
	app.debug = False	# aws/heroku account - no debug
brand = "CrowdLit"

HIGHLIGHT_COLOR = '\x1b[96;1m'
HIGHLIGHT_END = '\x1b[0m'

@app.route('/')
def index():
	return render_template('home.html')

def begin_session(args, no_session=True):
	if 'sessionId' in args:
		userId = history.History(args['sessionId'])
		dbgInfo("Logged in as", userId.userId)
		return userId
	elif no_session:
		userId = history.History('000')
		dbgInfo("Logged in as", userId.userId)
		return userId
	else:
		dbgErr("no sessionId submitted and no_session turned off")
		return False

@app.route('/getuser', methods=['POST', 'GET'])
def getuser():
	return begin_session(request.args).userId

@app.route('/home', methods=['POST', 'GET'])
def home():
	u = begin_session(request.values)
	if not u:
		dbgErr('request', request)
		return "Error: provide sessionId"
	return u.get_all_history()

@app.route('/delete', methods=['POST', 'GET'])
def delete_history():
	u = begin_session(request.values)
	if not u:
		dbgErr('request', request)
		return "Error: provide sessionId"
	return u.clear_history()

@app.route('/submitlight', methods=['POST', 'GET'])
def submitlight():
	"""Submit to seattle streetlight and internal DB"""	
	print HIGHLIGHT_COLOR + "RECEIVED: " + HIGHLIGHT_END + str(request.values)

	mandatory_args = ['LastName', 'Email', 'PoleNumber', 'Street']
	for a in mandatory_args: 
		if not a in request.values: 
			return "failure: submit all args. " + a + " is missing"

	u = begin_session(request.values, no_session=True)
	if not u:
		dbgErr('request', request)
		return "failure: provide sessionId"

	dbgInfo('seattle light request to submit', streetlight_form.build_string(request.args))

	return "success" + "<br>submitted: " + streetlight_form.build_string(request.args)
	#return render_template('submitlight.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
	"""Pass a userId=myuserid pair to login"""
	print "\n"
	if not 'userId' in request.values:
		return "ERROR: submit a userId"

	userId = request.values['userId']
	return users.login(userId)
	
@app.route('/logged_in', methods=['POST', 'GET'])
def logged_in():
	if not 'sessionId' in request.values:
		return "ERROR: submit a sessionId"
	sessionId = request.values['sessionId']
	return users.check_login(sessionId)

@app.route('/smsreply', methods=['POST', 'GET'])
def smsreply():
	return sms.process_sms_message(request.values)

@app.route('/submit2', methods=['POST', 'GET'])
def submit2():
	dbgInfo('request', request)
	print HIGHLIGHT_COLOR + "RECEIVED: " + HIGHLIGHT_END + str(request.values)
	resp = "<small>"+ render_args(request.values) + "</small><br>"
	return resp
	
@app.route('/submit', methods=['POST', 'GET'])
def submit():
	print HIGHLIGHT_COLOR + "RECEIVED: " + HIGHLIGHT_END + str(request.values)

	u = begin_session(request.values, no_session=True)
	if not u:
		dbgErr('request', request)
		return "Error: provide sessionId"

	if 'Body' in request.values:
		pole_number  = request.values['Body']
		if not sms.verify_pole_number(pole_number):
			dbgInfo('pole number is in wrong format. Continuing to From attr check and generic response')
		else:
			if 'Address' in request.values:
				dbgInfo('Got polenum and address')
				print u.add_history(pole_number, request.values['Address'])
				resp = "last history: " + u.get_last_history()
			else:	# use fake address
				dbgInfo('Got polenum and generated fake address')
				print u.add_history(pole_number, history.newaddr())
				resp = "last history: " + u.get_last_history()
			dbgInfo('added history. ALL history up to now', u.get_all_history())
			if 'Test' in request.values and request.values['Test'] == 'True':
				dbgInfo("Got polenum. Return JSON because of 'Test' param. last history", u.get_last_history())
				return u.get_last_history()

	if not 'From' in request.values:
		dbgWarn("no 'From' key in request. Not SMS - Not Replying")
		return render_args(request.values) + "<br>WARN: Not an SMS. Not replying"
	
	# SEND SMS
	dbgInfo("FROM DETECTED. WILL TRY TO RESPOND", request.values)
	rcpt = request.values['From']
	resp += "<hr>RECIPIENT: " + rcpt + "<br>"
	dbgInfo('FROM', rcpt)
	resp += "<h3>Twilio Response:</h3>"
	
	dbgInfo("send_sms() retval", sms.send_sms())
	return resp

def render_args(args):
	s = "<h3>REQUEST PARAMS</h3>"
	for item in args:
		s += item + " = " + args[item] + "<br>"
	return s

@app.route('/wsdl', methods=['POST', 'GET'])
def wsdl():
	return render_template('wsdl_response.wsdl')

@app.route('/hello', methods=['POST', 'GET'])
def hello_wsdl():
	return render_template('hello.wsdl')

def main():
	port = int(os.environ.get('PORT', 5000))	# for heroku
	app.run(host='0.0.0.0', port=port)
	return 0

if __name__ == "__main__":
	sys.exit(main())

