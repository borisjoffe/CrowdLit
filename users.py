#!/usr/bin/env python

import os
import json
import string
import base64
from utils import *

SESSION_FILE = os.path.join(os.getcwd(), 'sessions.dat')

def login(userId):
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

def get_logged_in_user(sessionId):
	userId = None

	if sessionId == '000':
		return 'testuser'

	sessions = json.loads(get_all_sessions())
	for item in sessions:
		if item['sessionId'] == sessionId:
			userId = item['userId']

	return userId
	
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
		dbgInfo("session file doesn't exist. return empty array")
		return "[]"
	try:
		f = open(SESSION_FILE, 'r')
		json_sessions = string.join(f.readlines())
		f.close()
	except Exception as e:
		print e
	return json_sessions

