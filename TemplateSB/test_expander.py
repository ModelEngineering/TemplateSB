"""
Tests for Expander
"""
from expander import Expander, EXPRESSION_START,  \
    EXPRESSION_END
from executor import Executor

import unittest
import numpy as np


IGNORE_TEST = True
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
    self.expander = Expander(Executor())

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
    
  def testDo(self):
    if IGNORE_TEST:
      return
    executor = Executor()
    executor.setDefinitions(DEFINITIONS)
    expander = Expander(executor)
    result = expander.do(SUBSTITUTION1)
    self.assertEqual(result[0], SUBSTITUTION1)
    result = expander.do(SUBSTITUTION2)
    expected = len(DEFINITIONS['a'])
    self.assertEqual(len(result), expected)
    
  def testDoSubstitutionNoDefinition(self):
    if IGNORE_TEST:
      return
    executor = Executor()
    expander = Expander(executor)
    result = expander.do(SUBSTITUTION1)
    self.assertEqual(result[0], SUBSTITUTION1)

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

  def testExpandTemplateExpressions(self):
    #if IGNORE_TEST:
    #  return
    executor = Executor()
    var = 'n'
    definitions = {var: [1, 2, 3]}
    executor.setDefinitions(definitions)
    expander = Expander(executor)
    template = "T{%s} + A -> T{%s+1}" % (var, var)
    expansion = expander.do(template)
    self.assertEqual(len(expansion), len(definitions[var]))
    # Check that each substitution is found
    for value in definitions[var]:
      found = False
      for substitution in expansion:
        if "T%d" % value in substitution:
          found = True
          break
      self.assertTrue(found)
      
    

if __name__ == '__main__':
  unittest.main()
