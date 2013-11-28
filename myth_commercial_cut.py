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
    def __init__(self, chanid, starttime):
        self.chanid = chanid
        self.starttime = starttime
        self._dbSetup()
        self._jobSetup()
        self._getCutlist()

    def _dbSetup(self):
        config_path = os.path.expanduser('~') + os.sep + '.mythtv' + os.sep + 'mysql.txt'
        config = StringIO.StringIO()
        config.write('[dummysection]\n')
        config.write(open(config_path, 'r').read())
        config.seek(0, os.SEEK_SET)
        cp = ConfigParser.SafeConfigParser()
        cp.readfp(config)
        self.user = cp.get('dummysection','DBUserName')
        self.passwd = cp.get('dummysection','DBPassword')
        self.db = cp.get('dummysection','DBName')
        self.host = cp.get('dummysection','DBHostName')
        self.port = int(cp.get('dummysection','DBPort'))

    def _jobSetup(self):
        try:
            db = MySQLdb.Connect(host=self.host,
                    db=self.db,
                    user=self.user,
                    passwd=self.passwd,
                    port=self.port)
            db.autocommit(True)
            cur = db.cursor()
            cur.execute("""SELECT data
                FROM recordedmarkup
                WHERE chanid=%s
                AND starttime=%s
                AND type=30""",
                (self.chanid,self.starttime))
            self.width = cur.fetchone()[0]
            cur.execute("""SELECT data
                FROM recordedmarkup
                WHERE chanid=%s
                AND starttime=%s
                AND type=31""",
                (self.chanid,self.starttime))
            self.height = cur.fetchone()[0]
            cur.execute("""SELECT data
                FROM recordedmarkup
                WHERE chanid=%s
                AND starttime=%s
                AND type=32""",
                (self.chanid,self.starttime))
            self.fps = cur.fetchone()[0]
        except MySQLdb.Error, e:
            print('Error: ' + str(e.args[0]) + str(e.args[1]))
            exit(1)
        finally:
            cur.close()
            db.close()

    def _getCutlist(self):
        try:
            db = MySQLdb.connect(host=self.host,
                    db=self.db,
                    user=self.user,
                    passwd=self.passwd,
                    port=self.port)
            cur = db.cursor()
            cur.execute("""SELECT type,mark
                FROM recordedmarkup
                WHERE chanid=%s
                AND starttime=%s
                AND (type=0 OR type=1)
                ORDER BY mark
                """,
                (self.chanid,self.starttime))
            self.cutlist = cur.fetchall()
            print(len(self.cutlist))
            print(self.cutlist)
            self.printCutlist()
        except MySQLdb.Error, e:
            print('Error: ' + str(e.args[0] + str(e.args[1])))
            exit(1)
        finally:
            cur.close()
            db.close()


    def printCutlist(self):
        print("Type\tMark\r\n")
        for cl in self.cutlist:
            print("%d\t%d\r\n" % (cl[0],cl[1]))


# How you call this script:
# $myth_commercial_cut DIR FILE CHANID STARTTIME
if __name__ == "__main__":
	if (len(sys.argv) !=5):
		print('Error: Arguments\r\nUsage: myth_commercial_cut DIR FILE CHANID STARTTIME\r\n')
		exit(1)
	
	filename = os.path.join(sys.argv[1], sys.argv[2])
	chanid = sys.argv[3]
	starttime = sys.argv[4]
