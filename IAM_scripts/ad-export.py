#! /usr/bin/env python

import ldap
import re
import json
import os
import getpass

# You can fetch the simple bind credentials from an environment variable
ldap_user_env = 'LDAP_USER'
ldap_pw_env = 'LDAP_PW'
ldap_user = os.environ.get(ldap_user_env)
ldap_pw = os.environ.get(ldap_pw_env)

if ldap_user == None:
    ldap_user = input("Enter LDAP username for simple bind: ")
if ldap_pw == None:
    ldap_pw = getpass.getpass("Enter LDAP password for simple bind: ")

# file that the script will write to
export_file = 'divvy_ad_python_export.json'

#sometimes display_name isn't available, so use this user attribute instead
display_name_subst = 'samAccountName'

# search context for the users #MUST CHANGE THIS TO WORK IN YOUR ENVIRONMENT
search_context = 'ou=Users,ou=iamtest,dc=iamtest,dc=divvycloud,dc=com'

# LDAP host to connect to #MUST CHANGE THIS TO WORK IN YOUR ENVIRONMENT
ldap_conn_string = 'ldap://localhost:9999'


# This is what we use to get the initial set of groups that we will loop through and find
# the group members
search_filter =  '(&(objectClass=group)(cn=AWS_*))'

# This is to used to compare the group names a user belongs to as we loop through the users.
# It also parses out the account and role name from a AD group name.

#the below would match a group name like foo_AWS_123456789123_AdminRole
p = re.compile(r'^.*?AWS_(?P<account>\d{12})_(?P<role>.*)$')

# this would match AWS_123456789123_AdminRole
#p = re.compile(r'^AWS_(?P<account>\d{12})_(?P<role>.*)$')


# initialize the connection
connect = ldap.initialize(ldap_conn_string)
connect.set_option(ldap.OPT_REFERRALS, 0)
connect.simple_bind_s(ldap_user, ldap_pw)


# grab all the users who are member of AWS groups
federated_users = []
ad_groups = []
aws_members_l = []

# Build up the list of users who are members of groups that match the search filter
result = connect.search_s(search_context,
                          ldap.SCOPE_SUBTREE,
                          search_filter)

for r in result:
    aws_members_l += r[1]['member']

# make that list unique
aws_members = set(aws_members_l)

total_users = len(aws_members)
print(f'Total number of AWS users is: {str(total_users)}.')

# Begin looping through users list
for m in aws_members:
    m = m.decode('utf-8')
    dn_parts = ldap.dn.explode_dn(m)
    cn = dn_parts[0]
    search_filter =  cn
    assumable_roles = []

    result = connect.search_s(search_context,
                          ldap.SCOPE_SUBTREE,
                          search_filter)
    for r in result:
        for group in r[1]['memberOf']:
            dn_parts = ldap.dn.explode_dn(group)
            group_name = dn_parts[0].replace('CN=','')
            m = re.match(p, group_name)
            if m:
                account = m.groupdict()['account']
                role = m.groupdict()['role']
                role_arn = f'arn:aws:iam::{account}:role/{role}'
                assumable_roles.append(role_arn)
        sam_account_name = r[1]['sAMAccountName'][0].decode('utf-8')
        try:
            display_name = r[1]['displayName'][0].decode('utf-8')
        except:
            display_name = sam_account_name

        # Build the user dictionary
        user_dict = { 'assumableRoles': assumable_roles,
                      'displayName': display_name,
                      'uid': sam_account_name}
        federated_users.append(user_dict)
        print(f'Finished working on: {display_name}')
        print(f'Records Processed: {str(len(federated_users))} / {str(total_users)}.')

with open(export_file, 'w') as f:
    json.dump(federated_users, f, indent=4,)
        


