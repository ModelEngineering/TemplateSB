"""
Tests ExpressionEvaluator
"""
from expression_evaluator import ExpressionEvaluator
import unittest

IGNORE_TEST = False
VAR1 = 'A'
VAR2 = 'B'
VALUES1 = range(4)
VALUES2 = [10*x for x in VALUES1]
NAMESPACE = {VAR1: VALUES1, VAR2: VALUES2}


#############################
# Tests
#############################
# pylint: disable=W0212,C0111,R0904
class TestExpressionEvaluator(unittest.TestCase):

  def setUp(self):
    self.evaluator = ExpressionEvaluator(NAMESPACE)

  def testConstructor(self):
    if IGNORE_TEST:
      return
    self.assertEqual(self.evaluator._namespace[VAR1],
        NAMESPACE[VAR1])

  def testAddNamespace(self):
    if IGNORE_TEST:
      return
    var3 = 'CCC'
    values3 = range(10)
    self.assertFalse(var3 in self.evaluator._namespace)
    self.evaluator.addNamespace({var3: values3})
    self.assertEqual(self.evaluator._namespace[var3], values3)

  def testDeleteNamespace(self):
    if IGNORE_TEST:
      return
    self.assertTrue(VAR2 in self.evaluator._namespace)
    self.evaluator.deleteNames([VAR2])
    self.assertFalse(VAR2 in self.evaluator._namespace)

  def testDo(self):
    namespace = {'a': 1, 'b': 2}
    expression = "a + b"
    self.evaluator.addNamespace(namespace)
    result = self.evaluator.do(expression)
    self.assertEqual(result, namespace['a'] + namespace['b'])

  def testDoException(self):
    namespace = {'a': 1, 'b': 0}
    expression = "a / b"
    self.evaluator.addNamespace(namespace)
    with self.assertRaises(Exception):
      result = self.evaluator.do(expression)
    


if __name__ == '__main__':
  unittest.main()
