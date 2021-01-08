# Script to list all organizations in DivvyCloudf

import json
import requests
import getpass

requests.packages.urllib3.disable_warnings() # verify=False throws warnings otherwise

# USER INFO:
users_to_add = [
    { "email": "jhudson@rapid7.com", "name": "Joey Hudson", "username": "jhudson" },
    { "email": "afoster@rapid7.com", "name": "Alan Foster", "username": "afoster" },
    { "email": "awarnick@rapid7.com", "name": "Andrew Warnick", "username": "awarnick" },
    { "email": "aetheridge@rapid7.com", "name": "Antonio Etheridge", "username": "aetheridge" },
    { "email": "astambaugh@rapid7.com", "name": "Autumn Stambaugh", "username": "astambaugh" },
    { "email": "bgarber@@rapid7.com", "name": "Ben Garber", "username": "bgarber" },
    { "email": "bcannon@rapid7.com", "name": "Billy Cannon", "username": "bcannon" },
    { "email": "blaws@rapid7.com", "name": "Brendan Laws", "username": "blaws" },
    { "email": "crees@rapid7.com", "name": "Charlotte Rees", "username": "crees" },
    { "email": "dprauser@rapid7.com", "name": "Daniel Prauser", "username": "dprauser" },
    { "email": "dbosquet@rapid7.com", "name": "David Bosquet", "username": "dbosquet" },
    { "email": "dcoleman@rapid7.com", "name": "David Coleman", "username": "dcoleman" },
    { "email": "dhowe@rapid7.com", "name": "David Howe", "username": "dhowe" },
    { "email": "dpodgurskiy@rapid7.com", "name": "Denis Podgurskiy", "username": "dpodgurskiy" },
    { "email": "dsimon@rapid7.com", "name": "Dondi Simon", "username": "dsimon" },
    { "email": "ewilson@rapid7.com", "name": "Eric Wilson", "username": "ewilson" },
    { "email": "eburns@rapid7.com", "name": "Erik Burns", "username": "eburns" },
    { "email": "eenriquez@rapid7.com", "name": "Evan Enriquez", "username": "eenriquez" },
    { "email": "flegorreta@rapid7.com", "name": "Felipe Legorreta", "username": "flegorreta" },
    { "email": "gruberto@rapid7.com", "name": "Giovanni Ruberto", "username": "gruberto" },
    { "email": "gmcmillan@rapid7.com", "name": "Graem McMillan", "username": "gmcmillan" },
    { "email": "goverton@rapid7.com", "name": "Greg Overton", "username": "goverton" },
    { "email": "hcoakley@rapid7.com", "name": "Hanna Coakley", "username": "hcoakley" },
    { "email": "ilee@rapid7.com", "name": "Ivan Lee", "username": "ilee" },
    { "email": "jely@rapid7.com", "name": "Jake Ely", "username": "jely" },
    { "email": "jchow@rapid7.com", "name": "Jay Chow", "username": "jchow" },
    { "email": "jbauvinet@rapid7.com", "name": "Jean-Baptiste Auvinet", "username": "jbauvinet" },
    { "email": "jcarson@rapid7.com", "name": " Jennifer Carson", "username": "jcarson" },
    { "email": "jbrumbley@rapid7.com", "name": "Joe Brumbley", "username": "jbrumbley" },
    { "email": "jagnew@rapid7.com", "name": "Joseph Agnew", "username": "jagnew" },
    { "email": "jkelso@rapid7.com", "name": "Justin Kelso", "username": "jkelso" },
    { "email": "kaoki@rapid7.com", "name": "Kazuhito Aoki", "username": "kaoki" },
    { "email": "kfarhat@rapid7.com", "name": "Khalil Farhat", "username": "kfarhat" },
    { "email": "lwolfe@rapid7.com", "name": "Levi Wolf", "username": "lwolfe" },
    { "email": "lnakhils@rapid7.com", "name": "Lyev Nakhlis", "username": "lnakhils" },
    { "email": "mjansson@rapid7.com", "name": "Magnus Jansson", "username": "mjansson" },
    { "email": "meaton@rapid7.com", "name": "Marcus Eaton", "username": "meaton" },
    { "email": "mapena@rapid7.com", "name": "Mark Pena", "username": "mapena" },
    { "email": "mzemanek@rapid7.com", "name": "Martin Zemanek", "username": "mzemanek" },
    { "email": "mrider@rapid7.com", "name": "Matt Rider", "username": "mrider" },
    { "email": "mkilchenstein@rapid7.com", "name": "Matthew Kilchenstein", "username": "mkilchenstein" },
    { "email": "mconnolly@rapid7.com", "name": "Megan Connolly", "username": "mconnolly" },
    { "email": "mmckinley@rapid7.com", "name": "Michael McKinley", "username": "mmckinley" },
    { "email": "mlegall@rapid7.com", "name": "Michael Legall", "username": "mlegall" },
    { "email": "mdenyes@rapid7.com", "name": "Mike Denyes", "username": "mdenyes" },
    { "email": "mramasamy@rapid7.com", "name": "Mk Ramasamy", "username": "mramasamy" },
    { "email": "nhurd@rapid7.com", "name": "Natalie Hurd", "username": "nhurd" },
    { "email": "opinchard@rapid7.com", "name": "Olivier Pinchard", "username": "opinchard" },
    { "email": "pbehmer@rapid7.com", "name": "Philip Behmer", "username": "pbehmer" },
    { "email": "pvanlerverghe@rapid7.com", "name": "Pieter Vanlerverghe", "username": "pvanlerverghe" },
    { "email": "pmehta@rapid7.com", "name": "Pooja Mehta", "username": "pmehta" },
    { "email": "rwaskow@rapid7.com", "name": "Ralph Waskow", "username": "rwaskow" },
    { "email": "rchami@rapid7.com", "name": "Raymond Chami", "username": "rchami" },
    { "email": "rdepalma@rapid7.com", "name": "Raymond DePalma", "username": "rdepalma" },
    { "email": "rwebb@rapid7.com", "name": "Robert Webb", "username": "rwebb" },
    { "email": "rchettiar@rapid7.com", "name": "Rohit Chettiar", "username": "rchettiar" },
    { "email": "rtomita@rapid7.com", "name": "Ryuichi Tomita", "username": "rtomita" },
    { "email": "shooda@rapid7.com", "name": "Shamaz Hooda", "username": "shooda" },
    { "email": "sphadke@rapid7.com", "name": "Shivani Phadke", "username": "sphadke" },
    { "email": "stadi@rapid7.com", "name": "Siri Tadi", "username": "stadi" },
    { "email": "tgrifa@rapid7.com", "name": "Taylor Grifa", "username": "tgrifa" },
    { "email": "tgreen@rapid7.com", "name": "Thomas Green", "username": "tgreen" },
    { "email": "thonker@rapid7.com", "name": "Tim Honker", "username": "thonker" },
    { "email": "thonda@rapid7.com", "name": "Toshio Honda", "username": "thonda" },
    { "email": "trichardson@rapid7.com", "name": "Trevor Richardson", "username": "trichardson" },
    { "email": "vshrivaishnav@rapid7.com", "name": "Vinayak Shrivaishnav", "username": "vshrivaishnav" },
    { "email": "wbianchini@rapid7.com", "username": "wbianchini", "name": "Will Vianchini"}
]


# Username/password to authenticate against the API
username = "alexc"
password = "xTm=cT8r+AvjwjhFT" # Leave this blank if you don't want it in plaintext and it'll prompt you to input it when running the script. 

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
        "username": user['email']
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
