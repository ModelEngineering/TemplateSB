"""
Tests for constants
"""
import constants
import os
import unittest


IGNORE_TEST = False
TEST_FILE = "testdata_constants.yaml"
PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILE = os.path.join(PARENT_DIR, "testdata_constants.yaml")

#############################
# Tests
#############################
# pylint: disable=W0212,C0111,R0904
class TestConstants(unittest.TestCase):

  def testBasicr(self):
    if IGNORE_TEST:
      return
    unassigned = [k for k,v in constants.getGlobals().items()
                  if (v is None) and k[0] != "_"]
    self.assertEqual(len(unassigned), 0)

  def testSetConstantsFromConfig(self):
    constants.setConstantsFromConfig(path=TEST_FILE)
    self.assertEqual(constants.WARNING_ASSIGNMENTS, -1)



if __name__ == '__main__':
  unittest.main()
