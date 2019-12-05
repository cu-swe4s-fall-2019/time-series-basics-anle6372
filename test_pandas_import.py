"""Unittesting framework for data_import.py
Parameters
----------
None
Returns
-------
None
"""

import unittest
from os import path
import pandas_import

# Test output file creation
class TestFileCreation(unittest.TestCase):

    def test_no_file(self):
        self.assertFalse(path.exists('five_min.csv'))
        self.assertFalse(path.exists('fifteen_min.csv'))

    def test_yes_file(self):
        pandas_import.main()
        self.assertTrue(path.exists('five_min.csv'))
        self.assertTrue(path.exists('fifteen_min.csv'))

if __name__ == '__main__':
    unittest.main()