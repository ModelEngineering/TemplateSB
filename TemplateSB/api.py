'''Run time for evaluating python codes in template'''


class Api(object):

  def __init__(self):
    self._namespace = {}
    self._definitions = {}
    self._constraints = []
    self._primaries = {}

  def addDefinition(self, name, values, primary=None):
    """
    :param str name: name being defined
    :param list values: values assignable to the name
    :param str primary: variable that is used to
       aligned this variable
    """
    self._definitions[name] = values
    if primary is None:
      self._primaries[primary] = []
    if primary is not None:
      if len(self._definitions[primary])  \
          != len(self._definitions[name]):
        raise ValueError("Length mismatch between %s and %s"
            % (name, dependent))
      self._primaries[primary].append(name)

  def getDefinitions(self):
    """
    :return list:
    """
    return self._definitions
