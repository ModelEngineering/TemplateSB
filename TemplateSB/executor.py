'''Evaluates expressions in a namespace.'''

from api import Api

class Executor(object):
  """
  Executes statements and expressions.
  Manages the name space and access to definitions.
  """

  def __init__(self):
    self._api = Api()
    self._namespace = {'api': self._api}

  def addNamespace(self, namespace):
    """
    Adds the names in the namespace to the current namespace.
    :param dict namepsace:
    """
    for name in namespace.keys():
      self._namespace[name] = namespace[name]

  def deleteNames(self, names):
    """
    Removes the names in the namespace to the current namespace.
    :param list-of-str names:
    """
    for name in names:
      del self._namespace[name]

  def doExpression(self, expression):
    """
    Evaluates the expression in the namespace, returning
    the result.
    :param str expression: python expression
    """
    result = eval(expression, self._namespace)
    return result

  def doScript(self, program):
    """
    Evaluates a program consisting of one or more statements.
    :param str program:
    """
    exec(program, self._namespace)

  def getDefinintions(self):
    """
    :return dict: Variable definitions
    """
    return self._namespace['api'].getDefinitions()

