"""
Tests Executor
"""
from executor import Executor
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
class TestExecutor(unittest.TestCase):

  def setUp(self):
    self.executor = Executor()

  def testConstructor(self):
    if IGNORE_TEST:
      return
    self.assertTrue('api' in self.executor._namespace)

  def testAddNamespace(self):
    if IGNORE_TEST:
      return
    self.executor.addNamespace(NAMESPACE)
    self.assertEqual(self.executor._namespace[VAR1], VALUES1)
    self.assertEqual(self.executor._namespace[VAR2], VALUES2)

  def testDeleteNamespace(self):
    if IGNORE_TEST:
      return
    self.executor.addNamespace(NAMESPACE)
    self.executor.deleteNames([VAR2])
    self.assertFalse(VAR2 in self.executor._namespace)

  def testDoExpression(self):
    namespace = {'a': 1, 'b': 2}
    expression = "a + b"
    self.executor.addNamespace(namespace)
    result = self.executor.doExpression(expression)
    self.assertEqual(result, namespace['a'] + namespace['b'])

  def testDoExpressionException(self):
    namespace = {'a': 1, 'b': 0}
    expression = "a / b"
    self.executor.addNamespace(namespace)
    with self.assertRaises(Exception):
      result = self.executor.doExpression(expression)

  def testDoScript(self):
    namespace = {'a': 1, 'b': 2}
    program = "y = a + b"
    self.executor.addNamespace(namespace)
    self.executor.doScript(program)
    y_value = self.executor._namespace['y']
    self.assertEqual(y_value, namespace['a'] + namespace['b'])

  def testDoScriptException(self):
    namespace = {'a': 1, 'b': 0}
    program = "y = a / b"
    self.executor.addNamespace(namespace)
    with self.assertRaises(Exception):
      result = self.executor.doScript(program)
    

if __name__ == '__main__':
  unittest.main()
