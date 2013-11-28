#!/usr/bin/env python

from myth_commercial_cut import CommercialCutJob
import unittest

class testCommercialCutJob(unittest.TestCase):
    def setUp(self):
        self.ccj = CommercialCutJob()

    def testProps(self):
        self.assertEqual(self.ccj.width, 1280)
        self.assertEqual(self.ccj.height, 720)
        self.assertEqual(self.ccj.fps, 59940)


def main():
    unittest.main()

if __name__ == "__main__":
    main()
