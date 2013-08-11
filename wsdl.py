#!/usr/bin/env python

from pyws.server import SoapServer
from pyws.functions.register import register


server = SoapServer(
    service_name='Test',
    tns='http://example.com/',
    location='http://localhost:8000/api/',
)

@register()
def add_simple(a, b):
    return a + b


if __name__=="__main__":
	print "hello"
