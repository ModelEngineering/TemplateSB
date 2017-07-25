'''Class for processing templates. See README for syntax.'''

"""
Parses text to expand based on values of template variables.
Lines:
  Begins with {{ - starts an escape of python code
  Begins with }} - ends an escape of python code

Notes
  1. Define a template variable as being without the '{}'
    a. Change subtituter
    b. Change expand
  2. Can't do implicit definitions if have expressions?

1. Test getTemplateExpressions (substituter)
2. Evaluate template expressions and extend the set of substitions
   done by the substituter?
"""

from api import Api
import re
import fileinput
import sys


ESCAPE_START = "{{"
ESCAPE_END = "}}"
VERSION = '1.1'
SPLIT_STG = "\n"
COMMENT_STG = "#"
CONTINUED_STG = "\\"  # Indicates a continuation follows
VARIABLE_START = "{"
VARIABLE_END = "}"
LINE_TRAN = 1  # Transparent - nothing to process (comment line, no template variable)
LINE_SUBS = 3  # Substitution line
LINE_CODE_START = 4  # Starts a code escape
LINE_CODE_END = 5
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
    """
    :param str template_string: string containing template variables
        and template escape statements to execute
    """
    self._template_string = template_string
    self._lines = self._template_string.split(SPLIT_STG)
    self._definitions = {}  # Dictionary of template variables and values
    self._lineno = 0
    self._current_line = None  # Complete line extracted from input
    self._api = Api()
    self._namespace = {'api': self._api}

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
      LINE_SUBS: Substitution line
      LINE_CODE_START: Start a code escape
      LINE_CODE_END: End a code escape
    State used:
      reads: _current_line
    :return int: see LINE_* for interpretation
    """
    text = self._current_line.strip()
    if len(text) == 0:
      result = LINE_TRAN
    elif text[0] == COMMENT_STG or len(text) == 0:
      result = LINE_TRAN
    elif text[0:2] == ESCAPE_START:
      result = LINE_CODE_START
    elif text[0:2] == ESCAPE_END:
      result = LINE_CODE_END
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

  def _getNextLine(self, strip=True):
    """
    Gets the next line, handling continued lines.
    State used:
      reads: _lineno, _lines
      writes: _current_line, _lineno
    :parm bool strip: flag to indicate if white space should be stripped
    :sideeffects: self._current_line, self._lineno
    :return str: Current line with continuations
    """
    self._current_line = None
    while self._lineno < len(self._lines):
      if self._current_line is None:
        self._current_line = ""
      if strip:
        text = self._lines[self._lineno].strip()
      else:
        text = self._lines[self._lineno]
      self._lineno += 1
      if len(text) == 0:
        continue
      if text[-1] == CONTINUED_STG:
        self._current_line = self._current_line + text[0:-1]
      else:
        self._current_line = self._current_line + text
        break
    return self._current_line

  @staticmethod
  def _makeComment(line):
    return "%s%s" % (COMMENT_STG, line)

  def _execute_statements(self, statements):
    """
    Executes the statements and updates the variable
    definitions.
    :param list-of-str statements:
    """
    program = '\n'.join(statements)
    try:
      exec(program, self._namespace)
    except Exception as e:
      msg = "***Error %s executing:\n %s" % (e.message, program)
      raise ValueError(msg)
    self._definitions = self._namespace['api'].getDefinitions()

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
    statements = []
    is_escape = False
    while line is not None:  # End of input if None
      line_type = self._classifyLine()
      if is_escape:
        if line_type == LINE_CODE_END:
          is_escape = False
          self._execute_statements(statements)  # updates self._definitions
          statements = []
          substituter = Substituter(self._definitions)
          expansions.append(TemplateSB._makeComment(line))
        else:
          statements.append(line)
          expansions.append(TemplateSB._makeComment(line))
      # Not a code escape
      else:
        if line_type == LINE_TRAN:
          expansions.append(line)
        elif line_type == LINE_CODE_START:
          is_escape = True
          expansions.append(TemplateSB._makeComment(line))
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
      line = self._getNextLine(strip= not is_escape)
    return "\n".join(expansions)

  def get(self):
    """
    :return str: template
    """
    return self._template_string
