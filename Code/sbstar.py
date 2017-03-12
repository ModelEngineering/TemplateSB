'''Class for processing templates. See README for syntax.'''


ESCAPE_STG = '#!'
PROCESSOR_NAME = "SbStar"
VERSION = '1.0'
SPLIT_STG = "\n"
COMMENT_STG = "#"
CONTINUED_STG = "\\"  # Indicates a continuation follows
VARIABLE_START = "{"
VARIABLE_END = "}"
LINE_TRAN = 1  # Transparent - nothing to process (comment line, no template variable)
LINE_DEFN = 2  # Variable definition - variable definition line
LINE_SUBS = 3  # Substitution line
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

  def __init__(self, substitutions):
    """
    :param list-of-dict substitutions: List of dictionaries in which the 
         key is the target and the value is its replacement
    """
    self._substitutions = substitutions

  @classmethod
  def makeSubstitutionList(cls, definitions,
      left_delim=VARIABLE_START,
      right_delim=VARIABLE_END):
    """
    Creates a list of substitutions from a substitution defintion.
    Suppose that the defintions are the dictionary 
    {'a': ['a1', 'a2'], 'b': ['b1', 'b2', 'b3']}.
    Then a substituion list will be a list of dictionaries, each of which
    has a key for the two targets ('a' and 'b') and every combination of
    value for the keys. Assume the default left and right delimiters. In this case:
      [ {'{a}': 'a1', '{b}': 'b1'}, ['{a}': 'a2', '{b}': 'b1'},
        {'{a}': 'a1', '{b}': 'b2'}, ['{a}': 'a2', '{b}': 'b2'},
        {'{a}': 'a1', '{b}': 'b3'}, ['{a}': 'a2', '{b}': 'b3'}
      ]
    :param dict definitions: key is target name, value is list of replacements
    :param str left_delim: left delimiter for target
    :param str right_delim: right delimiter for target
    :return list-of-dict:
    """
    substitutions = [{}]
    for key in definitions.keys():
      accum_list = []
      for val in definitions[key]:
        # Create an substituion instance for this key and value
        new_list = [dict(d) for d in substitutions]
        tgt = "%s%s%s" % (left_delim, str(key), right_delim)
        [d.update({tgt: val}) for d in new_list]
        accum_list.extend(new_list)
      substitutions = list(accum_list)
    return [d for d in substitutions if len(d.keys()) > 0]

  def replace(self, stg):
    """
    Replaces all instances of target strings in the line,
    eliminating redundant lines.
    :param str stg: string where replacements are done
    :return list-of-str:
    """
    replacements = []
    for substitution_dict in self._substitutions:
      replaced_string = stg
      for target, replc in substitution_dict.items():
        new_string = replaced_string.replace(target, replc)
        replaced_string = new_string
      if not replaced_string in replacements:
        replacements.append(replaced_string)
    if len(replacements) == 0:
      replacements.append(stg)
    return replacements


class SbStar(object):
  """
  This class processes an Antimony model written using template variable substitutions.
  See the project README for syntax details.
  Usage:
    import tellurium as te
    sbstar = Sbstar(template_string)
    expanded_string = sbstar.expand()
    rr = te.loada(expanded_string)
    results = rr.simulate(start, end, samples)
  """

  def __init__(self, template_string):
    self._template_string = template_string
    self._lines = self._template_string.split(SPLIT_STG)
    self._definitions = {}  # Dictionary of template variables and values
    self._substitutions = []  # List of dictionaries of substitutions
    self._lineno = 0
    self._current_line = None  # Complete line extracted from input

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
    except Exception:
      self._errorMsg("Version number not recognized")
    # Valid Variable Definitions line
    definitions = " ".join(tokens[TOKEN_DEFSTART:])
    try:
      self._definitions = eval(definitions)
    except:
      self._errorMsg("Invalid variable definitions.")

  def _makeComment(self, line):
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
    substituter = None
    line = self._getNextLine()
    while line is not None:  # End of input if None
      line_type = self._classifyLine()
      if line_type == LINE_TRAN:
        expansions.append(line)
      elif line_type == LINE_DEFN:
        # Process definitions of template variables
        expansions.append(self._makeComment(line.strip()))
        self._makeVariableDefinitions()
        substitutions = Substituter.makeSubstitutionList(self._definitions)
        substituter = Substituter(substitutions)
      else:
        if substituter is None:
          msg = "Substitution encountered before definition of template variables."
          self._errorMsg(msg)
        # Do the variable substitutions
        expansion = substituter.replace(line)
        is_ok = all([False if (VARIABLE_START in e) 
                     or (VARIABLE_END in e)
                     else True for e in expansion])
        if not is_ok:
          self._errorMsg("Undefined template variable in line.")
        if len(expansion) > 1:
          expansions.append(self._makeComment(line))
        expansions.extend(expansion)
      line = self._getNextLine()
    return "\n".join(expansions)
