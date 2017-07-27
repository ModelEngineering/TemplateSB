"""
Tests for Expander
"""
from expander import Expander, EXPRESSION_START,  \
    EXPRESSION_END

import unittest
import numpy as np


IGNORE_TEST = False
DEFINITIONS = {'a': ['a', 'b', 'c'], 'm': ['1', '2', '3'],
    'c': ['c', '']}
SUBSTITUTION1 = "J1: S1 -> S2; k1*S1"
SUBSTITUTION2 = "J{a}1: S{a}1 -> S{a}2; k1*S{a}1"


#############################
# Tests
#############################
# pylint: disable=W0212,C0111,R0904
class TestSubtituter(unittest.TestCase):

  def setUp(self):
    self.expander = Expander(DEFINITIONS)

  def testMakeSubtitutionList(self):
    if IGNORE_TEST:
      return
    substitution_list = Expander.makeSubstitutionList(DEFINITIONS)
    expected = np.prod([len(v) for v in DEFINITIONS.values()])
    self.assertEqual(len(substitution_list), expected)
    substitution_list = Expander.makeSubstitutionList({})
    self.assertEqual(len(substitution_list), 0)
    definitions = dict(DEFINITIONS)
    key = DEFINITIONS.keys()[0]
    del definitions[key]
    substitution_list = Expander.makeSubstitutionList(definitions)
    expected = np.prod([len(v) for v in definitions.values()])
    self.assertEqual(len(substitution_list), expected)

  def testGetTemplateExpressions(self):
    return
    if IGNORE_TEST:
      return
    variables = self.expander._getTemplateVariables("x{a} -> x + {a}; k*{a}")
    self.assertEqual(variables,["{a}"])
    variables = self.expander._getTemplateVariables("x{a} -> x + {b}; k*{a}")
    self.assertEqual(variables, ["{a}", "{b}"])
    variables = self.expander._getTemplateVariables("x{a} -> x + { b }; k*{a}")
    self.assertEqual(variables, ["{a}", "{b}"])
    variables = self.expander._getTemplateVariables("x{a} -> x + { 1, 2,3 }; k*{a}")
    self.assertEqual(set(variables), set(["{a}", "{1,2,3}"]))
    
  def testReplace(self):
    if IGNORE_TEST:
      return
    expander = Expander(DEFINITIONS)
    result = expander.do(SUBSTITUTION1)
    self.assertEqual(result[0], SUBSTITUTION1)
    result = expander.do(SUBSTITUTION2)
    expected = len(DEFINITIONS['a'])
    self.assertEqual(len(result), expected)

  def testGetTemplateExpressions(self):
    if IGNORE_TEST:
      return
    expression1 = "a + b"
    expression2 = "x"
    expression3 = "cos(a) + sin(b)"
    proto_template = "xy%s%s%sz + yz%s%s%sx"  
    for expr in [expression1, expression2, expression3]:
      template = proto_template % (
          EXPRESSION_START, expr, EXPRESSION_END,
          EXPRESSION_START, expr, EXPRESSION_END)
      result = self.expander.getTemplateExpressions(template)
      self.assertEqual(len(result), 1)
      self.assertEqual(result[0], expr)

if __name__ == '__main__':
  unittest.main()
