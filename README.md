# ArcGISOnline_delete_users
Python 3.8x script to selectively delete users from an ArcGIS online organization based on a list from a textfile.  This list can contain users filtered / sorted by whichever criteria you wish.

The script checks to see if the users are members of any groups or are storing any content (items) prior to revoking their ArcGIS Pro licenses and deleted the user.  Otherwise, the script will throw Traceback errors when attempting to delete the user.
