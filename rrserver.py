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
			print("(%s)" % cmd)
			print("(%s)" % str(parms))
			try:
				r = requests.get(self.ipAddr + "/" + cmd, params=parms)
			except requests.exceptions.ConnectionError:
				print("Unable to send request  is dispatcher running?")

