# Script to iterate through list of users in your ArcGIS organizaton and remove ArcPro license from users that have not logged in for over a year.
# Written to operate in conda environment where arcgis Python API is installed.
# Script by jkopera@umass.edu

# import libraries & modules
from arcgis.gis import GIS
from arcgis.gis import User
from arcgis.gis import admin
from datetime import datetime, timedelta

#  Parameters
now = datetime.now()
outFileNameAndPath = r"PATH_AND_FILENAME" + str(now.year) + str(now.month) + str(now.year) + r".txt"

# log in to ArcGIS Online
print("Logging In...")
gis = GIS("PORTAL_URL", "USERNAME", "PASSWORD")
print("Logged in as: " + gis.properties.user.username)

# Get list of users who are currently licenses for arc pro
# This is *a lot* faster than iterating through all users in the org
arcProList = gis.admin.license.get('ArcGIS Pro').all()
arcProUserNames = []
# print(arcProList)
for x in arcProList:
    arcProUserNames.append(x.get("username"))
print("\n {} users are licensed for ArcGIS Pro.".format(len(arcProUserNames)))

# iterate through user list
inactive_users = [] # creates list object to put names of inactive users in.
for x in arcProUserNames:
    a_user = gis.users.get(x)
    last_accessed = datetime.fromtimestamp(a_user.lastLogin/1000) # .fromtimestamp property returns Unix timestamp in milliseconds so we need to divide by 1000 to turn into datetime object, which is in Unix seconds.
    delta = now-last_accessed # gives time since last login
    if delta >= timedelta(days = 365): # if more than 365 days since last login, removes ArcGIS Pro license
        print(str(a_user.fullName) + "\n has not been active since: {}.".format(last_accessed))
        revokeCheck = gis.admin.license.get('ArcGIS Pro').revoke(username=a_user.username, entitlements='*') # the part that revokes the ArcGIS Pro license
        if revokeCheck == True: # just a check in case for some reason it couldn't revoke their license
            print("{}'s ArcPro license has been revoked.".format(a_user.username))
            inactive_users.append(a_user.username) # appends their username to list to be exported to file later
        else:
            print("Error, could not revoke license.")
            pass
    else:
        print("{} is active, keeping license".format(a_user.username))
        pass

print("\n{} inactive users have had their arcpro licenses removed".format(len(inactive_users)))

with open(outFileNameAndPath,'a', encoding='cp1252') as outFile:
    for x in inactive_users:
        outFile.write("\n{}".format(x))
print("Users with revoked licenses written to {}".format(outFileNameAndPath))