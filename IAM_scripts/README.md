# Usage Instructions


This repository contains scripts for dumping user information from Active Directory (AD) in to JSON file structure used by the Cloud IAM Governance Module.  By understanding the membership of AD Groups that are [mapped to AWS roles](https://aws.amazon.com/blogs/security/aws-federated-authentication-with-active-directory-federation-services-ad-fs/), we can provide direct linkage of a federated user to an AWS resource. 

We have provided an example in PowerShell as well as Python.  These were tested with PowerShell 7, and Python 3.8.

The scripts have variables that must be modified by the user in order to pull out the relevant group membership information from AD.  You will find instructions in the scripts as to what needs to be modified.


Executing the file:

```./ad-export.ps1```

or

```ad-export.py```


Here is an example of what the output should look like:


```
[
   {
       "displayName": "Catherine Laine",
       "name": "Aurélie Legendre",
       "uid": "43d00bfc-cf0a-43da-aa99-493642755ec6",
       "assumableRoles": [
           "arn:aws:iam::123456789012:role/cherry_role_sns_allow",
           "arn:aws:iam::123456789012:role/redoak_role_s3_deny_list"
       ]
   },
   {
       "displayName": "Maryse Aubert",
       "name": "Raymond Tanguy",
       "uid": "19855a44-8993-4780-8f7e-c5431411b239",
       "assumableRoles": [
           "arn:aws:iam::123456789012:role/silvermaple_role_sns_allow",
           "arn:aws:iam::123456789012:role/redoak_role_s3_deny",
           "arn:aws:iam::123456789012:role/redoak_role_s3_allow"
       ]
   }
]
```

# Setting up a Development Environment for PowerShell



If adding users, you'll need to do install the Active Directory User Tools on the Windows System that you are using to managing AD.
You should also install latest version of PowerShell.

Once installed.  If you prefer to develop from a non-Windows platform you can run the following commands to set up SSH on the Windows machine and use PowerShell remoting capabilities.

```
 Install-Module -Name Microsoft.PowerShell.RemotingTools
 Enable-SSHRemoting
```

Alternately, these steps are the manual equivalences:

Setup ssh https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse
Setup powershell remoting over ssh https://docs.microsoft.com/en-us/powershell/scripting/learn/remoting/ssh-remoting-in-powershell-core?view=powershell-7


## Client Side

 To use the remote PowerShell session in VS Code or on the CLI, run the following command, where "1.2.3.4" is the IP/Hostname of the Windows machine where you'll be executing the PowerShell.
 
$session = New-PSSession -HostName 1.2.3.4  -UserName Admin@iamtest
 Enter-PSSession $session
 Invoke-Command -FilePath ./ad-export.ps1 -Session $session


# Setting up Dev Environment For Python

You'll need a SSH tunnel to a linux system that can connect to the AD in AWS:

In this case 1.2.0.2 is the IP of the AD Server and 11.0.7.8 is the IP of the Linux system that you are tunneling through.

```ssh -L 9999:1.2.0.2:389 ec2-user@11.0.7.8```

You can then validate the connection:

```ldapsearch -vvv -H ldap://localhost:9999 -x -D Admin@iamtest -w 'PUT_PASSWORD_HERE' -b 'ou=users,ou=iamtest,dc=iamtest,dc=divvycloud,dc=com' '(sAMAccountName=*)'```

This should dump all AD Groups that map to an AD Role:


```ldapsearch -vvv -H ldap://localhost:9999 -x -D Admin@iamtest -w 'PUT_PASSWORD_HERE' -b 'ou=users,ou=iamtest,dc=iamtest,dc=divvycloud,dc=com' '(&(objectClass=group)(cn=AWS_*))'```