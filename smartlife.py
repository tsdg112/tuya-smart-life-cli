#!/usr/bin/python

# Smart Life on/off/devlist

# usage: smartlife.py
# usage: smartlife.py [-v] on|off device_id

import requests
import pprint
import time
import os
import sys
import stat
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description='smartlife controller')
parser.add_argument('-v', action="store_true", dest='verbose')
parser.add_argument('-d', action="store_true", dest='debug')
parser.add_argument('command', type=str, default='', nargs='?')
parser.add_argument('id', type=str, default='', nargs='?')
args = parser.parse_args()

command = args.command
id = args.id
debug = args.debug

if args.verbose:
	print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+':', "smartlife", command, id)

auth_file = "/tmp/smartlife_auth";
max_age = 864000 - 300
refresh_age = 86400/2

try:
	age = time.time() - os.stat(auth_file)[stat.ST_MTIME]
except:
	age = max_age

if age < refresh_age:
	access_token = open(auth_file, 'r').readline().strip()
	if debug:
		print("DEBUG: reuse", access_token)
elif age < max_age:
	f = open(auth_file, 'r')
	access_token = f.readline().strip()
	refresh_token = f.readline().strip()
	if debug:
		print("DEBUG: refresh", refresh_token)
	response = requests.get("https://px1.tuyaus.com/homeassistant/access.do?grant_type=refresh_token&refresh_token=" + refresh_token).json()
	try:
		access_token = response["access_token"]
		refresh_token = response["refresh_token"]
		open(auth_file, 'w').write(access_token + "\n" + refresh_token  + "\n")
	except:
		print("auth.do failed")
		pprint.pprint(auth)
		sys.exit(1)
else:
	if debug:
		print("DEBUG: renew")
	response = requests.post(
	    "https://px1.tuyaus.com/homeassistant/auth.do",
	    data={
	        "userName": "person@example.com",
	        "password": "123456",
	        "countryCode": "1",
	        "bizType": "smart_life",
	        "from": "tuya",
	    },
	).json()
	try:
		access_token = response["access_token"]
		refresh_token = response["refresh_token"]
		open(auth_file, 'w').write(access_token + "\n" + refresh_token  + "\n")
	except:
		print("auth.do failed")
		pprint.pprint(auth)
		sys.exit(1)

if command == 'on':
	value = "1"
elif command == 'off':
	value = "0"
else:
	devices = requests.post(
	    "https://px1.tuyaus.com/homeassistant/skill",
	    json={"header": {"name": "Discovery", "namespace": "discovery", "payloadVersion": 1}, "payload": {"accessToken": access_token}}
	).json()
	pprint.pprint(devices)
	sys.exit(0)

response = requests.post(
    "https://px1.tuyaus.com/homeassistant/skill",
    json={"header": {"name": "turnOnOff", "namespace": "control", "payloadVersion": 1}, "payload": {"accessToken": access_token, "devId": id, "value":value}}
).json()

if response["header"]["code"] != 'SUCCESS':
	print("smartlife: error:", response["header"]["code"])
elif args.verbose:
	# print("smartlife: return:", response["header"]["code"])
	pass

# references:
# https://github.com/PaulAnnekov/tuyaha
# https://www.reddit.com/r/smartlife/comments/gj5ixd/smart_life_web_interface/
# https://github.com/ndg63276/smartlife/blob/master/functions.js
