"""
Tests for TemplateProcessor
"""
from template_processor import TemplateProcessor, LINE_TRAN,  \
    LINE_SUBS, LINE_COMMAND, CONTINUED_STG
from command import COMMAND_START, COMMAND_END

import copy
import unittest
import numpy as np
import os


IGNORE_TEST = False
DEFINITIONS = {'a': ['a', 'b', 'c'], 
               'm': ['1', '2', '3'],
               'c': ['c', '']}
COMMAND = \
'''%s ExecutePython Start %s
DEFINITIONS = %s
api.addDefinitions(DEFINITIONS)
%s ExecutePython End %s '''  \
    %(COMMAND_START, COMMAND_END, str(DEFINITIONS),
    COMMAND_START, COMMAND_END)
SUBSTITUTION1 = "J1: S1 -> S2; k1*S1"
SUBSTITUTION2 = "J{a}1: S{a}1 -> S{a}2; k1*S{a}1"
SUBSTITUTION3 = "J{c}1: S{c}1 -> S{c}2; k1*S{c}1"
TEMPLATE_STG1 = '''
%s
%s
''' % (COMMAND, SUBSTITUTION1)
TEMPLATE_BAD = '''%s
%s''' % (COMMAND_START, SUBSTITUTION1)
TEMPLATE_STG2 = '''%s
%s''' % (COMMAND, SUBSTITUTION2)
TEMPLATE_STG3 = '''%s
%s''' % (COMMAND, SUBSTITUTION3)
TEMPLATE_NO_DEFINITION = SUBSTITUTION3


def isSubDict(dict_super, dict_sub):
  """
  Tests if the second dictonary is a subset of the first.
  :param dict dict_super:
  :param dict dict_sub:
  :return bool:
  """
  for key in dict_sub.keys():
    if not key in dict_super:
      return False
    if not dict_sub[key] == dict_super[key]:
      return False
  return True


#############################
# Tests
#############################
# pylint: disable=W0212,C0111,R0904
class TestTemplateProcessor(unittest.TestCase):

  def setUp(self):
    self.processor = TemplateProcessor(TEMPLATE_STG2)

  def testConstructor(self):
    if IGNORE_TEST:
      return
    self.assertTrue(len(self.processor._lines) > 0)

  def testClassifyLine(self):
    if IGNORE_TEST:
      return
    self.processor._current_line = COMMAND_START
    self.assertEqual(self.processor._classifyLine(), LINE_COMMAND)
    self.processor._current_line = SUBSTITUTION1
    self.assertEqual(self.processor._classifyLine(), LINE_TRAN)
    self.processor._current_line = SUBSTITUTION2
    self.assertEqual(self.processor._classifyLine(), LINE_SUBS)

  def testErrorMsg(self):
    if IGNORE_TEST:
      return
    with self.assertRaises(ValueError):
      self.processor._errorMsg("")

  def testGetNextLine(self):
    if IGNORE_TEST:
      return
    processor = TemplateProcessor(TEMPLATE_STG2)
    line = processor._getNextLine()
    lines = []
    idx = 0
    expecteds = TEMPLATE_STG2.split('\n')
    while line is not None:
      expected = expecteds[idx].strip()
      idx += 1
      lines.append(line)
      self.assertEqual(line, expected)
      line = processor._getNextLine()
    expected = len(expecteds)
    self.assertEqual(expected, len(lines))

  def testGetNextLineContinued(self):
    line_1 = "Line part 1."
    line_2 = "Line part 2."
    line = "%s %s\n%s" % (line_1, CONTINUED_STG, line_2)
    processor = TemplateProcessor(line)
    result = processor._getNextLine()
    self.assertTrue(line_1 in result)
    self.assertTrue(line_2 in result)

  def testGetNextLineContinuation(self):
    if IGNORE_TEST:
      return
    stg = '''this \
    is a \
    continuation.'''
    processor = TemplateProcessor(stg)
    line = processor._getNextLine()
    self.assertTrue("is a" in line)
    self.assertTrue("continuation" in line)
    line = processor._getNextLine()
    self.assertIsNone(line)

  def testExecuteStatements(self):
    if IGNORE_TEST:
      return
    template = TemplateProcessor(COMMAND)
    self.assertEqual(len(template._definitions.keys()), 0)
    result = template.do()
    self.assertEqual(result.count('\n'), COMMAND.count('\n'))

  def _testExpand(self, template, variable):
    """
    :param str template: template to expand
    :param str variable: variable to check
    """
    self.processor = TemplateProcessor(template)
    lines = self.processor.do()
    for val in DEFINITIONS[variable]:
      self.assertTrue("J%s1:" % val in lines)

  def testDo(self):
    if IGNORE_TEST:
      return
    self._testExpand(TEMPLATE_STG2, 'a')
    self._testExpand(TEMPLATE_STG3, 'c')

  def testExpandErrorInDefinition(self):
    if IGNORE_TEST:
      return
    with self.assertRaises(ValueError):
      processor = TemplateProcessor(TEMPLATE_BAD)
      result = processor.do()

  def testNoDefinintion(self):
    if IGNORE_TEST:
      return
    self.processor = TemplateProcessor(TEMPLATE_NO_DEFINITION)
    with self.assertRaises(ValueError):
      lines = self.processor.do()

  def testFile(self):
    if IGNORE_TEST:
      return
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_path = os.path.dirname(dir_path)
    src_path = os.path.join(parent_path, "Example")
    src_path = os.path.join(src_path, "sample.tmpl")
    TemplateProcessor.processFile(src_path, "/tmp/out.mdl")

  def testExecuteStatements(self):
    if IGNORE_TEST:
      return
    var1 = 'aa'
    var2 = 'bb'
    value1 = 1
    const2 = 5
    statements = ["%s = %d" % (var1, value1), 
        "%s = %d*%s" % (var2, const2, var1)]
    self.processor._execute_statements(statements)
    self.assertEqual(self.processor._namespace['aa'], value1)
    self.assertEqual(self.processor._namespace['bb'], value1*const2)

  def testExecuteStatementsError(self):
    if IGNORE_TEST:
      return
    var1 = 'aa'
    var2 = 'bb'
    value1 = 1
    const2 = 5
    statements = ["%s = " % (var1), 
        "%s = %d*%s" % (var2, const2, var1)]
    with self.assertRaises(ValueError):
      self.processor._execute_statements(statements)
    

if __name__ == '__main__':
  unittest.main()
