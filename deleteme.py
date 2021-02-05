# Script to list all pre-canned insights by cloud. 
# Sample output:
# ================================================================
# ===========================AWS==================================
# ================================================================
# Cloud Account Without Global API Accounting Config
# Instance Has Ephemeral Public IP
# Database Instance Retention Policy Too Low
# Load Balancer Cross Zone Balancing Disabled
# Load Balancer Connection Draining Disabled

import json
import requests
import getpass

requests.packages.urllib3.disable_warnings() # verify=False throws warnings otherwise

# Username/password to authenticate against the API
username = "alexc"
passwd = "xTm=cT8r+AvjwjhFT" # Leave this blank if you don't want it in plaintext and it'll prompt you to input it when running the script. 

# API URL
base_url = "https://sales-demo.divvycloud.com"

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

# Get Org info
def get_insights():
    data = {}

    response = requests.get(
        url=base_url + '/v2/public/insights/list',
        data=json.dumps(data),
        verify=False,
        headers=headers
        )
    return response.json()    

# get the insights
insight_info_array = get_insights()


for insight in insight_info_array:
    if insight['source'] == 'backoffice':
        print( str(insight['insight_id']) + " || " + insight['name'])
