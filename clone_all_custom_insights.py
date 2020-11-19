# Script to create a "best practices pack" and add insights to it
# Update packaged_insight_ids with the IDs of existing insights. 
# Add new filters to the insight_configs array

# How to run:
# This can be ran from any system that has access to the DivvyCloud instance (including the one that's running Divvy)
# sudo pip3 install requests
# curl -o create_best_practices_pack.py https://raw.githubusercontent.com/alpalwal/Divvy/master/Prod/scripts/Create%20Pack/create_poc_cost_optimization_pack.py
# python3 create_best_practices_pack.py

import json
import requests
import getpass


######### Prod ENV

# Username/password to authenticate against the API
username = ""
password = "" # Leave this blank if you don't want it in plaintext and it'll prompt you to input it when running the script. 

# API URL
base_url = "https://sales-demo.divvycloud.com"

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


# list all insights
def list_insights():
    data = {}
    response = requests.get(
        url=base_url + '/v2/public/insights/list',
        data=json.dumps(data),
        headers=headers
        )
    return response.json()    


# Create a custom insight
def create_insight(insight_config):
    response = requests.post(
        url=base_url + '/v2/public/insights/create',
        data=json.dumps(insight_config),
        headers=headers
        )
    return response.json()        


# Add notes to insight
def add_insight_notes(insight_id,description):
    data = {
        "notes": description
    }

    response = requests.post(
        url=base_url + '/v2/public/insights/' + str(insight_id) + '/notes/update',
        data=json.dumps(data),
        headers=headers
        )
    return response
# No response expected   

print("Generating list of custom insights")
all_insights = list_insights()
custom_insights = []
for insight in all_insights:
    if insight["source"] == "custom":
        #Clean up unneeded params
        insight['name'] = "TESTTTTTTTT"
        del insight['by_cloud'] 
        del insight['by_resource_group'] 
        del insight['insight_id']
        del insight['owner_resource_id']
        del insight['organization_id']
        del insight['resource_group_blacklist']
        del insight['updated_at']
        del insight['tags']
        del insight['user_resource_id']
        del insight['source']
        del insight['results']
        del insight['total']
        del insight['exemptions']
        del insight['duration']
        del insight['author']
        del insight['version']
        del insight['bots']        
        custom_insights.append(insight)
  


print("Adding insights to new environment")

# Username/password to authenticate against the API
username = ""
password = "" # Leave this blank if you don't want it in plaintext and it'll prompt you to input it when running the script. 

# API URL
base_url = "https://sales-preview.divvycloud.com"

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


print("Creating custom insights")
# Loop through insight_configs and add a filter for each
custom_insight_ids = []
for insight in custom_insights:
    print("Creating new insight: " + insight['name'])
    new_insight_info = create_insight(insight)
    custom_insight_ids.append(new_insight_info['insight_id'])

    # Add notes to the insight
    add_insight_notes(new_insight_info['insight_id'],insight['description'])  
    break
