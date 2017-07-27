'''Evaluates expressions in a namespace.'''

class ExpressionEvaluator(object):

  def __init__(self, namespace):
    self._namespace = namespace

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

  def do(self, expression):
    """
    Evaluates the expression in the namespace, returning
    the result.
    """
    result = eval(expression, self._namespace)
    return result
