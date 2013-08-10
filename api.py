#!/usr/bin/env python
import sys

from flask import Flask, render_template, url_for, request, redirect, session, g
app = Flask(__name__)
 
app.debug = False
brand = "CrowdLit"

@app.route('/')
def index():
	return render_template('home.html', brand=brand)

@app.route('/home')
def index():
	return render_template('userpage.html', brand=brand)


def main():
    app.run('0.0.0.0')
    return 0

if __name__ == "__main__":
	sys.exit(main())

