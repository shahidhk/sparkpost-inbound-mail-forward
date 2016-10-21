from flask import Flask, request, jsonify
import requests
import json
app = Flask(__name__)

AUTH_TOKEN = os.getenv('AUTH_TOKEN', '')
SPARKPOST_API_KEY = os.getenv('SPARKPOST_API_KEY', '')
SPARKPOST_API = "https://api.sparkpost.com/api/v1/transmissions?num_rcpt_errors=3"

SPARKPOST_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': SPARKPOST_API_KEY
}

@app.route("/hello")
def hello():
    return "Hello World from Flask"

@app.route("/sparkpost-handler", methods=["POST"])
def handle_email()
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
          "address": "thewebopsclubiitm@gmail.com"
        }
      ],
      "content": {
        "from": "inbound-forward@108hackathon.in",
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
    	print "\n>>>>>>>> FORWARDING DATA"
	print forward_data
	print "\n>>>>>>>> CALLING SPARKPOST"
	resp = requests.post(SPARKPOST_API, headers=SPARKPOST_HEADERS, data=json.dumps(forward_data))
	print "\n>>>>>>>> SPARKPOST RESPONSE"
	print resp
	return 'ok'
    except Exception, e:
        print "\n>>>>>>>> EXCEPTION"
        print e
        return 'not ok'

    return 'not ok'

#@app.route("/aa", methods=["POST"])
#def subject_access_review():
#    data = request.get_json()
#    response = {
#        "apiVersion": "authorization.k8s.io/v1beta1",
#        "kind": "SubjectAccessReview",
#        "status": {
#            "allowed": True
#        }    
#    }
#    print ">>>> REQUEST:"
#    print data
#    if data:
#        authorized, reason = namespace_service_account_authz(data)
#        if authorized:
#            return jsonify(response)
#        else:
#            response['status']['reason'] = reason
#    response['status']['allowed'] = False
#    print ">>>> RESPONSE:"
#    print response
#    print ""
#    return jsonify(response)
#
#def namespace_service_account_authz(data):
#    """
#    data:
#    {
#      "apiVersion": "authorization.k8s.io/v1beta1",
#      "kind": "SubjectAccessReview",
#      "spec": {
#	"resourceAttributes": {
#	  "namespace": "kittensandponies",
#	  "verb": "GET",
#	  "group": "*",
#	  "resource": "pods"
#	},
#	"user": "jane",
#	"group": [
#	  "group1",
#	  "group2"
#	]
#      }
#    }
#    
#    username format `system:serviceaccount:<namespace>:default`
#    for valid action, user(namespace) == resourceAttributes.namespace	
#    
#    response:
#    {
#      "apiVersion": "authorization.k8s.io/v1beta1",
#      "kind": "SubjectAccessReview",
#      "status": {
#	"allowed": true
#      }
#    }
#    {
#      "apiVersion": "authorization.k8s.io/v1beta1",
#      "kind": "SubjectAccessReview",
#      "status": {
#	"allowed": false,
#	"reason": "user does not have read access to the namespace"
#      }
#    }
#    """
#    if 'resourceAttributes' and 'user' in data['spec'].keys():
#        user = data['spec']['user']
#        resource_namespace = data['spec']['resourceAttributes']['namespace']
#        
#        user_split = user.split(':')
#        if len(user_split) == 4:
#            user_namespace = user_split[2]
#            if user_namespace == resource_namespace:
#                return True, 'authorized'
#            else:
#                return False, 'user not allowed to access ' + resource_namespace
#    return False, 'un-recognizable request'


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
