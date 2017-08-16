"""
Tests for StatusMessage
"""
from status_message import StatusMessage
from line_extractor import LineExtractor
import unittest
import warnings


IGNORE_TEST = False

#############################
# Tests
#############################
# pylint: disable=W0212,C0111,R0904
class TestStatusMessage(unittest.TestCase):

  def setUp(self):
    self.extractor = LineExtractor("")
    self.message = StatusMessage(self.extractor)

  def testError(self):
    if IGNORE_TEST:
      return
    with self.assertRaises(ValueError):
      self.message.error("")

  def testWarning(self):
    if IGNORE_TEST:
      return
    with warnings.catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        self.message.warning("")
        # Verify some things
        assert len(w) == 1
    

if __name__ == '__main__':
  unittest.main()
