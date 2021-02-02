# Script to iterate through list of users in your ArcGIS organizaton and migrate users over to new GIS Professional user type.
# Written to operate in conda environment where arcgis Python API is installed: https://developers.arcgis.com/python/
# Note: this API is not ArcPy and vice versa
# Script by jkopera@umass.edu
# February 2021

# I stole several parts of Carlos Barahona's great script to do this. Their script is at: https://github.com/crbarahona/migrate_ago_usertype/blob/main/migrate_ago_usertype.py

# import libraries & modules

from arcgis.gis import GIS
from arcgis.gis import User
from arcgis.gis import admin
import logging
from datetime import datetime
import time # David Tenant insisted on this

# Woot Woot parameters!
agolAdminName = "" # your AGOL administrator account
agolAdminPassword = "" # the password to that account
creditLimit = 1000 # the credit limit you want to assign to all users. Make sure you have enough credits in your pool and adjust accordingly
outputLogFile = r"{:%Y-%m-%d}-migration-prod.log".format(datetime.now()) # location and name of the log file to log what happened.
gisURL = r"" # the URL to your ArcGIS Online or Portal organization

# set up logging
logging.basicConfig(filename=outputLogFile,format='%(asctime)s %(message)s', level=logging.INFO)

# log in to ArcGIS Online
print("Logging In...")
gis = GIS(gisURL, agolAdminName, agolAdminPassword)
print("Logged in as: " + gis.properties.user.username)

# Getting basic info. for assigning all extensions for ArcGIS Pro and giving GIS Professional user types them.
proLicense = gis.admin.license.get('ArcGIS Pro') # gets the license object for Pro
licEntitlements = list(proLicense.properties['provision']['orgEntitlements']['entitlements'].keys()) # Makes list of extensions for that pro license objects
if "desktopAdvN" in licEntitlements:
    licEntitlements.remove("desktopAdvN") # This removes the license for Pro itself from the above list, since a Pro license is automatically part of the GIS Professional Advanced User Type
else:
    pass

# The first step in the license migration is one needs to revoke all Pro licenses from Creators in order to update all users to the GIS Professional user type
# That's what this code block does:

# Get list of users in your AGOL org who are currently licensed for ArcPro
# This method is *a lot* faster than iterating through all users in the org
arcProList = gis.admin.license.get('ArcGIS Pro').all()
print(str(len(arcProList)) + " users are licensed for ArcGIS Pro.")
arcProUserNames = []
# print(arcProList)
for x in arcProList:
    arcProUserNames.append(x.get("username"))


# this function is written to process a list of username strings, and not arcgis API user objects
# it goes through the above list and revokes their ArcPro licenses, upgrades the User Type to GIS Professional Advanced, provisions all the ArcPro extensions to them, and bumps up their credits
def revokeArcProLicense(userlist):
    for name in userlist:
        user = gis.users.get(name)
        print(user.username + " is being processed...")
        try:
            gis.admin.license.get('ArcGIS Pro').revoke(username=user.username, entitlements='*') # the part that revokes the ArcGIS Pro license
            logging.info("Removed ArcPro license for" + user.username)
            user.update_license_type('GISProfessionalAdvUT') # reassigns this user to GIS professional
            logging.info("Updated user type for" + user.username)
            proLicense.assign(username=user.username, entitlements=licEntitlements, suppress_email=True) # provisions them ArcPro extensions
            logging.info("Added extensions for" + user.username)
            gis.admin.credits.allocate(user, creditLimit) # allocate them credits
            logging.info("Updated credit limit for" + user.username)
        except Exception as e: # just a check in case for some reason it couldn't revoke their license. There are more elegant error handling workflows for trying this again
            print(e)
            logging.info("Failed revoking licenses for " + user.username + "because:")
            logging.info(e)
            time.sleep(10) # waits 10 seconds before moving on to next user
        arcProUserNames.remove(name) # removes this user from the list if revoking & reassigning license is successful

# evoking the above function
print("Revoking ArcPro licenses for Creator user types who have them, updating user type, and provisioning ArcPro extensions...")
while len(arcProUserNames) != 0: # basically keeps looping through list of users with ArcPro licenses until that list has no people left in it.  Kind of brute force approach and can get stuck if there are errors but...
    revokeArcProLicense(arcProUserNames)
else:
    pass

# So this should have taken care of migrating all the users who already had an ArcGIS Pro license or had onboarded as a new GIS Professional while I was writing this script.

# Now we're going go through the whole list of all the users in the org who aren't GIS Professionals, and weren't taken care of by the above steps, and simply update their user type.

print("Now iterating through users who aren't licensed for ArcPro and changing them to GIS Professionals")
print("Retrieving list of all the users in the org (this may take a while)...")
users = gis.users.search(max_users=9999) # this max users is needed because otherwise this method defaults to 100 users
print("Success in getting list of all users")

for user in users:
    if user.userLicenseTypeId != "GISProfessionalAdvUT": # This only handles creator user types not handled by above function
        try:
            user.update_license_type('GISProfessionalAdvUT')
            logging.info("Changing user type for " + user.username +" to GIS Professional.")
            print("Success changing " + user.username +" to GIS Professional.")
        except Exception as e:
            logging.info("Unsuccessful changing " + user.username + " to GIS Professional because " + str(e))
            print("unsuccessful changing" + user.username + " to GIS professional!")
            time.sleep(10)
    else:
        pass

print("All done!")