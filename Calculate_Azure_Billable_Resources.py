#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Package Dependancies
#-> pip install azure-mgmt-resource==3.0.0
#-> pip install haikunator
#-> pip install azure-identity>=1.5.0

# Import the needed credential and management objects from the libraries.
import os
import json
from datetime import datetime
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.identity import AzureCliCredential

# Prompt the user for a password without echoing
import getpass as secret



# Define Billable Instance Counters
computeCount=0
dbCount=0
cacheCount=0


# Retrieve the list of Resource Groups in your subscription.  
def get_resource_groups():  
    resourceGroups=[]
    for item in resource_client.resource_groups.list():
        resourceGroups.append(item.name)
    return resourceGroups

    
# Retrieve the list Compute Instances (Virtual Machines) by Resource Group.    
def check_compute_by_group():
    
    allResourceGroups = get_resource_groups()
        
    for reGroup in allResourceGroups:
        
        global computeCount
        rvmCount=0
        
        resource_list = resource_client.resources.list_by_resource_group(reGroup,filter ="resourceType eq 'Microsoft.Compute/virtualMachines' or resourceType eq 'microsoft.compute/virtualmachinescalesets' or resourceType eq 'microsoft.containerinstance/containergroups'")
        
        for resource in resource_list:
            rvmCount+=1
            print("\n--> FOUND ONE: \t"+ reGroup + "\t|\t" +resource.name + "\t|\t" + resource.type+"\n")

        if(rvmCount>0):
            print("-----------------------------------------------------------------------")
            print(f"Number of Compute instances in Resource Group {reGroup} is: " + str(rvmCount))
            print("-----------------------------------------------------------------------")
            computeCount+=rvmCount

            
            
# Retrieve the list cache instances by Resource Group.
def check_redis_by_group():
    
    allResourceGroups = get_resource_groups()
        
    for reGroup in allResourceGroups:
        
        global cacheCount
        redCount=0
        
        resource_list = resource_client.resources.list_by_resource_group(reGroup,filter ="resourceType eq 'microsoft.cache/redis'")
        
        for resource in resource_list:
            redCount+=1
            print("\n--> FOUND ONE: \t"+ reGroup + "\t|\t" +resource.name + "\t|\t" + resource.type+"\n")

        if(redCount>0):
            print("-----------------------------------------------------------------------")
            print(f"Number of Redis instances in Resource Group {reGroup} is: " + str(redCount))
            print("-----------------------------------------------------------------------")
            cacheCount+=redCount

            
# Retrieve the list of Databases and DB Instances (Virtual Machines) by Resource Group.    
def check_db_by_group():
    
    allResourceGroups = get_resource_groups()
        
    for reGroup in allResourceGroups:
        
        global dbCount
        rDBCount=0
        
        resource_list = resource_client.resources.list_by_resource_group(reGroup,filter ="resourceType eq 'microsoft.dbformysql/flexibleservers' or resourceType eq 'microsoft.dbformysql/servers' or resourceType eq 'microsoft.dbforpostgresql/servers' or resourceType eq 'microsoft.sql/servers' or resourceType eq 'microsoft.sql/servers/databases' or resourceType eq 'microsoft.dbformariadb/servers' or resourceType eq 'microsoft.documentdb/databaseaccounts'")
        
        for resource in resource_list:
            rDBCount+=1
            print("\n--> FOUND ONE: \t"+ reGroup + "\t|\t" +resource.name + "\t|\t" + resource.type+"\n")

        if(rDBCount>0):
            print("-----------------------------------------------------------------------")
            print(f"Number of DBs instances in Resource Group {reGroup} is: " + str(rDBCount))
            print("-----------------------------------------------------------------------")
            dbCount+=rDBCount
            

# Calculate and out put Billable Instances Totals.            
def calculate_billable_instances():  
    
    print("RESOURCE_GROUP" + "\t|\t" + "RESOURCE_NAME" + "\t|\t" + "RESOURCE_TYPE\n")
    
    print("1. Calculating Compute Instances now\n")
    check_compute_by_group()
    
    print("\n2. Calculating DB instances now\n")
    check_db_by_group()
    
    print("\n3. Calculating Cache instances now\n")
    check_redis_by_group()
    
    print("\nBILLABLE INSTANCES\n")
    print(">> Compute Instances >  " + str(computeCount)) 
    print("------------------------------------------------")
    print(">> Database Instances >  " + str(dbCount)) 
    print("------------------------------------------------")
    print(">> Cache Instances >  " + str(cacheCount)) 
    print("------------------------------------------------")
    print("\n######################################")
    print("| Total Billable instances   >  " + str(computeCount+dbCount+cacheCount) +" |") 
    print("######################################")
        

def start_here():
    
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Please note you will need the following to proceed: ")
    print("\t1. Your Subscription ID ")
    print("\t2. Your Client ID ")
    print("\t3. Your Secret Key ")     
    print("\t4. Your tenant ID ")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("\n")
    
start_here()
subscription = input('ENTER YOUR SUBSCRIPTION ID: ')
    
# Acquire a credential object using CLI-based authentication.
credential = ServicePrincipalCredentials(
client_id=input("ENTER YOUR CLIENT ID: "),
secret=secret.getpass("ENTER YOUR SECRET KEY: "),    
tenant=input('ENTER YOUR TENANT ID: '))
    
# Retrieve subscription ID from environment variable.
subscription_id = os.environ.get(
    "AZURE_SUBSCRIPTION_ID", subscription) 

# Obtain the management object for resources.
resource_client = ResourceManagementClient(credential, subscription_id) 

print("\n")
print("Please wait, this may take a moment ...")
print("\n")
calculate_billable_instances()

