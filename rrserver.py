import requests

import pprint

class RRServer(object):
	def __init__(self):
		self.ipAddr = None
	
	def SetServerAddress(self, ip, port):
		self.ipAddr = "http://%s:%s" % (ip, port)

	def SendRequest(self, req):
		pprint.pprint(req)

		for cmd, parms in req.items():
			r = requests.get(self.ipAddr + "/" + cmd, params=parms)

