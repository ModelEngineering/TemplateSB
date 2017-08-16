'''Class that does string expansion using template expressions.'''

from constants import EXPRESSION_START, EXPRESSION_END,  \
    WARNING_ASSIGNMENTS
import re


class Expander(object):
  """
  This class makes expands a string with template expressions,
  an expression of template variables, based on the possible
  values of the template variables. The resulting expansion
  consists of multiple strings, one for each combination of
  the values of the template variables.
  """

  def __init__(self, executor, message,
       left_delim=EXPRESSION_START, right_delim=EXPRESSION_END):
    """
    :param Executor executor:
    :param StatusMessage message:
    :param char left_delim: left delimiter for a template expression
    :param char right_delim: right delim for a template expression
    """
    self._executor = executor
    self._message = message
    self._left_delim = left_delim
    self._right_delim = right_delim

  @classmethod
  def makeSubstitutionList(cls, definitions):
    """
    Creates a list of dictionaries that constitute the combinations
    of assignment of values to the template variables.
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
        # Create a substituion for this key and value
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
    raw_expressions = set(pat.findall(stg))
    expressions = [e[1:-1].strip() for e in raw_expressions]
    return expressions
      
  def do(self, segment):
    """
    Creates a set of substitutions of template expressions using the
    values of template variables.
    Eliminates redundant lines.
    :param str segment: segment of the template; may be multiple lines
    :return list-of-str:
    :raises ValueError: if not all template expressions are eliminated
    """
    substitutions = []
    cls = Expander
    # Create the combinations of assignments of values to variables
    definitions = self._executor.getDefinitions()
    assignments = cls.makeSubstitutionList(definitions)
    if len(assignments) > WARNING_ASSIGNMENTS:
      msg = "Number of assignments is %d!" % len(assignments)
      self._message.warning(msg)
    expressions = self.getTemplateExpressions(segment)
    for assignment in assignments:
      self._executor.addNamespace(assignment)
      substitution = segment
      for expression in expressions:
        target = "%s%s%s" % (self._left_delim,
            expression, self._right_delim)
        replacement = self._executor.doExpression(expression)
        new_string = substitution.replace(target, str(replacement))
        substitution = new_string
      if substitution not in substitutions:
        substitutions.append(substitution)
    # Remove the added names
    self._executor.deleteNames(definitions.keys())
    # Handle case of no template variable in segment
    if len(substitutions) == 0:
      substitutions = [segment]
    # Verify there are no remaining template variables
    for substitution in substitutions:
      if len(self.getTemplateExpressions(substitution)) > 0:
        raise ValueError("Unresolved template expressions in %s"
            % segment)
    return substitutions
