#!/usr/bin/env python

from myth_commercial_cut import CommercialCutJob
import unittest

class testCommercialCutJob(unittest.TestCase):
    def setUp(self):
        self.ccj = CommercialCutJob('/var/lib/mythtv/recordings/1234_20131127020000.mpg',1234, '2013-11-27 02:00:00')

    def testDBCredentials(self):
        self.assertIsNotNone(self.ccj.user)
        self.assertIsNotNone(self.ccj.passwd)
        self.assertIsNotNone(self.ccj.db)
        self.assertIsNotNone(self.ccj.host)
        self.assertIsNotNone(self.ccj.port)

    def testProps(self):
        self.assertEqual(self.ccj.width, 1280)
        self.assertEqual(self.ccj.height, 720)
        self.assertEqual(self.ccj.fps, 59940)
        self.assertIsNotNone(self.ccj.cutlist)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
