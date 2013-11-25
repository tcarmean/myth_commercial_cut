#!/usr/bin/env python

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

# Go into the database and get the list of cut points
# Return an array of cut points
def getCutlist(chanid, starttime):
	# SELECT type,mark FROM recrodedmarkup WHERE chanid=$chanid AND starttime=$starttime AND (type=0 OR type=1) ORDER BY mark;
	# Figure out how to feed that into mysqldb and fetch all rows into an array
	pass

# Lossless export of each segment based on cut points
# 
def cutCommercials():
	pass

# Merge all output files in order
def cutMerge():
	pass

def updateDB():
	pass



# How you call this script:
# $myth_commercial_cut CHANID STARTTIME
if __name__ == "__main__":
	if (len(sys.argv) !=3):
		print('Error: Arguments\r\nUsage: myth_commercial_cut CHANID STARTTIME\r\n')
		exit(1)
	
	filename = os.path.join(sys.argv[1], sys.argv[2])
	

