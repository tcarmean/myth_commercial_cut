#!/usr/bin/env python

from decimal import *

getcontext().prec = 40

import os
import sys
import base64
import uuid
import subprocess
import ConfigParser
import StringIO
import shutil
try:
        import MySQLdb
except ImportError:
        print('You need to install the MySQLdb python module in order to use this script')
        exit(1)

# Every User Job is a CommercialCutJob
class CommercialCutJob(object):
    def __init__(self, directory, filename, chanid, starttime):
        self.filename = os.path.join(directory, filename)
        self.chanid = chanid
        self.starttime = startime
        # todo: internal method to do database lookups for fps, width, length, and cutlist

    def _getMetaData(self):
        # Query for the Width
        # SELECT data from recordedmarkup WHERE chanid=$chanid AND startime=$startime AND type=30
        # Query for the Length
        # SELECT data from recordedmarkup WHERE chanid=$chanid AND startime=$startime AND type=31
        # Query for the Framerate
        # SELECT data FROM recordedmarkup where chanid=$chanid AND starttime=$starttime AND type=32
        # Query for the CutList
        # SELECT type,mark FROM recrodedmarkup WHERE chanid=$chanid AND starttime=$starttime AND (type=0 OR type=1) ORDER BY mark;
        pass

    # Loop through the cutlist and generate a list of files that contain the segments we are looking for
    def cutCommercials(self):
        pass

    # Loop through the files generated by cutCommercials and merge them together
    def cutMerge(self):
        pass

    # Copy the merged file back and update the database with the new filename (extension) and size
    def updateDB(self):
        pass

# How you call this script:
# $myth_commercial_cut DIR FILE CHANID STARTTIME
if __name__ == "__main__":
	if (len(sys.argv) !=5):
		print('Error: Arguments\r\nUsage: myth_commercial_cut DIR FILE CHANID STARTTIME\r\n')
		exit(1)
	
	filename = os.path.join(sys.argv[1], sys.argv[2])
	chanid = sys.argv[3]
	starttime = sys.argv[4]
