# Script to list all organizations in DivvyCloudf

import json
import requests
import getpass

requests.packages.urllib3.disable_warnings() # verify=False throws warnings otherwise

# USER INFO:
users_to_add = [
    { "email": "youremail@rapid7.com", "name": "First Lastnamerson", "username": "flast" }
]

# Username/password to authenticate against the API
username = ""
password = "" # Leave this blank if you don't want it in plaintext and it'll prompt you to input it when running the script. 

# API URL
base_url = ""

# Param validation
if not username:
    username = input("Username: ")

if not password:
    passwd = getpass.getpass('Password:')
else:
    passwd = password

if not base_url:
    base_url = input("Base URL (EX: http://localhost:8001 or http://45.59.252.4:8001): ")

# Full URL
login_url = base_url + '/v2/public/user/login'

# Shorthand helper function
def get_auth_token():
    response = requests.post(
        url=login_url,
        verify=False,
        data=json.dumps({"username": username, "password": passwd}),
        headers={
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json'
        })
    return response.json()['session_id']

auth_token = get_auth_token()

headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'application/json',
    'X-Auth-Token': auth_token
}

def add_user(user):
    data = {
        "authentication_type": "saml",
        "access_level": "ORGANIZATION_ADMIN",
        "authentication_server_id": 3,
        "authentication_type": "saml",
        "email": user['email'],
        "name": user['name'],
        "username": user['username']
    }

    response = requests.post(
        url=base_url + '/v2/public/user/create',
        data=json.dumps(data),
        verify=False,
        headers=headers
        )
    return response.json()    

## Add users
for user in users_to_add:
    try:
        new_user_output = add_user(user)
        print("User created: " + new_user_output['username'])
    except Exception as e:
        print("unexpected error with user: " + user['email'])
        print (e)
