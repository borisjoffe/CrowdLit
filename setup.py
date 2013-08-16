#!/usr/bin/python
import os, sys

config_filename = 'config.py'
options = { 'api_key' : 'Paste Twilio API Key (from https://www.twilio.com/user/account)',
			'twilio_sender': 'Paste Twilio number here (in the format +18001115555)',
			'default_recipient': 'Paste your phone number here (in the format +18001115555)' }

def main():
	if os.access(config_filename, os.F_OK):	# if file exists
		print "A configuration file already exists." 
		c = raw_input("Are you sure you want to overwrite this? (type yes to override): ")
		if c != "yes":
			print "Exited without writing to config file."
			return

	f = open(config_filename, 'w')

	for option in options:
		myvalue = raw_input(options[option] + ': ')
		f.write(option + ' = "' + myvalue + '"\n')

	f.close()

if __name__ == "__main__":
	sys.exit(main())
