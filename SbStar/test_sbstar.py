"""
Tests for SbStar.
"""
import unittest
import numpy as np
from sbstar import SbStar, PROCESSOR_NAME, Substituter,  \
    LINE_TRAN, LINE_DEFN, ESCAPE_STG, LINE_SUBS


IGNORE_TEST = False
DEFINITIONS = {'a': ['a', 'b', 'c'], 'm': ['1', '2', '3']}
DEFINITIONS_LINE = "%s %s Version 1.0 %s" %  \
    (ESCAPE_STG, PROCESSOR_NAME, str(DEFINITIONS))
SUBSTITUTION1 = "J1: S1 -> S2; k1*S1"
SUBSTITUTION2 = "J{a}1: S{a}1 -> S{a}2; k1*S{a}1"
TEMPLATE_STG1 = '''
%s
# No substitution
%s
''' % (DEFINITIONS_LINE, SUBSTITUTION1)
TEMPLATE_STG2 = '''%s
# Substitution
%s''' % (DEFINITIONS_LINE, SUBSTITUTION2)
TEMPLATE_STG3 = '''
# Missing template variable definition
J{c}1: S{c}1 -> S{c}2; k1*S{c}1
'''
TEMPLATE_STG4 = '''%s
# Substitution error
SUBSTITUTION2 = "J{d}1: S{d}1 -> S{d}2; k1*S{d}1"
''' % (DEFINITIONS_LINE)



#############################
# Tests
#############################
# pylint: disable=W0212,C0111,R0904
class TestSubtituter(unittest.TestCase):

  def setUp(self):
    pass

  def testMakeSubtitutionList(self):
    if IGNORE_TEST:
      return
    substitution_list = Substituter.makeSubstitutionList(DEFINITIONS)
    expected = np.prod([len(v) for v in DEFINITIONS.values()])
    self.assertEqual(len(substitution_list), expected)
    substitution_list = Substituter.makeSubstitutionList({})
    self.assertEqual(len(substitution_list), 0)
    definitions = dict(DEFINITIONS)
    key = DEFINITIONS.keys()[0]
    del definitions[key]
    substitution_list = Substituter.makeSubstitutionList(definitions)
    expected = np.prod([len(v) for v in definitions.values()])
    self.assertEqual(len(substitution_list), expected)

  def testReplace(self):
    if IGNORE_TEST:
      return
    substitution_list = Substituter.makeSubstitutionList(DEFINITIONS)
    substituter = Substituter(substitution_list)
    result = substituter.replace(TEMPLATE_STG1)
    self.assertEqual(result[0], TEMPLATE_STG1)
    result = substituter.replace(SUBSTITUTION2)
    expected = len(DEFINITIONS['a'])
    self.assertEqual(len(result), expected)


#############################
# Tests
#############################
# pylint: disable=W0212,C0111,R0904
class TestSbstar(unittest.TestCase):

  def setUp(self):
    self.sbstar = SbStar(TEMPLATE_STG2)

  def testConstructor(self):
    if IGNORE_TEST:
      return
    self.assertTrue(len(self.sbstar._lines) > 0)

  def testClassifyLine(self):
    if IGNORE_TEST:
      return
    self.sbstar._current_line = SUBSTITUTION1
    self.assertEqual(self.sbstar._classifyLine(), LINE_TRAN)
    self.sbstar._current_line = DEFINITIONS_LINE
    self.assertEqual(self.sbstar._classifyLine(), LINE_DEFN)
    self.sbstar._current_line = SUBSTITUTION2
    self.assertEqual(self.sbstar._classifyLine(), LINE_SUBS)

  def testErrorMsg(self):
    if IGNORE_TEST:
      return
    with self.assertRaises(ValueError):
      self.sbstar._errorMsg("")

  def testGetNextLine(self):
    if IGNORE_TEST:
      return
    sbstar = SbStar(TEMPLATE_STG2)
    line = sbstar._getNextLine()
    lines = []
    idx = 0
    expecteds = TEMPLATE_STG2.split('\n')
    while line is not None:
      expected = expecteds[idx]
      idx += 1
      lines.append(line)
      self.assertEqual(line, expected)
      line = sbstar._getNextLine()
    expected = len(expecteds)
    self.assertEqual(expected, len(lines))

  def testGetNextLineContinuation(self):
    if IGNORE_TEST:
      return
    stg = '''this \
    is a \
    continuation.'''
    sbstar = SbStar(stg)
    line = sbstar._getNextLine()
    self.assertTrue("is a" in line)
    self.assertTrue("continuation" in line)
    line = sbstar._getNextLine()
    self.assertIsNone(line)

  def testMakeVariableDefinitions(self):
    if IGNORE_TEST:
      return
    self.sbstar._current_line = DEFINITIONS_LINE
    self.sbstar._makeVariableDefinitions()
    self.assertEqual(DEFINITIONS, self.sbstar._definitions)

  def testExpand(self):
    if IGNORE_TEST:
      return
    lines = self.sbstar.expand()
    for val in DEFINITIONS['a']:
      self.assertTrue("J%s1:" % val in lines)

  def testExpandErrorInDefinition(self):
    #if IGNORE_TEST:
    #  return
    sbstar = SbStar(TEMPLATE_STG3)
    with self.assertRaises(ValueError):
      _ = sbstar.expand()
    sbstar = SbStar(TEMPLATE_STG4)
    with self.assertRaises(ValueError):
      _ = sbstar.expand()


if __name__ == '__main__':
  unittest.main()
