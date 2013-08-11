#!/usr/bin/env python
import sys
import os
from flask import Flask, render_template, url_for, request, redirect, session

import streetlight_form
 
app = Flask(__name__)
app.debug = False
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

@app.route('/submit', methods=['POST', 'GET'])
def submit():
	HIGHLIGHT_COLOR = '\x1b[96;1m'
	HIGHLIGHT_END = '\x1b[0m'

	print HIGHLIGHT_COLOR + "RECEIVED: " + HIGHLIGHT_END + str(request.values)
	s = "<h3>REQUEST PARAMS</h3>"
	for item in request.values:
		s += item + " = " + request.values[item] + "<br>"
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

