# Script to delete list of users who have are not members of groups and have no items (content), from your ArcGIS organizaton
# I got this list from filtering a spreadsheet to meet certain criteria for users who haven't logged in within the past year
# I exported this sheet from GeoJobe's admin tools on our local ArcGIS Online organization.
# I do not yet trust myself to not cause damage by trying to sort through all of the users and applying a filter users with Python
# list of usernames is designated text file below.

# Written to operate in conda environment where arcgis Python API is installed.
# Script by jkopera@umass.edu

# import arcgis & os libraries
from arcgis.gis import GIS
from arcgis.gis import User
from arcgis.gis import admin
import os

#log in to ArcGIS Online
print("Logging In...")
gis = GIS("portal URL", "username", "password")
print("Logged in as: " + gis.properties.user.username)

# Reads a simple text file with a list of ArcGIS Online user names, one name per line.
user_list_file = open(r"path to textfile",'r') # textfile with list of users
user_list = [] # user list object
# Create a list object by iterating through the text file. There are better ways to do this using dict.reader
for line in user_list_file:
    sliced = slice(-1) # Removes the new line '\n' character at the end of each username
    user_list.append(line[sliced])
# print(user_list)

### Iterate through the user list, checking to see if they are members of groups, have content (items), and if so, revokes their ArcGIS Pro license and deletes them

# Set up lists of results that script will print at the end.
undeleted_users = []
deleted_users = []

for x in user_list:
    if len(gis.users.search(query='username: {}'.format(x))) == 0: #crude check to see if that username exists or has already been deleted. Elsewise script throws Traceback
        pass
    else:
        group_list = gis.users.get(x).groups # checks if user is assigned to any groups or has any items.  If they do they can't be deleted.
        item_list = gis.users.get(x).items()
        if not item_list: # checks to see if user has items. Script will abort with Traceback upon deletion unless one does this.
            if not group_list: # checks to see if user is member of groups. Script will abort with Traceback upon deletion unless one does this.
                if gis.admin.license.get('ArcGIS Pro').revoke(username=x, entitlements='*') == True:
                    print("Revoked licenses for {}".format(x))
                    delete = gis.users.get(x).delete()
                    deleted_users.append(x)
                    print("Deleted " + x)
                else:
                    print("Could not revoke licenses for some reason. User not deleted.")
                    pass
            else:
                print("{} is member of a group. Could not delete user.".format(x))
                undeleted_users.append(x)
                pass
        else:
            print ("{} has items, cannot delete user".format(x))
            pass

del_num = len(deleted_users)

print ("Successfully deleted {} users:\n".format(del_num))
for x in deleted_users:
    print(x)

print ("Could not delete following users: \n")
for x in undeleted_users:
    print(x)