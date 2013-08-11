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
	return render_template('submitlight.html')

def main():
	port = int(os.environ.get('PORT', 5000))	# for heroku
	app.run(host='0.0.0.0', port=port)
	return 0

if __name__ == "__main__":
	sys.exit(main())

