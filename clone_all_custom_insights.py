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

# Username/password to authenticate against the API
old_env_username = ""
old_env_password = "" # Leave this blank if you don't want it in plaintext and it'll prompt you to input it when running the script. 
new_env_username = ""
new_env_password = "" # Leave this blank if you don't want it in plaintext and it'll prompt you to input it when running the script. 

# API URLs
old_env_base_url = ""
new_env_base_url = ""

# Param validation
if not old_env_base_url or not new_env_base_url:
    print("Please set the base URLs in the paramters. Exiting")
    exit()

if not old_env_username:
    old_env_username = input("Original Environment Username: ")

if not old_env_password:
    old_env_passwd = getpass.getpass('Original Environment Password:')
else:
    old_env_passwd = old_env_password

if not new_env_username:
    new_env_username = input("New Environment Username: ")

if not new_env_password:
    new_env_passwd = getpass.getpass('New Environment Password:')
else:
    new_env_passwd = new_env_password


# Shorthand helper function
def get_auth_token(username,passwd,base_url):
    response = requests.post(
        url=base_url + '/v2/public/user/login',
        data=json.dumps({"username": username, "password": passwd}),
        headers={
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json'
        })
    return response.json()['session_id']

# Get new auth tokens with new creds
old_env_auth_token = get_auth_token(old_env_username,old_env_passwd,old_env_base_url)
new_env_auth_token = get_auth_token(new_env_username,new_env_passwd,new_env_base_url)


old_env_headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'application/json',
    'X-Auth-Token': old_env_auth_token
}

new_env_headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'application/json',
    'X-Auth-Token': new_env_auth_token
}

# list all insights
def list_insights(headers,base_url):
    data = {}
    response = requests.get(
        url=base_url + '/v2/public/insights/list',
        data=json.dumps(data),
        headers=headers
        )
    return response.json()    

# Create a custom insight
def create_insight(insight_config,headers,base_url):
    response = requests.post(
        url=base_url + '/v2/public/insights/create',
        data=json.dumps(insight_config),
        headers=headers
        )
    return response.json()        

# Add notes to insight
def add_insight_notes(insight_id,description,headers,base_url):
    data = {
        "notes": description
    }
    response = requests.post(
        url=base_url + '/v2/public/insights/' + str(insight_id) + '/notes/update',
        data=json.dumps(data),
        headers=headers
        )
    return response # No response expected   


# # Add notes to insight
# def list_packs(headers,base_url):
#     response = requests.get(
#         url=base_url + '/v2/public/insights/packs/list',
#         headers=headers
#         )
#     print(response)
#     return response.json # No response expected   
# list_packs(old_env_headers,old_env_base_url)
# exit()    

print("Generating list of custom insights")
all_insights = list_insights(old_env_headers,old_env_base_url)
custom_insights = []
for insight in all_insights:
    if insight["source"] == "custom":
        #Clean up unneeded params
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

# Loop through insight_configs and add a filter for each
custom_insight_ids = []
for insight in custom_insights:
    print("Creating new insight: " + insight['name'])
    new_insight_info = create_insight(insight,new_env_headers,new_env_base_url)
    custom_insight_ids.append(new_insight_info['insight_id'])

    # Add notes to the insight
    add_insight_notes(new_insight_info['insight_id'],insight['description'],new_env_headers,new_env_base_url)  
