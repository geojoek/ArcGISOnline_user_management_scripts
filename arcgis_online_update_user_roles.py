# Script to iterate through users in AGOL organization if they have the member role of "Publisher"
# and update their member role to a custom role that allows Jupityr notebook privileges
# By Joe Kopera (jkopera@umass.edu), September 2020
# designed to run in conda environment with arcgis python API installed

# load libraries
from arcgis.gis import *

#log in to ArcGIS Online
print("Logging In...")
gis = GIS(, , ) # fill in your login credentials here
print("Logged in as: " + gis.properties.user.username)

# Reads a simple text file with a list of ArcGIS Online user names, one name per line.
user_list_file = open(r"FILENAME",'r') # textfile with list of users
user_list = [] # user list object
# Create a list object by iterating through the text file. There are better ways to do this using dict.reader
for line in user_list_file:
    sliced = slice(-1) # Removes the new line '\n' character at the end of each username
    user_list.append(line[sliced])

needs_account = []
updated_users = []

jupyter_role = arcgis.gis.RoleManager(gis).get_role('[ROLE_ID]') # insert the role ID... can get this via using arcgis.gis.RoleManager to list all roles and their corresponding IDs
print(jupyter_role.description)

# iterate through list of users and update their user roles

for x in user_list:
    if len(gis.users.search(query='email: {}'.format(x))) == 0: #crude check to see if that username exists... in this case letting me know who has yet to create account
        needs_account.append(x)
        pass
    else:
        account_to_update = (gis.users.search(query='email: {}'.format(x)))
        for account in account_to_update:
            account.update_role(role = jupyter_role)
            print ("{}'s role has been updated to {}".format(account.username,account.role))
            updated_users.append(account)

for x in needs_account:
     print("{} has not yet created an account".format(x)) # prints list of folks who still need to create accounts