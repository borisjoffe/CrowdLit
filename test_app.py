#!/usr/bin/env python

import unittest
import api

class SOAPTestCase(unittest.TestCase):

	def setUp(self):
		self.app = api.app.test_client()
		#self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
		#flaskr.init_db()

	def tearDown(self):
		pass
		#os.close(self.db_fd)
		#os.unlink(flaskr.app.config['DATABASE'])

	def test_empty_db(self):
		request = """<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <add_simple xmlns="http://www.example.org/">
      <a>hello </a>
      <b>world</b>
    </add_simple>
  </soap:Body>
</soap:Envelope>"""
		rv = self.app.post('/submit', data=request)
		print rv.data


if __name__ == '__main__':
	unittest.main()
