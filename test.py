#!/usr/bin/env python

from myth_commercial_cut import CommercialCutJob
import unittest

class testCommercialCutJob(unittest.TestCase):
    def setUp(self):
        self.ccj = CommercialCutJob()

def main():
    unittest.main()

if __name__ == "__main__":
    main()
