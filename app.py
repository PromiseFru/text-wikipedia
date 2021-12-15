# importing the module
import wikipedia
from flask import Flask, request, jsonify
import json
from wikipedia.exceptions import DisambiguationError, PageError
import requests
import configparser
import phonenumbers
from phonenumbers import carrier

config = configparser.ConfigParser()
config.read('config.ini')

auth_id = config.get("keys", "authId")
url = config.get("cluster", "url")

class swob_cluster:
	def __init__(self, isp, text, number):
		self.isp = isp
		self.text = text
		self.number = number
	
	def __repr__(self):
		payload = {
			"auth_id": "{}".format(auth_id),
			"data": [{
				"isp": "{}".format(self.isp),
				"number": "{}".format(self.number),
				"text": "{}".format(self.text)}
				]}
		try:
			print("--> Sending result to {}".format(self.number))
			requests.post("{}/sms".format(url), json = payload)
			return True
		except Exception as e:
			print("Cluster error:")
			print(str(e))

class isp_finder:
	def __init__(self, number):
		self.number = number
		
	def __repr__(self):
		number_ro = phonenumbers.parse(self.number, None)
		number_carrier = carrier.name_for_number(number_ro, "en")
		return(number_carrier.split()[0].lower())

#app = Flask(__name__)
#
#@app.route('/income', methods=['POST'])
#def in_data():
#    try:
#        data = request.json
#        text = data["text"]
#        number = data["phonenumber"]
#        result = wikipedia.summary("({})".format(text), sentences=1)
#        payload = {
#            "auth_id":"04de485a26e2b2ba682b44e55e249d16a326001c4abff244a1b4ec30d7d3599f",
#	        "data":[{
#		        "isp":"mtn",
#		        "number":"{}".format(number),
#		        "text":"{}".format(result)
#            }]
#        }
#        print("--> Sending result to {}". format(number))
#        requests.post("http://smswithoutborders.com:15673/sms", json = payload)
#        return {}, 200
#    except DisambiguationError as e:
#        error = {
#            "auth_id":"04de485a26e2b2ba682b44e55e249d16a326001c4abff244a1b4ec30d7d3599f",
#	        "data":[{
#		        "isp":"mtn",
#		        "number":"{}".format(number),
#		        "text":"{}: Please be more specific about '{}'".format(e.__class__.__name__, text)
#            }]
#        }
#        print("--> error: {}". format(e.__class__.__name__))
#        print("--> Sending error to {}". format(number))
#        requests.post("http://smswithoutborders.com:15673/sms", json = error)
#        return str(e.__class__.__name__), 500
#    except PageError as e:
#        error = {
#            "auth_id":"04de485a26e2b2ba682b44e55e249d16a326001c4abff244a1b4ec30d7d3599f",
#	        "data":[{
#		        "isp":"mtn",
#		        "number":"{}".format(number),
#		        "text":"{}: '{}' has no matching article".format(e.__class__.__name__, text)
#            }]
#        }
#        print("--> error: {}". format(e.__class__.__name__))
#        print("--> Sending error to {}". format(number))
#        requests.post("http://smswithoutborders.com:15673/sms", json = error)
#        return str(e.__class__.__name__), 500
#
#if __name__ == '__main__':
#    app.run(host="localhost", port=9000, debug=True)

