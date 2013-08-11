#!/usr/bin/env python

import sys
import os
import urllib, urlparse		# is this necessary
import urllib2

SEATTLE_STREETLIGHT_URL = "http://www.seattle.gov/light/streetlight/form.asp"
#SEATTLE_STREETLIGHT_URL = "http://127.0.0.1:5000/submit"

test_post_request = "LastName=Joffe&Phone=1-973-419-5443&PhoneExtension=&Email=seattle-street-light@joff3.com&PoleNumber=1313189&StreetNumber=Jackson%20St%20%26%202nd%20Ave%20S&ProblemType=Out&ProblemDescription=Submitted%20via%20CrowdLit&SubmitForm=Submit+Trouble+Report"
test_string = (("LastName", "mylastname"), ("Phone", "206-111-555"))

outputfile = os.path.join(os.getcwd(), "streetlight_response.html")

def build_string():
	return test_post_request
	#return urllib.urlencode(test_string)
	# urlparse.parse_qs() 		# parse post query string into dictionary

def submit_to_seattle_streetlight():
	req = urllib2.Request(url=SEATTLE_STREETLIGHT_URL,
		data=build_string())
	print "REQUEST: " + build_string() + " to: " + SEATTLE_STREETLIGHT_URL + "\n"
	try:
		out = urllib2.urlopen(req)
	except Exception as e:
		print e

	f = open(outputfile, 'w')
	f.write(out.read())	
	f.close()
	print "Wrote to file://" + outputfile

	return "DONE"

def main():
	print submit_to_seattle_streetlight()

if __name__ == "__main__":
	sys.exit(main())
