#!/usr/bin/env python
import sys
import os
import urllib
import urllib2
from flask import Flask, render_template, url_for, request, redirect, session

import streetlight_form
import sms
import users
from utils import *
 
app = Flask(__name__)
if os.getlogin() == "boris":
	app.debug = True	# local account - debug
else:
	app.debug = False	# aws/heroku account - no debug
brand = "CrowdLit"

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

@app.route('/submit', methods=['POST', 'GET'])
def submit():
	dbgInfo('request', request)
	HIGHLIGHT_COLOR = '\x1b[96;1m'
	HIGHLIGHT_END = '\x1b[0m'

	print HIGHLIGHT_COLOR + "RECEIVED: " + HIGHLIGHT_END + str(request.values)

	if not 'From' in request.values:
		dbgWarn("no 'From' key in request. Not SMS - Not Replying")
		return render_args(request.values) + "<br>WARN: Not an SMS. Not replying"
	
	# SEND SMS
	dbgInfo("FROM DETECTED. WILL TRY TO RESPOND", request.values)
	resp = "<small>"+ render_args(request.values) + "</small><br>"
	rcpt = request.values['From']
	resp += "<hr>RECIPIENT: " + rcpt + "<br>"
	dbgInfo('FROM', rcpt)
	resp += "<h3>Twilio Response:</h3>"
	
	"""		REST API TWILIO
	data = "From=%2B12067353590&To=" + rcpt + "&Body=Streetlight%20issue%20reported.%20Thank%20you%21"
	resp += "SUBMITTING API CALL with data: " + TWILIO_SEND_SMS_API + "?" + data + "<br>"

	req = urllib2.Request(TWILIO_SEND_SMS_API, data=data)
	req.add_header('authorization', 'Basic ' + base64.b64encode(TWILIO_SID) + ":" + base64.b64encode(TWILIO_AUTH_TOKEN))
	#req.add_header('Content-Type', 'application/x-www-form-urlencoded')

	try:
		resp += str(urllib2.urlopen(req).read())
	except Exception as e:
		dbgInfo("urlerror", e)
	"""
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

