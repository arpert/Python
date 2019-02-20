import os
import glob
import datetime 

def average(values):
    """Computes the arithmetic mean of a list of numbers.

    >>> print(average([20, 30, 70]))
    40.0
    """
    return sum(values) / len(values)

for e in glob.glob('./*.py', recursive=True):
  st = os.stat(e)
  print("%40s %12d %s" % (e, st.st_size, datetime.datetime.fromtimestamp(st.st_atime).strftime('%Y.%m.%d %H:%M:%S')))

import doctest
doctest.testmod() 

raw_input('Press any key to continue')

import unittest

class TestStatisticalFunctions(unittest.TestCase):

    def test_average(self):
        self.assertEqual(average([20, 30, 70]), 40.0)
        self.assertEqual(round(average([1, 5, 7]), 1), 4.3)
        with self.assertRaises(ZeroDivisionError):
            average([])
        with self.assertRaises(TypeError):
            average(20, 30, 70)

unittest.main()