# importing the module
import wikipedia
from flask import Flask, request, jsonify
from wikipedia.exceptions import DisambiguationError, PageError
import requests
import configparser
import phonenumbers
from phonenumbers import carrier

config = configparser.ConfigParser()
config.read('config.ini')

auth_id = config.get("keys", "authId")
url = config.get("cluster", "url")

def swob_cluster(isp, text, number):
	payload = {
		"auth_id": "{}".format(auth_id),
		"data": [{
			"isp": "{}".format(isp),
			"number": "{}".format(number),
			"text": "{}".format(text)
			}]
		}
	try:
		requests.post("{}/sms".format(url), json = payload)
	except Exception as e:
		print("Cluster error:")
		print(str(e))
		raise

def isp_finder(number):		
	number_ro = phonenumbers.parse(number, None)
	number_carrier = carrier.name_for_number(number_ro, "en")
	return(number_carrier.split()[0].lower())

app = Flask(__name__)

@app.route('/income', methods=['POST'])
def in_data():
	try:
		data = request.json
		text = data["text"]
		number = data["phonenumber"]
		result = wikipedia.summary("({})".format(text), sentences=1)
		carrier = isp_finder("{}".format(number))
		print("--> Sending result to {}".format(number))
		swob_cluster(carrier, result, number)
		return "Online routing successful", 200
	except DisambiguationError as e:
		DisambiguationError_msg = "{}: Please be more specific about '{}'".format(e.__class__.__name__, text)
		print("--> error: {}". format(e.__class__.__name__))
		print("--> Sending error to {}". format(number))
		swob_cluster(carrier, DisambiguationError_msg, number)
		return str(e.__class__.__name__), 500
	except PageError as e:
		PageError_msg = "'{}' has no matching article".format(e.__class__.__name__, text)
		print("--> error: {}". format(e.__class__.__name__))
		print("--> Sending error to {}". format(number))
		swob_cluster(carrier, PageError_msg, number)
		return str(e.__class__.__name__), 500

if __name__ == '__main__':
   app.run(host="localhost", port=9000, debug=True)

