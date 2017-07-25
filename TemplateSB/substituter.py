'''Class for doing expression substitution.'''

import re

VARIABLE_START = "{"
VARIABLE_END = "}"

class Substituter(object):
  """
  This class makes string substitutions for a set of targets and
  replacement values. Multiple instances of replacement values are
  considered for each target.
  """

  def __init__(self, definitions,
       left_delim=VARIABLE_START, right_delim=VARIABLE_END):
    """
    :param dict definitions: key is the string to replace, values are the substitutions
    :param char left_delim:
    :param char right_delim:
    """
    self._definitions = definitions
    self._left_delim = left_delim
    self._right_delim = right_delim
    self._input_state = INPUT_STATE_TEXT

  @classmethod
  def makeSubstitutionList(cls, definitions):
    """
    Creates a list of substitutions from a substitution defintion.
    Suppose that the defintions are the dictionary
    {'a': ['a1', 'a2'], 'b': ['b1', 'b2', 'b3']}.
    Then a substituion list will be a list of dictionaries, each of which
    has a key for the two targets ('a' and 'b') and every combination of
    value for the keys. Assume the default left and right delimiters. In this case:
      [ {'a': 'a1', 'b': 'b1'}, ['a': 'a2', 'b': 'b1'},
        {'a': 'a1', 'b': 'b2'}, ['a': 'a2', 'b': 'b2'},
        {'a': 'a1', 'b': 'b3'}, ['a': 'a2', 'b': 'b3'}
      ]
    :param dict definitions: key is target name, value is list of replacements
    :return list-of-dict:
    """
    substitutions = [{}]
    for key in definitions.keys():
      accum_list = []
      for val in definitions[key]:
        # Create an substituion instance for this key and value
        new_list = [dict(d) for d in substitutions]
        tgt = key
        _ = [d.update({tgt: val}) for d in new_list]
        accum_list.extend(new_list)
      substitutions = list(accum_list)
    return [d for d in substitutions if len(d.keys()) > 0]

  def getTemplateExpressions(self, stg):
    """
    Finds the template expressions in the string, 
    the strings between the template delimiters.
    :param str stg: string to process
    :return list-of-str: Unique template expressions without delimiters
    """
    # Single template variable
    pattern_str = "\%s[^%s]+\%s"  \
       % (self._left_delim, self._left_delim, self._right_delim)
    pat = re.compile(pattern_str)  # Single template variable
    raw_expressions = pat.findall(stg)
    for expression in raw_expressions:
      expression = expression[1:-1]
    expressions = [x for x in set(raw_expressions)]
    return expressions
      
  def replace(self, stg):
    """
    Replaces all instances of target strings in the line,
    eliminating redundant lines.
    :param str stg: string where replacements are done. includes delimiter.
    :return list-of-str:
    """
    replacements = []
    cls = Substituter
    substitutions = cls.makeSubstitutionList(self._definitions)
    for substitution_dict in substitutions:
      replaced_string = stg
      for target, replc in substitution_dict.items():
        full_target = "%s%s%s" % (self._left_delim,
            target, self._right_delim)
        new_string = replaced_string.replace(full_target, replc)
        replaced_string = new_string
      if replaced_string not in replacements:
        replacements.append(replaced_string)
    if len(replacements) == 0:
      replacements.append(stg)
    return replacements
