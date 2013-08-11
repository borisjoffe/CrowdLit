#!/usr/bin/env python
import sys
import os
import re
import base64
import json
import string
import urllib
import urllib2
from flask import Flask, render_template, url_for, request, redirect, session

import streetlight_form
from utils import *
 
app = Flask(__name__)
if os.getlogin() == "boris":
	app.debug = True
else:
	app.debug = False
brand = "CrowdLit"

TWILIO_AUTH_TOKEN = "0d793a4c38362e49f51b19e3c3ca7ea9"
TWILIO_SID = "ACf3f9ee7b4f7e932576ac40fbfbd2ef3c"
TWILIO_API = "https://api.twilio.com/2010-04-01/"
TWILIO_SEND_SMS_API = TWILIO_API + "Accounts/" + TWILIO_SID + "/SMS/Messages.json"

SMS_POLE_REGEXP = '\d{7}'

SESSION_FILE = os.path.join(os.getcwd(), 'sessions.dat')

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/home')
def home():
	return render_template('userpage.html')

@app.route('/submitlight', methods=['POST', 'GET'])
def submitlight():
	"""Submit to seattle streetlight and internal DB"""	
	print request.values
	return render_template('submitlight.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
	"""Pass a userId=myuserid pair to login"""
	print "\n"
	if not 'userId' in request.values:
		return "ERROR"

	userId = request.values['userId']
	print "userId: " + str(userId)
	sessions = clear_previous_sessions(userId)
	print "sessions: " + str(sessions)

	sessionId = base64.urlsafe_b64encode(os.urandom(12))
	print sessionId
	new_session = {'userId': userId, 'sessionId': sessionId}
	sessions.append(new_session)
	print "new session: " + json.dumps(new_session)

	write_all_sessions(sessions)
	print "done writing all sessions: " + json.dumps(sessions)
	return sessionId

@app.route('/logged_in', methods=['POST', 'GET'])
def logged_in():
	if not 'sessionId' in request.values:
		return "ERROR"
	sessionId = request.values['sessionId']
	return check_login(sessionId)

def check_login(sessionId):
	#print "checking session id " + sessionId
	sessions = get_all_sessions()
	#print "all sessions: " + sessions

	logged_in = False
	sessions = json.loads(sessions)
	for item in sessions:
		if item['sessionId'] == sessionId:
			logged_in = True
		#print "checking: " + item['sessionId']
	return str(logged_in)


@app.route('/smsreply', methods=['POST', 'GET'])
def smsreply():
	dbgInfo("/smsreply args", request.values)
		
	# Check for body attribute
	if not 'Body' in request.values:
		dbgErr("no 'body' key in request")
		msg = "Please send the streetlight number to (206) 496-0852. (ERROR: no ['body'])"
		return render_template('sms_confirm.xml', msg=msg)
		
	pole_number = str(request.values['Body']).strip()
	dbgInfo('processing stripped pole number', pole_number)

	# check for 7 digits
	if not re.search(SMS_POLE_REGEXP, pole_number):
		dbgErr("pole number did not match regexp")
		msg = "Please supply the 7 digit pole number"
		return render_template('sms_confirm.xml', msg=msg)
	else:
		dbgInfo("polenumber matches regepx")

	msg = "Streetlight issue reported. Thank you!."
	return render_template('sms_confirm.xml', msg=msg)

@app.route('/submit', methods=['POST', 'GET'])
def submit():
	dbgInfo('request', request)
	HIGHLIGHT_COLOR = '\x1b[96;1m'
	HIGHLIGHT_END = '\x1b[0m'

	print HIGHLIGHT_COLOR + "RECEIVED: " + HIGHLIGHT_END + str(request.values)

	# SEND SMS
	if not 'From' in request.values:
		dbgWarn("no 'From' key in request. Not SMS - Not Replying")
		return render_args(request.values) + "<br>WARN: Not an SMS. Not replying"
	
	dbgInfo("FROM DETECTED. WILL TRY TO RESPOND", request.values)
	resp = "<small>"+ render_args(request.values) + "</small><br>"
	rcpt = request.values['From']
	resp += "<hr>RECIPIENT: " + rcpt + "<br>"
	dbgInfo('FROM', rcpt)
	
	"""		REST API TWILIO
	data = "From=%2B12067353590&To=" + rcpt + "&Body=Streetlight%20issue%20reported.%20Thank%20you%21"
	resp += "SUBMITTING API CALL with data: " + TWILIO_SEND_SMS_API + "?" + data + "<br>"

	req = urllib2.Request(TWILIO_SEND_SMS_API, data=data)
	req.add_header('authorization', 'Basic ' + base64.b64encode(TWILIO_SID) + ":" + base64.b64encode(TWILIO_AUTH_TOKEN))
	#req.add_header('Content-Type', 'application/x-www-form-urlencoded')
	"""

	resp += "<h3>Twilio Response:</h3>"

	""" REST API TWILIO
	try:
		resp += str(urllib2.urlopen(req).read())
	except Exception as e:
		dbgInfo("urlerror", e)
	"""

	# Download the Python helper library from twilio.com/docs/python/install
	from twilio.rest import TwilioRestClient
	from twilio import TwilioRestException
	# Your Account Sid and Auth Token from twilio.com/user/account
	account_sid = "ACf3f9ee7b4f7e932576ac40fbfbd2ef3c"
	auth_token = "{{ auth_token }}"
	msg = "Streetlight issue reported. Thanks for the message!."

	client = TwilioRestClient(TWILIO_SID, TWILIO_AUTH_TOKEN)
	message = None
	try:
		message = client.sms.messages.create(body=render_template('sms_confirm.xml', msg=msg),
		to="+19734195443",
		#from_="+12067353590")
		from_="+12064960852")
		resp += "TWILIO API MESSAGE: " + str(message) + "<br>"
	except TwilioRestException as e:
		dbgErr("TwilioException", e)
		resp += "<br><b>TwilioException</b>: " + str(e)

	if message and message.sid:
		resp += "<br>" + str(message.sid)
		dbgInfo("message.sid", message.sid)
	else:
		dbgInfo('message has no sid attribute', message)
		resp += "<br> message has no sid attribute"

	return resp


def clear_previous_sessions(userId):
	"""Clear values in json array string with specified userId"""
	sessions = json.loads(get_all_sessions())
	i = 0
	l = len(sessions)
	while i < l:
		if sessions[i]['userId'] == userId:
			del sessions[i]
			print "old session cleared"
			l = len(sessions) # adjust length
			
		i += 1

	return sessions

def write_all_sessions(sessions_object):
	try:
		f = open(SESSION_FILE, 'w')
		f.write( json.dumps(sessions_object) )
		f.close
	except Exception as e:
		print e

def get_all_sessions():
	if not os.access(SESSION_FILE, os.F_OK):	# if file doesn't exist
		print "session file doesn't exist. return empty array"
		return "[]"
	try:
		f = open(SESSION_FILE, 'r')
		json_sessions = string.join(f.readlines())
		f.close()
	except Exception as e:
		print e
	return json_sessions

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

