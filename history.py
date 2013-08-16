#!/usr/bin/env python

import sys
import os
from datetime import datetime
import json
import random

import users
from utils import *

DATE_FORMAT = "%c"

class History(object):
	HISTORY_FILE = None
	USER_IS_SET = False
	userId = None

	def __init__(self, sessionId='000'):
		if sessionId == '000': 	# special test case
			self.userId = 'testuser'
			self.HISTORY_FILE = os.path.join(os.getcwd(), 'history.dat')
			self.USER_IS_SET = True
		else:
			self.userId = users.get_logged_in_user(sessionId)	
			if self.userId: 	# wrong or non-existent sessionId
				self.HISTORY_FILE = os.path.join(os.getcwd(), self.userId + 'history.dat')
				self.USER_IS_SET = True

	def add_history(self, pole_number, address):
		pole_number = str(pole_number)
		if self.check_for_pole_duplicate(pole_number):
			return '{}'
		today = datetime.today().strftime(DATE_FORMAT)
		new_event = { 'date': today, 'pole_number': str(pole_number), 'address': address }
		all_history = json.loads(self.get_all_history())
		all_history.append(new_event)
		if self.write_all_history(all_history):
			return json.dumps(new_event)
		else:
			return None

	def check_for_pole_duplicate(self, pole_number):
		all_history = json.loads(self.get_all_history())
		l = len(all_history)
		for i in range(l):
			if all_history[i]['pole_number'] == pole_number:
				dbgInfo("Found duplicate", pole_number)
				return True

	def clear_history(self):
		if not os.access(self.HISTORY_FILE, os.F_OK):	# if file doesn't exist
			dbgErr("Cannot delete file because it doesn't exist", self.HISTORY_FILE)
			return False
		os.remove(self.HISTORY_FILE)
		return True

	def get_last_history(self):
		all_history = json.loads(self.get_all_history())
		l = len(all_history)
		if l < 1: return '{}'
		min_item = all_history[0]
		min_date = min_item['date']
		i = 1

		while i < l:
			if datetime.strptime(min_date, DATE_FORMAT) > datetime.strptime(all_history[i]['date'], DATE_FORMAT):
				min_item = all_history[i]
				min_date = min_item['date']
			i += 1
		
		return json.dumps(min_item)

	def write_all_history(self, history_object):
		if not self.USER_IS_SET:
			dbgErr('provide sessionId to set user')
			return
		try:
			f = open(self.HISTORY_FILE, 'w')
			f.write( json.dumps(history_object) )
			f.close
		except Exception as e:
			print e

	def get_all_history(self):
		if not self.USER_IS_SET:
			dbgErr('provide sessionId to set user')
			return '[]'
		if not os.access(self.HISTORY_FILE, os.F_OK):	# if file doesn't exist
			dbgInfo("history file doesn't exist. return empty array")
			return "[]"
		try:
			f = open(self.HISTORY_FILE, 'r')
			json_history = f.read()
			f.close()
		except Exception as e:
			print e
		return json_history

def main():
	u = History('000');

	a("old history", u.get_all_history())
	a("last item", u.get_last_history())

	u.clear_history()
	a("cleared", u.get_all_history())

	u.add_history(newnum(), newaddr())
	u.add_history(newnum(), newaddr())
	u.add_history(newnum(), newaddr())
	a("3 added", u.get_all_history())
	a("last item", get_last_history())

	u.add_history(newnum(), newaddr())
	a("one MORE added (4 total)", u.get_all_history())

	u.clear_history()
	a("cleared (0)", u.get_all_history())
	a("last item", u.get_last_history())

	u.add_history(newnum(), newaddr())
	a("one added (1)", u.get_all_history())
	a("last item", u.get_last_history())

	u.clear_history()
	a("cleared", u.get_all_history())

	return 0

def newnum():
	return random.randint(1000000, 9999999)

def newaddr():
	return str(random.randint(10, 9999)) + ' Fake St'

a = dbgInfo

if __name__=="__main__":
	sys.exit(main())	
