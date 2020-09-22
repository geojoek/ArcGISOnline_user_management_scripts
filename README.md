# ArcGISOnline_user_management_scripts
Various Python 3.8x scripts to manage user accounts on an ArcGIS Online organization.

<strong>ArcGISOnline_Delete_Users.py</strong> <br>
To selectively delete users from an ArcGIS online organization based on a list from a textfile.  This list can contain users filtered / sorted by whichever criteria you wish. The script checks to see if the users are members of any groups or are storing any content (items) prior to revoking their ArcGIS Pro licenses and deleted the user.  Otherwise, the script will throw Traceback errors when attempting to delete the user.

<strong>arcgis_online_update_user_roles.py</strong> <br>
To iterate through list of e-mails, check if a user is associated with that e-mail address, and then update their user role.

<strong>arcgis_online_deauthhorize_Pro.py</strong><br>
Script that calls up list of users authorized for ArcGIS Pro, iterates through that list, and revokes all licenses and entitlements for users who have not logged into ArcGIS online for over a year
