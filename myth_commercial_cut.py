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

# How you call this script:
# $myth_commercial_cut DIR FILE
if __name__ == "__main__":
	if (len(sys.argv) !=3):
		print('This script only accepts 2 arguments! You passed in ' + len(sys.argv) + '!')
		exit(1)
	
	filename = os.path.join(sys.argv[1], sys.argv[2])
	

