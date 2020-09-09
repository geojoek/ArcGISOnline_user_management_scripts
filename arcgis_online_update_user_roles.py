# Script to iterate through a textfile list of users in AGOL organization
# and update their member role to a custom role that allows Jupityr notebook privileges
# By Joe Kopera (jkopera@umass.edu), September 2020

# designed to run in conda environment with arcgis python API installed: https://developers.arcgis.com/python/guide/install-and-set-up/

# load libraries
from arcgis.gis import * # This just imports all of the modules

#log in to ArcGIS Online
print("Logging In...")
gis = GIS("", "", "") # fill in your login credentials here. See https://developers.arcgis.com/python/guide/using-the-gis/
print("Logged in as: " + gis.properties.user.username)

# Reads a simple text file with a list of ArcGIS Online user e-mails, one e-mail per line. Make sure that there's a blank line at the end of file
user_list_file = open(r"FILENAME",'r') # textfile with list of user e-mails
user_list = [] # user list object

# Create a list object by iterating through the text file. There are better ways to do this using dict.reader
for line in user_list_file:
    sliced = slice(-1) # Removes the new line '\n' character at the end of each e-mail, which is why you need to add a blank line at the end of the file, or else it clips the last letter from the text on this line
    user_list.append(line[sliced])

needs_account = [] # list of e-mails not associated with any accounts.  These are ostensibly users who need to create accounts
updated_users = [] # list of users whose roles were updated

jupyter_role = arcgis.gis.RoleManager(gis).get_role('[ROLE_ID]') # insert the role ID... you can get this via using arcgis.gis.RoleManager to list all roles and their corresponding IDs for your AGOL organization. See https://developers.arcgis.com/python/guide/accessing-and-managing-users/
print(jupyter_role.description)

# iterate through list of users and update their user roles

for x in user_list:
    if len(gis.users.search(query='email: {}'.format(x))) == 0: #crude check to see if that username exists... in this case letting me know who has yet to create account
        needs_account.append(x)
        pass # if username doesn't exist, script does nothing.
    else:
        account_to_update = (gis.users.search(query='email: {}'.format(x))) # creating a variable here is an inelegant hack to create a single User object that can actaully be acted on via using the .search method (which returns a list of User objects) to get the user account associated with the e-mail address
        for account in account_to_update:
            account.update_role(role = jupyter_role)
            print ("{}'s role has been updated to {}".format(account.username,gis.users.roles.get_role(account.roleId).name)) # This checks against the actual role assigned to the user after this task to confirm, as a fail-safe
            updated_users.append(account)

print("User roles updated for the following users:")
for x in updated_users:
    print(x)

print("\nThe following users still need to create accounts:")
for x in needs_account:
     print(x) # prints list of folks who still need to create accounts