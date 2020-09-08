# ArcGISOnline_user_management_scripts
Various Python 3.8x scripts to manage user accounts on an ArcGIS Online organization.

ArcGISOnline_Delete_Users.py <br>
To selectively delete users from an ArcGIS online organization based on a list from a textfile.  This list can contain users filtered / sorted by whichever criteria you wish. The script checks to see if the users are members of any groups or are storing any content (items) prior to revoking their ArcGIS Pro licenses and deleted the user.  Otherwise, the script will throw Traceback errors when attempting to delete the user.

arcgis_online_update_user_roles.py <br>
To iterate through list of e-mails, check if a user is associated with that e-mail address, and then update their user role.
