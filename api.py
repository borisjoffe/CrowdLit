#!/usr/bin/env python
import sys

from flask import Flask, render_template, url_for, request, redirect, session
app = Flask(__name__)
 
app.debug = False
brand = "CrowdLit"

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/home')
def home():
	return render_template('userpage.html')

def main():
    app.run(host='0.0.0.0')
    return 0

if __name__ == "__main__":
	sys.exit(main())

