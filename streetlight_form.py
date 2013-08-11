#!/usr/bin/env python

import sys
import os
import urllib, urlparse		# is this necessary

SEATTLE_STREETLIGHT_URL = "http://www.seattle.gov/light/streetlight/form.asp"

test_string = (("LastName", "mylastname"), ("Phone", "206-111-555"))

def build_string():
	return urllib.urlencode(test_string)
	# urlparse.parse_qs() 		# parse post query string into dictionary

def submit_to_seattle_streetlight():
	return SEATTLE_STREETLIGHT_URL

def main():
	print build_string()

if __name__ == "__main__":
	sys.exit(main())
