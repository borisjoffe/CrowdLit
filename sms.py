#!/usr/bin/env python

import re
from flask import render_template
from twilio.rest import TwilioRestClient
from twilio import TwilioRestException
from utils import *

TWILIO_AUTH_TOKEN = "0d793a4c38362e49f51b19e3c3ca7ea9"
TWILIO_SID = "ACf3f9ee7b4f7e932576ac40fbfbd2ef3c"
TWILIO_API = "https://api.twilio.com/2010-04-01/"
TWILIO_SEND_SMS_API = TWILIO_API + "Accounts/" + TWILIO_SID + "/SMS/Messages.json"

SMS_POLE_REGEXP = '\d{7}'

def send_sms(sender="+12064960852", recipient="+19734195443", text="Streetlight issue reported."):
	# Download the Python helper library from twilio.com/docs/python/install
	# Your Account Sid and Auth Token from twilio.com/user/account

	client = TwilioRestClient(TWILIO_SID, TWILIO_AUTH_TOKEN)
	message = None
	try:
		message = client.sms.messages.create(body=text,
		to=recipient,
		#from_="+12067353590")
		from_=sender)
		dbgInfo("TWILIO API MESSAGE", message)
	except TwilioRestException as e:
		dbgErr("TwilioException", e)

	if message and message.sid:
		dbgInfo("message.sid", message.sid)
		return message.sid
	else:
		dbgInfo('message has no sid attribute', message)
		return None

def process_sms_message(args):
	"""Return template for smsreply - Messaging Request URL"""
	dbgInfo("/smsreply args", args)

	# Check for body attribute
	if not 'Body' in args:
		dbgErr("no 'body' key in request")
		msg = "Please send the streetlight number to (206) 496-0852. (ERROR: no ['body'])"
		return render_template('sms_confirm.xml', msg=msg)
	
	if verify_pole_number(args['Body'])
		msg = "Streetlight issue reported. Thank you!."
		return render_template('sms_confirm.xml', msg=msg)
	else:
		return render_template('sms_confirm.xml', msg=msg)

def verify_pole_number(pole_number):
	pole_number = str(pole_number).strip()
	dbgInfo('processing stripped pole number', pole_number)

	# check for 7 digits
	if not re.search(SMS_POLE_REGEXP, pole_number):
		dbgErr("pole number did not match regexp")
		msg = "Please supply the 7 digit pole number"
		return False
	else:
		dbgInfo("polenumber matches regepx")
		return True



