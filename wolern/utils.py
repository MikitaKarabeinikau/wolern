"""
utils.py is meant for small, reusable helper functions that are not specific to business logic.

Date formatting is a general-purpose helper — you will probably want to reuse this for:

    Logging when words were added.

    Debug messages.

    File naming (if you use timestamps).

    Displaying last update time in GUI.

"""

from time import gmtime,strftime

def current_datetime():
    return strftime("%d-%m-%Y %H:%M:%S",gmtime())