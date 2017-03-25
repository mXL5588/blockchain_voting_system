from django import template
from django.template.defaultfilters import stringfilter
import datetime

import json
import requests
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse


register = template.Library()

@register.filter
@stringfilter
def lower(value):
    return value.lower()

@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)

@register.simple_tag
def test():
	now = 'test 123'
	
	return now

@register.simple_tag
def getCounterpartyInfo():
	url = "http://localhost:14000/api/"
	headers = {'content-type': 'application/json'}
	auth = HTTPBasicAuth('rpc', 'sweng')

	payload = {
	  "method": "get_running_info",
	  "params": {},
	  "jsonrpc": "2.0",
	  "id": 0
	}
	node=json.dumps(payload)
	

	#response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
	response = requests.post(url, data=node, headers=headers, auth=auth)
	return (response.text)

@register.simple_tag
def getBallotCandidateBalance(candidateAddress):
# Fetch all balances for all assets for both of two addresses, using keyword-based arguments
	url = "http://localhost:14000/api/"
	headers = {'content-type': 'application/json'}
	auth = HTTPBasicAuth('rpc', 'sweng')

	payload = {
	  "method": "get_balances",
	  "params": {"filters": [{"field": "address", "op": "==", "value": candidateAddress}],
                      "filterop": "or"
                      },
	  "jsonrpc": "2.0",
	  "id": 0
	}
	node=json.dumps(payload)
	response = requests.post(url, data=node, headers=headers, auth=auth)
	return (response.text)

@register.simple_tag
def castBallot(strSourceAddress, strCandidateAddress, strAssetName):
# Send 1 XCP (specified in satoshis) from one address to another.
    url = "http://localhost:14000/api/"
    headers = {'content-type': 'application/json'}
    auth = HTTPBasicAuth('rpc', 'sweng')

    payload = {
	  "method": "get_balances",
	  "params": {
	  				"source": userSourceAddress,
                    "destination": candidateAddress,
                    "asset": assetName,
                    "quantity": 100000000
                      },
	  "jsonrpc": "2.0",
	  "id": 0
	}
    node=json.dumps(payload)
    response = requests.post(url, data=node, headers=headers, auth=auth)
    return (response.text)


