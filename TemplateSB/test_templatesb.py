"""
Tests for TemplateSB.
"""
from templatesb import TemplateSB, LINE_TRAN, LINE_SUBS, LINE_COMMAND
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
%s ExecutePython End %s  
''' %(COMMAND_START, COMMAND_END, str(DEFINITIONS),
    COMMAND_START, COMMAND_END)
SUBSTITUTION1 = "J1: S1 -> S2; k1*S1"
SUBSTITUTION2 = "J{a}1: S{a}1 -> S{a}2; k1*S{a}1"
SUBSTITUTION3 = "J{c}1: S{c}1 -> S{c}2; k1*S{c}1"
TEMPLATE_STG1 = '''
%s
%s
''' % (COMMAND, SUBSTITUTION1)
TEMPLATE_BAD = '''%s
%s
''' % (COMMAND_START, SUBSTITUTION1)
TEMPLATE_STG2 = '''%s
%s
''' % (COMMAND, SUBSTITUTION2)
TEMPLATE_STG3 = '''%s
%s
''' % (COMMAND, SUBSTITUTION3)
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
class TestTemplateSB(unittest.TestCase):

  def setUp(self):
    self.templatesb = TemplateSB(TEMPLATE_STG2)

  def testConstructor(self):
    if IGNORE_TEST:
      return
    self.assertTrue(len(self.templatesb._lines) > 0)

  def testClassifyLine(self):
    if IGNORE_TEST:
      return
    self.templatesb._current_line = COMMAND_START
    self.assertEqual(self.templatesb._classifyLine(), LINE_COMMAND)
    self.templatesb._current_line = SUBSTITUTION1
    self.assertEqual(self.templatesb._classifyLine(), LINE_TRAN)
    self.templatesb._current_line = SUBSTITUTION2
    self.assertEqual(self.templatesb._classifyLine(), LINE_SUBS)

  def testErrorMsg(self):
    if IGNORE_TEST:
      return
    with self.assertRaises(ValueError):
      self.templatesb._errorMsg("")

  def testGetNextLine(self):
    if IGNORE_TEST:
      return
    templatesb = TemplateSB(TEMPLATE_STG2)
    line = templatesb._getNextLine()
    lines = []
    idx = 0
    expecteds = TEMPLATE_STG2.split('\n')
    while line is not None:
      expected = expecteds[idx]
      idx += 1
      lines.append(line)
      self.assertEqual(line, expected)
      line = templatesb._getNextLine()
    expected = len(expecteds)
    self.assertEqual(expected, len(lines))

  def testGetNextLineContinuation(self):
    if IGNORE_TEST:
      return
    stg = '''this \
    is a \
    continuation.'''
    templatesb = TemplateSB(stg)
    line = templatesb._getNextLine()
    self.assertTrue("is a" in line)
    self.assertTrue("continuation" in line)
    line = templatesb._getNextLine()
    self.assertIsNone(line)

  def testExecuteStatements(self):
    if IGNORE_TEST:
      return
    template = TemplateSB(COMMAND)
    self.assertEqual(len(template._definitions.keys()), 0)
    result = template.expand()
    self.assertEqual(result.count('\n'), COMMAND.count('\n'))

  def _testExpand(self, template, variable):
    """
    :param str template: template to expand
    :param str variable: variable to check
    """
    self.templatesb = TemplateSB(template)
    lines = self.templatesb.expand()
    for val in DEFINITIONS[variable]:
      self.assertTrue("J%s1:" % val in lines)

  def testExpand(self):
    if IGNORE_TEST:
      return
    self._testExpand(TEMPLATE_STG2, 'a')
    self._testExpand(TEMPLATE_STG3, 'c')

  def testExpandErrorInDefinition(self):
    if IGNORE_TEST:
      return
    with self.assertRaises(ValueError):
      templatesb = TemplateSB(TEMPLATE_BAD)
      result = templatesb.expand()

  def testNoDefinintion(self):
    if IGNORE_TEST:
      return
    self.templatesb = TemplateSB(TEMPLATE_NO_DEFINITION)
    with self.assertRaises(ValueError):
      lines = self.templatesb.expand()

  def testFile(self):
    if IGNORE_TEST:
      return
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_path = os.path.dirname(dir_path)
    src_path = os.path.join(parent_path, "Example")
    src_path = os.path.join(src_path, "sample.tmpl")
    TemplateSB.processFile(src_path, "/tmp/out.mdl")


if __name__ == '__main__':
  unittest.main()
