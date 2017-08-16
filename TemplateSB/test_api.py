"""
Tests for Api.
"""
from api import Api
import unittest

IGNORE_TEST = False
VALUES = range(4)
NAME = 'a'
DEFINITIONS = {NAME: VALUES}


#############################
# Tests
#############################
# pylint: disable=W0212,C0111,R0904
class TestApi(unittest.TestCase):

  def setUp(self):
    self.api = Api()

  def testConstructor(self):
    if IGNORE_TEST:
      return
    self.assertEqual(len(self.api._definitions.items()), 0)

  def _testAddDefinitions(self, definitions):
    self.api.addDefinitions(definitions)
    self.assertEqual(self.api._definitions.items(), definitions.items())

  def testAddDefinitions(self):
    if IGNORE_TEST:
      return
    self._testAddDefinitions(DEFINITIONS)

  def testRemoveDefinitions(self):
    if IGNORE_TEST:
      return
    self._testAddDefinitions(DEFINITIONS)
    self.api.removeDefinitions(DEFINITIONS.keys())
    for name in DEFINITIONS.keys():
      self.assertFalse(name in self.api._definitions.keys())

  def testGetDefinitions(self):
    self.api.addDefinitions({NAME: VALUES})
    definitions = self.api.getDefinitions()
    self.assertEqual(definitions.items(), DEFINITIONS.items())


if __name__ == '__main__':
  unittest.main()
