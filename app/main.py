from flask import Flask, request, jsonify
import requests
import json
import os
app = Flask(__name__)

AUTH_TOKEN = os.getenv('AUTH_TOKEN', '')
SPARKPOST_API_KEY = os.getenv('SPARKPOST_API_KEY', '')
SPARKPOST_API = "https://api.sparkpost.com/api/v1/transmissions?num_rcpt_errors=3"
FORWARD_EMAIL = os.getenv('FORWARD_EMAIL', 'email@example.com')
FROM_EMAIL = os.getenv('FROM_EMAIL', 'inbound-forward@example.com')

SPARKPOST_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': SPARKPOST_API_KEY
}

@app.route("/hello")
def hello():
    return "Hello World from Flask"

@app.route("/sparkpost-handler", methods=["POST"])
def handle_email():
    auth = request.headers.get('X-MessageSystems-Webhook-Token')
    if auth != AUTH_TOKEN:
        return 'not ok'
    data = request.get_json()
    print "\n>>>>>>>> INCOMING DATA"
    print data
    forward_data = {
      "options": {
  	"transactional": True,
	"inline_css": True
      },
      "recipients": [
        {
          "address": FORWARD_EMAIL
        }
      ],
      "content": {
        "from": {
            "name":"",
            "email": FROM_EMAIL
            },
    	"reply_to": "",
        "subject": "",
        "html": ""
      }
    }

    try:
        email = data[0]['msys']['relay_message']
	content = email['content']
	forward_data['content']['html'] = content['html']
	forward_data['content']['text'] = content['text']
	forward_data['content']['subject'] = content['subject']
	forward_data['content']['reply_to'] = email['msg_from']
	forward_data['content']['from']['name'] = email['msg_from']
    	print "\n>>>>>>>> FORWARDING DATA"
	print forward_data
	print "\n>>>>>>>> CALLING SPARKPOST"
	resp = requests.post(SPARKPOST_API, headers=SPARKPOST_HEADERS, data=json.dumps(forward_data))
	print "\n>>>>>>>> SPARKPOST RESPONSE"
	print resp.json()
	return 'ok'
    except Exception, e:
        print "\n>>>>>>>> EXCEPTION"
        print e
        return 'not ok'

    return 'not ok'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8080)
