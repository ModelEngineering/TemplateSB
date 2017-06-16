"""
Tests for SbStar.
"""
import unittest
import numpy as np
from sbstar import SbStar, PROCESSOR_NAME, Substituter,  \
    LINE_TRAN, LINE_DEFN, ESCAPE_STG, LINE_SUBS


IGNORE_TEST = False
DEFINITIONS = {'{a}': ['a', 'b', 'c'], '{m}': ['1', '2', '3']}
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
%s''' % SUBSTITUTION2
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
    self.substituter = Substituter(DEFINITIONS)

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

  def testGetTemplateVariables(self):
    if IGNORE_TEST:
      return
    variables = self.substituter._getTemplateVariables("x{a} -> x + {a}; k*{a}")
    self.assertEqual(variables,["{a}"])
    variables = self.substituter._getTemplateVariables("x{a} -> x + {b}; k*{a}")
    self.assertEqual(variables, ["{a}", "{b}"])
    variables = self.substituter._getTemplateVariables("x{a} -> x + { b }; k*{a}")
    self.assertEqual(variables, ["{a}", "{b}"])
    variables = self.substituter._getTemplateVariables("x{a} -> x + { 1, 2,3 }; k*{a}")
    self.assertEqual(set(variables), set(["{a}", "{1,2,3}"]))
    
  def testReplace(self):
    if IGNORE_TEST:
      return
    substituter = Substituter(DEFINITIONS)
    strings = TEMPLATE_STG1.split('\n')
    new_string = ('\n').join(strings[2:])
    result = substituter.replace(new_string)
    self.assertEqual(result[0], new_string)
    result = substituter.replace(SUBSTITUTION2)
    expected = len(DEFINITIONS['{a}'])
    self.assertEqual(len(result), expected)

  def _IsSubDict(self, dict_super, dict_sub):
    for key in dict_sub.keys():
      if not key in dict_super:
        return False
      if not dict_sub[key] == dict_super[key]:
        return False
    return True

  def testUpdateDefinitions(self):
    if IGNORE_TEST:
      return
    stg = "x{b} -> x + { 1, 2,3 }; k*{b}"
    self.substituter._updateDefinitions(stg)
    definitions = self.substituter._definitions
    self.assertTrue(self._IsSubDict(definitions, DEFINITIONS))
    new_definitions = {'{b}': ['b', ''], '{1,2,3}': ['1', '2', '3']}
    self.assertTrue(self._IsSubDict(definitions, new_definitions))
    

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
    import pdb; pdb.set_trace()
    for val in DEFINITIONS['{a}']:
      self.assertTrue("J%s1:" % val in lines)

  def testExpandErrorInDefinition(self):
    if IGNORE_TEST:
      return
    result = self.sbstar.expand()
    sbstar = SbStar(TEMPLATE_STG3)
    result2 = sbstar.expand()
    self.assertEqual(result, result2)
    sbstar = SbStar(TEMPLATE_STG4)
    with self.assertRaises(ValueError):
      _ = sbstar.expand()


if __name__ == '__main__':
  unittest.main()
