# This script will find all the users that match your AD Group -> AWS_Role mapping pattern
# as defined in $AWSGrouPattern.  It then will loop through each one of those users
# and build a list of all the roles the users are able to assume based on the group membership
# and writes that file to $export_file.

# You will may need to modify $aws_group_pattern, $export_file, and $regexp for your environment

#This is the regexp for extracting the strings from a group name needed to produced an ARN
$regexp = '^.*?AWS_(?<account>\d{12})_(?<role>.*)$'

# This would allow you to filter only subset of your AD group
$aws_group_patterns = @( 
      "AWS_*"
      "gRestricted_AWS_*"
)

# this is the file the script will write to
$export_file = "divvy_ad_export.json"

# in case a user user.DisplayName is null (like service accounts) we can specificy other user attributes here
# currently 'samAccountName' and 'DistinguishedName' are the only supported alternatives.

$display_name_subst = 'samAccountName'
#display_name_subst = 'DistinguishedName'

$aws_group_filters = @(
)

# We are going to to search for groups that match that pattern
foreach ($group_pattern in $aws_group_patterns) {
    $aws_group_filters += 'Name -like "' +  $group_pattern + '"'
}

#combine that filter string
$s = $aws_group_filters -join '-or '
$s
#Define the output file
$aws_group_members = Get-ADGroup -Filter "$s" | Get-ADGroupMember -Recursive
$aws_group_members = $aws_group_members | Select-Object -Unique
$aws_group_members


$federated_users = @()

Write-Host "Total Number of AD users that can assume AWS roles: " $aws_group_members.Count
foreach($group_user in $aws_group_members) {
    Write-Host "Fetching attributes for" $group_user.distinguishedName
    $user = Get-ADuser -Filter {samAccountName -like $group_user.SamAccountName }  -properties DisplayName, DistinguishedName, GivenName, Surname, Department, LockedOut, Enabled, MemberOf, PrimaryGroup
    Select-Object DisplayName, DistinguishedName, GivenName, Surname, Department, LockedOut, Enabled, MemberOf, PrimaryGroup
    $assumable_roles = @()
    foreach ($group in $user.MemberOf) {
      #get the group name from the DN
      $CN = $group -replace "(CN=)(.*?),.*",'$2'
      foreach ($pattern in $aws_group_patterns) {
          if ($CN -like $pattern){
              if ($CN -match $regexp) {
                $role_arn = "arn:aws:iam::" + $Matches.account + ":role/" + $Matches.role
                $assumable_roles += $role_arn
              }
          }
      }
    }
  
  # user alternatives if derived displayname is null
    $display_name = $user.DisplayName
    if ($display_name -eq $null ) {

        switch($display_name_subst) {
          'samAccountName' { $display_name = $user.SamAccountName }
          'DistinguishedName' { $display_name = $user.DistinguishedName }
        }
    }
    $user_hash = @{
      "assumableRoles" = $assumable_roles
      "displayName" = $display_name
      "uid" = $user.SamAccountName  
    }
    $federated_users += $user_hash
    Write-Host "Records Processed: " $federated_users.Count "/" $aws_group_members.Count
}

$obj = [PSCustomObject]$federated_users
$obj | ConvertTo-Json | Out-File $export_file