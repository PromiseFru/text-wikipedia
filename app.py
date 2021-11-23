# importing the module
import wikipedia
from flask import Flask, request, jsonify
from wikipedia.exceptions import DisambiguationError
import requests

app = Flask(__name__)

@app.route('/income', methods=['POST']) 
def in_data():
    try:
        data = request.json
        text = data["text"]
        number = data["phonenumber"]
        result = wikipedia.summary("{}".format(text), sentences=1)
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
    except DisambiguationError as err:
        print(err)

if __name__ == '__main__':
    app.run(host="localhost", port=9000, debug=True)