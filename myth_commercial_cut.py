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
    def __init__(self):
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
