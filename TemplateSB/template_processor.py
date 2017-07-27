'''Class for processing templates. See README for syntax.'''

"""
Parses text to expand based on values of template expressions.
A template expression is indicated by text enclosed in
"{" and "}". Variables are defined in Python codes
in the Python escape (see below).

Python code is used to define variables used in template expressions.
This is done with the object api that supports the following
methods:
  api.addDefinitions(<dict>) - <dict> is a dictionary with
     the variable name as key and its values are the possible
     values that can be assigned to the variable.

Notes
  1. Define a template variable as being without the '{}'
    a. Change subtituter
    b. Change expand
  2. Can't do implicit definitions if have expressions?

Command lines:
1. Completed code changes
2. Test
   a. Test new methods
   b. classify line operates differently
   c. use command line structure instead of code escape

1. Test getTemplateExpressions (expander)
2. Evaluate template expressions and extend the set of substitions
   done by the expander?
"""

from api import Api
from command import Command, COMMAND_START, COMMAND_END
from expander import Expander, EXPRESSION_START,  \
    EXPRESSION_END
import fileinput
import sys


VERSION = "1.1"
SPLIT_STG = "\n"
COMMENT_STG = "#"
CONTINUED_STG = "\\"  # Indicates a continuation follows
LINE_TRAN = 1  # Transparent - nothing to process (comment line, no template variable)
LINE_COMMAND = 2  # Command line
LINE_SUBS = 3  # Line to be processed for substitutions
 

class TemplateProcessor(object):
  """
  This class processes an Antimony model written using template variable substitutions.
  See the project README for syntax details.
  Usage:
    import tellurium as te
    templatesb = Sbstar(template_string)
    expanded_string = templatesb.do()
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
    self._command = None  # Command being processed

  @classmethod
  def processFile(cls, inpath, outpath):
    """
    Processes template strings in a file.
    :param str inpath: path to the file containing the templated model
    :param str outpath: path to the file where the flattened model is placed
    """
    template = ''
    with open(inpath, 'r') as infile:
      for line in infile:
        template += "\n" + line
    processor = cls(template)
    expansion = processor.do()
    with open(outpath, 'w') as outfile:
      outfile.write(expansion)

  def _classifyLine(self):
    """
    Classifies a line as:
      LINE_TRAN: Transparent - nothing to process (comment line, no template variable)
      LINE_SUBS: Substitution line
      LINE_COMMAND: Template processor command
    State used:
      reads: _current_line
    :return int: see LINE_* for interpretation
    """
    text = self._current_line.strip()
    if len(text) == 0:
      result = LINE_TRAN
    elif text[0] == COMMENT_STG or len(text) == 0:
      result = LINE_TRAN
    elif text[0:2] == COMMAND_START:
      result = LINE_COMMAND
    elif text.count(EXPRESSION_START) == 0 and  \
        text.count(EXPRESSION_END) == 0:
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
      references: _lineno, _lines
      updates: _current_line, _lineno
    :parm bool strip: flag to indicate if white space should be stripped
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

  def do(self):
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
    cls = TemplateProcessor
    expansions = []
    expander = Expander({})
    line = self._getNextLine()
    statements = []
    while line is not None:  # End of input if None
      line_type = self._classifyLine()
      # Handlie line specially if there is a command in effect
      # Paired commands (e.g., Start, End pairs) use self._command
      # as state to indicate that they are in a command block.
      if line_type == LINE_COMMAND:
        if self._command is not None:
          new_command = Command(line)
          if new_command.getCommandVerb()  \
              == self._command.getCommandVerb():
            if new_command.isEnd():
              self._command = Command(line)
            else:
              self._errorMsg("Cannot nest commands")
        else:
          self._command = Command(line)
      if self._command is not None:
        # Accumulate python codes to execute
        if self._command.isExecutePython():
          if self._command.isStart():
            if line_type != LINE_COMMAND:
              statements.append(line)
            expansions.append(cls._makeComment(line))
          elif self._command.isEnd():
            self._execute_statements(statements)  # updates self._definitions
            statements = []
            expander = Expander(self._definitions)  # Reflect updates from Python
            expansions.append(cls._makeComment(line))
            self._command = None
          else:
            raise RuntimeError("Unexepcted state")
        # SetVersion command
        elif self._command.isSetVersion():
          version = self._command.getArguments()[0]
          if float(version) > VERSION:
            self._errorMsg("Unsupported version %s" % version)
          self._command = None
        # Other commands
        else:
          self._errorMsg("Unknown command")
      # No command being processed
      else:
        # Transparent line (comment)
        if line_type == LINE_TRAN:
          expansions.append(line)
        # Line to be substituted
        elif line_type == LINE_SUBS:
          # Do the variable substitutions
          expansion = expander.do(line)
          is_ok = all([False if (EXPRESSION_START in e)
                       or (EXPRESSION_END in e)
                       else True for e in expansion])
          if not is_ok:
            msg = "Undefined template variable in line:\n%s" % line
            self._errorMsg(msg)
          if len(expansion) > 1:
            expansions.append(cls._makeComment(line))
          expansions.extend(expansion)
        else:
          raise RuntimeError("Unexepcted state")
      line = self._getNextLine(strip=(self._command is None))
    if self._command is not None:
      msg = "Still processing command %s at EOF" % str(self._command)
      self._errorMsg(msg)
    return "\n".join(expansions)

  def get(self):
    """
    :return str: template
    """
    return self._template_string
