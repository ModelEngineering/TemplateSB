'''Run time for evaluating python codes in template'''


import numpy as np


class Api(object):

  def __init__(self):
    self._definitions = {}

  def addDefinitions(self, name_value_dict):
    """
    :param dict name_value_dict: key is name
    """
    for key, values in name_value_dict.items():
      self._definitions[key] = values

  def removeDefinitions(self, names):
    """
    :param list names: Names to delete
    """
    for name in names:
      del self._definitions[name]

  def getDefinitions(self):
    """
    :return list:
    """
    return self._definitions
