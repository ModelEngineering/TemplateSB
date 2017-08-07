"""
Tests for LineExtractor
"""
from line_extractor import LineExtractor
from constants import LINE_TRAN,  \
    LINE_SUBS, LINE_COMMAND, CONTINUED_STG, LINE_NONE
from command import COMMAND_START, COMMAND_END

import unittest


IGNORE_TEST = False
COMMAND = "%s ExecutePython Start %s" %(COMMAND_START, COMMAND_END)
TEMPLATE_TRAN =  \
'''This is a line.
So is this.'''
TEMPLATE_SUBS =  \
'''This {is} a line.
So is {t}his.'''
TEMPLATE_COMMAND =  \
    "%s ExecutePython Start %s" %(COMMAND_START, COMMAND_END)


#############################
# Tests
#############################
# pylint: disable=W0212,C0111,R0904
class TestLineExtractor(unittest.TestCase):

  def setUp(self):
    self.extractor= LineExtractor(TEMPLATE_TRAN)

  def testConstructor(self):
    if IGNORE_TEST:
      return
    self.assertEqual(TEMPLATE_TRAN.count("\n")+1,
      len(self.extractor._lines))

  def _testGetNextLine(self):
    if IGNORE_TEST:
      return
    extractor = LineExtractor(TEMPLATE_TRAN)
    extractor._getNextLine()
    lines = []
    idx = 0
    expecteds = TEMPLATE_TRAN.split('\n')
    while extractor._current_line is not None:
      expected = expecteds[idx].strip()
      idx += 1
      lines.append(extractor._current_line)
      self.assertEqual(extractor._current_line, expected)
      extractor._getNextLine()
    expected = len(expecteds)
    self.assertEqual(expected, len(lines))

  def testGetNextLine(self):
    if IGNORE_TEST:
      return
    extractor = LineExtractor(TEMPLATE_TRAN)
    extractor._getNextLine()
    lines = []
    idx = 0
    expecteds = TEMPLATE_TRAN.split('\n')
    while extractor._current_line is not None:
      expected = expecteds[idx].strip()
      idx += 1
      lines.append(extractor._current_line)
      self.assertEqual(extractor._current_line, expected)
      extractor._getNextLine()
    expected = len(expecteds)
    self.assertEqual(expected, len(lines))

  def testGetNextLineContinued(self):
    line_1 = "Line part 1."
    line_2 = "Line part 2."
    line = "%s %s\n%s" % (line_1, CONTINUED_STG, line_2)
    extractor = LineExtractor(line)
    extractor._getNextLine()
    self.assertTrue(line_1 in extractor._current_line)
    self.assertTrue(line_2 in extractor._current_line)

  def _testClassifyLine(self, template, expected_classification):
    extractor= LineExtractor(template)
    extractor._getNextLine()
    extractor._classifyLine()
    self.assertEqual(extractor.getCurrentLineType(), 
        expected_classification)

  def testClassifyLine(self):
    if IGNORE_TEST:
      return
    self._testClassifyLine(TEMPLATE_TRAN, LINE_TRAN)
    self._testClassifyLine(TEMPLATE_SUBS, LINE_SUBS)
    self._testClassifyLine(TEMPLATE_COMMAND, LINE_COMMAND)

if __name__ == '__main__':
  unittest.main()
