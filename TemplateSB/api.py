'''Run time for evaluating python codes in template'''


import numpy as np


class Api(object):

  def __init__(self):
    self._namespace = {}
    self._definitions = {}
    self._constraints = []
    self._primaries = {}

  def addDefinitions(self, name_value_dict, primary=None):
    """
    :param dict name_value_dict: key is name
    :param str primary: the values in this dictionary
       should be 'aligned' with the primary
    """
    for key, values in name_value_dict.items():
      self._definitions[key] = values
    if primary is None:
      self._primaries[primary] = []
    if primary is not None:
      lengths = [len(v) for v in name_value_dict(k) for v,k in name_value_dict]
      if np.std(lengths) != 0:
        raise ValueError("Non-None primary but non-equal length variables")
      for key in name_value_dict:
        self._primaries[primary].append(key)

  def getDefinitions(self):
    """
    :return list:
    """
    return self._definitions
