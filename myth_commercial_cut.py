#!/usr/bin/env python

from decimal import *

getcontext().prec = 40

import os
from math import ceil
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
    def __init__(self, filename, chanid, starttime):
        print('In CommercialCutJob.__init__\r\n')
        self.filename = filename
        self.chanid = chanid
        self.starttime = starttime
        self._dbSetup()
        self._jobSetup()
        self._getCutlist()

    def _dbSetup(self):
        print('In CommercialCutJob._dbSetup\r\n')
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
        print('In CommercialCutJob._jobSetup\r\n')
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
        print('In CommercialCutJob._getCutlist\r\n')
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
        except MySQLdb.Error, e:
            print('Error: ' + str(e.args[0] + str(e.args[1])))
            exit(1)
        finally:
            cur.close()
            db.close()

    def cutCommercials(self):
        print('In CommercialCutJob.cutCommercials\r\n')
        slow_seek = 0.0
        skip = 0
        for i in range(len(self.cutlist)):
            # MARK_CUT_END
            if self.cutlist[i][0] == 0:
                time = Decimal(self.cutlist[i][1]) / Decimal(self.fps) * Decimal(1000)
                slow_seek = ceil(time * 1000) / 1000.0
            else:
                if i == 0:
                    # Special case
                    dur = (Decimal(self.cutlist[i+1][1]) / Decimal(self.fps) * Decimal(1000)) - Decimal(slow_seek)
                    dur = ceil(dur * 1000) / 1000.0
                else:
                    # need to get the duration
                    dur = (Decimal(self.cutlist[i][1]) / Decimal(self.fps) * Decimal(1000)) - Decimal(slow_seek)
                    dur = ceil(dur * 1000) / 1000.0
                print('avconv -i /var/lib/mythtv/recordings/1234_20131127020000.mpg -ss %s -t %s -vcodec copy -acodec copy /tmp/cc_test/ng_cc-%d.mpg' % (str(slow_seek),str(dur),i))
                # Here we call an internal method to create the intermediate files
                self._createSegment(slow_seek, dur, i)

    def _createSegment(self, seek, dur, i):
        print('In CommercialCutJob._createSegment\r\n')
        path, fn = os.path.split(self.filename)
        temp_dir = '/tmp/' + fn[:-4]

        if not os.path.exists(temp_dir):
            # create the directory that is named for the recording
            os.makedirs(temp_dir)
        tf = fn[:-4] + '-' + str(i) + '.mpg'
        temp_file = os.path.join(temp_dir,tf)
        # This is the command we will use to create the segment
        cmdline = [
                '/usr/bin/avconv',
                '-i',
                self.filename,
                '-ss',
                str(seek),
                '-t',
                str(dur),
                '-vcodec',
                'copy',
                '-acodec',
                'copy',
                temp_file
                ]
        try:
            #stuff
            subprocess.check_call(cmdline)
        except subprocess.CalledProcessError, e:
            print(e.cmd)
            print(e.returncode)
            exit(1)

# How you call this script:
# $myth_commercial_cut DIR FILE CHANID STARTTIME
if __name__ == "__main__":
    if (len(sys.argv) !=5):
        print('Error: Arguments\r\nUsage: myth_commercial_cut DIR FILE CHANID STARTTIME\r\n')
        exit(1)
    filename = os.path.join(sys.argv[1], sys.argv[2])
    chanid = sys.argv[3]
    starttime = sys.argv[4]
    ccj = CommercialCutJob(filename, chanid, starttime)
    ccj.cutCommercials()
