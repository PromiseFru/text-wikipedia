# importing the module
import wikipedia
from flask import Flask, request, jsonify
from wikipedia.exceptions import DisambiguationError, PageError
import requests

app = Flask(__name__)

@app.route('/income', methods=['POST']) 
def in_data():
    try:
        data = request.json
        text = data["text"]
        number = data["phonenumber"]
        result = wikipedia.summary("({})".format(text), sentences=1)
        payload = {
            "auth_id":"",
	        "data":[{
		        "isp":"mtn",
		        "number":"{}".format(number),
		        "text":"{}".format(result)
            }]
        }
        print("--> Sending result to {}". format(number))
        requests.post("", json = payload)
        return {}, 200
    except DisambiguationError as e:
        error = {
            "auth_id":"",
	        "data":[{
		        "isp":"mtn",
		        "number":"{}".format(number),
		        "text":"{}: Please be more specific about '{}'".format(e.__class__.__name__, text)
            }]
        }
        print("--> error: {}". format(e.__class__.__name__))
        print("--> Sending error to {}". format(number))
        requests.post("", json = error)
        return str(e.__class__.__name__), 500
    except PageError as e:
        error = {
            "auth_id":"",
	        "data":[{
		        "isp":"mtn",
		        "number":"{}".format(number),
		        "text":"{}: '{}' has no matching article".format(e.__class__.__name__, text)
            }]
        }
        print("--> error: {}". format(e.__class__.__name__))
        print("--> Sending error to {}". format(number))
        requests.post("", json = error)
        return str(e.__class__.__name__), 500

if __name__ == '__main__':
    app.run(host="localhost", port=9000, debug=True)