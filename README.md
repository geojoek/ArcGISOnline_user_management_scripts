# ArcGISOnline_user_management_scripts
Various Python 3.8x scripts to manage user accounts on an ArcGIS Online organization.

**ArcGISOnline_Delete_Users.py**

To selectively delete users from an ArcGIS online organization based on a list from a textfile.  This list can contain users filtered / sorted by whichever criteria you wish. The script checks to see if the users are members of any groups or are storing any content (items) prior to revoking their ArcGIS Pro licenses and deleted the user.  Otherwise, the script will throw Traceback errors when attempting to delete the user.

**arcgis_online_update_user_roles.py** 

To iterate through list of e-mails, check if a user is associated with that e-mail address, and then update their user role. Particularly handy if you have a group of people who want to access a new functionality or app that you've associated with a particular user role (i.e., ArcGIS/Jupyter Notebooks)

**arcgis_online_deauthhorize_Pro.py**

Script that calls up list of users authorized for ArcGIS Pro, iterates through that list, and revokes all licenses and entitlements for users who have not logged into ArcGIS online for over a year

**ArcGIS_Online_GIS_Professional_migration.py**

If you manage an ArcGIS Online organization or Portal under the ESRI Higher Education license program, this script is to migrate your users to a GIS Professional Advanced user type.  It goes through a list of your users who already have ArcGIS Pro licenses, revokes them, updates the User Type, and adds add-on licenses for all of the ArcPro extensions to each account.  It then goes through all of your AGOL organization members who aren't licensed for ArcPro and updates their user type to GIS Professional Advanced.
