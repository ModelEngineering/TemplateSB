'''Class for processing templates. See README for syntax.'''

"""
1. Completed draft of code for implicit definitions
2. Tests for different parsing cases
"""

import re
import fileinput
import sys


ESCAPE_STG = '#!'
PROCESSOR_NAME = "TemplateSB"
VERSION = '1.1'
SPLIT_STG = "\n"
COMMENT_STG = "#"
CONTINUED_STG = "\\"  # Indicates a continuation follows
VARIABLE_START = "{"
VARIABLE_END = "}"
LINE_TRAN = 1  # Transparent - nothing to process (comment line, no template variable)
LINE_DEFN = 2  # Variable definition - variable definition line
LINE_SUBS = 3  # Substitution line
SEP = ","  # Separator for template variables
TOKEN_ESCAPE = 0
TOKEN_PROCESSOR = 1
TOKEN_VERSION = 3
TOKEN_DEFSTART = 4


class Substituter(object):
  """
  This class makes string substitutions for a set of targets and
  replacement values. Multiple instances of replacement values are
  considered for each target.
  """

  def __init__(self, definitions):
    """
    :param dict definitions: key is the string to replace, values are the substitutions
    """
    self._definitions = definitions

  @classmethod
  def makeSubstitutionList(cls, definitions):
    """
    Creates a list of substitutions from a substitution defintion.
    Suppose that the defintions are the dictionary
    {'{a}': ['a1', 'a2'], '{b}': ['b1', 'b2', 'b3']}.
    Then a substituion list will be a list of dictionaries, each of which
    has a key for the two targets ('a' and 'b') and every combination of
    value for the keys. Assume the default left and right delimiters. In this case:
      [ {'{a}': 'a1', '{b}': 'b1'}, ['{a}': 'a2', '{b}': 'b1'},
        {'{a}': 'a1', '{b}': 'b2'}, ['{a}': 'a2', '{b}': 'b2'},
        {'{a}': 'a1', '{b}': 'b3'}, ['{a}': 'a2', '{b}': 'b3'}
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

  def _getTemplateVariables(self, stg, 
       left_delim=VARIABLE_START, right_delim=VARIABLE_END):
    """
    Finds the template variables in the line, those variables between 
    the delimiters.
    :param str stg:
    :param char left_delim:
    :param char right_delim:
    :return list-of-str:
    """
    pattern_str = "\%s[\w\s,]+\%s" % (left_delim, right_delim)  # Single template variable
    pat = re.compile(pattern_str)  # Single template variable
    raw_strings = pat.findall(stg)
    raw_variables =  \
        [r.strip().replace(' ', '')  for r in raw_strings]
    variables = [x for x in set(raw_variables)]
    return variables

  def _updateDefinitions(self, stg):
    """
    Creates the dictionary definition the implicit substitutions for the template variables.
    There are two cases. First, there is no comma in the variable name, such as
    {ll}. In this case, the substituitions are either "ll" or "".
    The second case is there is a list of values, such as "{1,3,55a}". Here
    the substions are are "1", "3", and "55a".
    :param str stg: line to be parsed
    """
    template_variables = self._getTemplateVariables(stg)
    result = {}
    for var in template_variables:
      # Ignore the variable if it is already defined
      if var in self._definitions.keys():
        continue
      trim_var = var[1:-1]
      # Not already definied
      if trim_var.find(SEP) > -1:
        # Is a list
        values = trim_var.split(SEP)
      else:
        # Singleton value
        values = [trim_var, ""]
      result[var] = values
    self._definitions.update(result)
      
  def replace(self, stg):
    """
    Replaces all instances of target strings in the line,
    eliminating redundant lines.
    :param str stg: string where replacements are done
    :return list-of-str:
    """
    replacements = []
    cls = Substituter
    self._updateDefinitions(stg)
    substitutions = cls.makeSubstitutionList(self._definitions)
    for substitution_dict in substitutions:
      replaced_string = stg
      for target, replc in substitution_dict.items():
        new_string = replaced_string.replace(target, replc)
        replaced_string = new_string
      if replaced_string not in replacements:
        replacements.append(replaced_string)
    if len(replacements) == 0:
      replacements.append(stg)
    return replacements

class TemplateSB(object):
  """
  This class processes an Antimony model written using template variable substitutions.
  See the project README for syntax details.
  Usage:
    import tellurium as te
    templatesb = Sbstar(template_string)
    expanded_string = templatesb.expand()
    rr = te.loada(expanded_string)
    results = rr.simulate(start, end, samples)
  """
  def __init__(self, template_string):
    self._template_string = template_string
    self._lines = self._template_string.split(SPLIT_STG)
    self._definitions = {}  # Dictionary of template variables and values
    self._lineno = 0
    self._current_line = None  # Complete line extracted from input

  @classmethod
  def processFile(cls, inpath, outpath):
    """
    Processes template strings in a file.
    :param str inpath: path to the file containing the templated model
    :param str outpath: path to the file where the flattened model is placed
    """
    template_stg = ''
    with open(inpath, 'r') as infile:
      for line in infile:
        template_stg += "\n" + line
    templatesb = cls(template_stg)
    expanded_stg = templatesb.expand()
    with open(outpath, 'w') as outfile:
      outfile.write(expanded_stg)

  def _classifyLine(self):
    """
    Classifies a line as:
      LINE_TRAN: Transparent - nothing to process (comment line, no template variable)
      LINE_DEFN: Variable definition - variable definition line
      LINE_SUBS: Substitution line
    State used:
      reads: _current_line
    :return int: see LINE_* for interpretation
    """
    text = self._current_line.strip()
    if len(text) == 0:
      result = LINE_TRAN
    elif text[0:len(ESCAPE_STG)] == ESCAPE_STG:
      result = LINE_DEFN
    elif text[0] == COMMENT_STG or len(text) == 0:
      result = LINE_TRAN
    elif text.count(VARIABLE_START) == 0 and  \
        text.count(VARIABLE_END) == 0:
      result = LINE_TRAN
    else:
      result = LINE_SUBS
    return result

  def _errorMsg(self, msg):
    """
    :param str msg:
    :raises ValueError:
    """
    error = "on line %d. %s" % (self._lineno, msg)
    raise ValueError(error)

  def _getNextLine(self):
    """
    Gets the next line, handling continued lines.
    State used:
      reads: _lineno, _lines
      writes: _current_line, _lineno
    :sideeffects: self._current_line, self._lineno
    :return str: Current line with continuations
    """
    self._current_line = None
    while self._lineno < len(self._lines):
      if self._current_line is None:
        self._current_line = ""
      text = self._lines[self._lineno].strip()
      self._lineno += 1
      if len(text) == 0:
        continue
      if text[-1] == CONTINUED_STG:
        self._current_line = self._current_line + text[0:-1]
      else:
        self._current_line = self._current_line + text
        break
    return self._current_line

  def _makeVariableDefinitions(self):
    """
    Extract the variable definitions from the input.
    State used:
      reads: _current_line
      writes: _definitions
    :sideeffects self._definitions:
    """
    tokens = self._current_line.split(' ')
    if tokens[TOKEN_ESCAPE] != ESCAPE_STG:
      raise RuntimeError("Not a variable definition line.")
    if tokens[TOKEN_PROCESSOR] != PROCESSOR_NAME:
      self._errorMsg("Could not find template processor")
    version = tokens[TOKEN_VERSION]
    try:
      if float(version) > float(VERSION):
        self._errorMsg("Version number not recognized")
    except ValueError:
      self._errorMsg("Version number not recognized")
    # Valid Variable Definitions line
    definitions = " ".join(tokens[TOKEN_DEFSTART:])
    # Verify that this is a valid Python dict
    try:
      #pylint: disable=W0123
      self._definitions = eval(definitions)
    #pylint: disable=W0703
    except Exception:
      self._errorMsg("Invalid variable definitions.")
    # Verify the format of the template variables
    for key in self._definitions.keys():
      if not key[0] == VARIABLE_START or  \
          not key[-1] == VARIABLE_END:
        msg = "Template variable '%s' must be enclosed in %s, %s"  \
            % (key, VARIABLE_START, VARIABLE_END)
        self._errorMsg(msg)

  @staticmethod
  def _makeComment(line):
    return "%s%s" % (COMMENT_STG, line)

  def expand(self):
    """
    Processes the template string and returns the expanded lines for input
    to road runner.
    Phases
      1. Construct content lines (non-blank, not comments)
      2. Extract the template variable definitions
      3. Construct the substitution instances
      4. Process the lines with template variables
    State used:
      reads: _definitions
    :return str expanded_string:
    :raises ValueError: errors encountered in the template string
    """
    expansions = []
    substituter = Substituter({})
    line = self._getNextLine()
    while line is not None:  # End of input if None
      line_type = self._classifyLine()
      if line_type == LINE_TRAN:
        expansions.append(line)
      elif line_type == LINE_DEFN:
        # Process definitions of template variables
        expansions.append(TemplateSB._makeComment(line.strip()))
        self._makeVariableDefinitions()
        substituter = Substituter(self._definitions)
      else:
        # Do the variable substitutions
        expansion = substituter.replace(line)
        is_ok = all([False if (VARIABLE_START in e)
                     or (VARIABLE_END in e)
                     else True for e in expansion])
        if not is_ok:
          msg = "Undefined template variable in line:\n%s" % line
          self._errorMsg(msg)
        if len(expansion) > 1:
          expansions.append(TemplateSB._makeComment(line))
        expansions.extend(expansion)
      line = self._getNextLine()
    return "\n".join(expansions)

  def get(self):
    """
    :return str: template
    """
    return self._template_string
