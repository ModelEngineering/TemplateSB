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
"""

from executor import Executor
from command import Command, COMMAND_START, COMMAND_END
from expander import Expander
from constants import EXPRESSION_START, EXPRESSION_END,  \
  VERSION, SPLIT_STG, COMMENT_STG,  \
  CONTINUED_STG, LINE_TRAN, LINE_COMMAND, LINE_SUBS, LINE_NONE
from line_extractor import LineExtractor
import fileinput
import sys


class TemplateProcessor(object):
  """
  This class processes an Antimony model written using template variable substitutions.
  See the project README for syntax details.
  """
  def __init__(self, template_string):
    """
    :param str template_string: string containing template variables
        and template escape statements to execute
    """
    self._extractor = LineExtractor(template_string)
    self._executor = Executor()
    self._expander = Expander(self._executor)
    self._command = None  # Command being processed
    self._define_variable_statements = []
    self._define_constraints_statements = []

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

  def _errorMsg(self, msg):
    """
    :param str msg:
    :raises ValueError:
    """
    error = "on line %d.\n'%s'\nError message: %s"  \
        % (self._extractor.getCurrentSourceLineNumber(), 
           self._extractor.getCurrentLine(), msg)
    raise ValueError(error)

  @staticmethod
  def _makeComment(line):
    return "%s%s" % (COMMENT_STG, line)

  def _processCommand(self):
    """
    Handles command processing, either the current line
    is a command or in the midst of processing a paired command.
    :param list-of-str expansion:
    :return bool: True if processed line
    """
    line = self._extractor.getCurrentLine()
    line_type = self._extractor.getCurrentLineType()
    is_processed = False
    # Current line is a command
    if line_type == LINE_COMMAND:
      is_processed = True
      # Check for nested commands
      if self._command is not None:
        new_command = Command(line)
        # Is this a paired command?
        if new_command.getCommandVerb()  \
            == self._command.getCommandVerb():
          if new_command.isEnd():
            pass
          else:
            self._errorMsg("Cannot nest commands")
      # Valid placement for a command.
      self._command = Command(line)
      # DefineVariables Command
      if self._command.isDefineVariables():
        if self._command.isBegin():
          self._define_variables_statements = []
        elif self._command.isEnd():
          try:
            program = '\n'.join(self._define_variables_statements)
            self._executor.doScript(program)
          except Exception as err:
            msg = "***Error %s executing on line %d:\n%s"  \
                % (err.msg, err.lineno, program)
            self._errorMsg(msg)
          self._command = None
      # SetVersion command
      elif self._command.isSetVersion():
        version = self._command.getArguments()[0]
        if float(version) > VERSION:
          self._errorMsg("Unsupported version %s" % version)
        self._command = None
      # Other commands
      else:
        self._errorMsg("Unknown command")
    # Process statements occurring within paired commands
    elif self._command is not None:
      is_processed = True
      if self._command.isDefineVariables() and self._command.isBegin():
        self._define_variables_statements.append(line)
      elif self._command.isDefineConstraints() and self._command.isBegin():
        self._define_constraints_statements.append(line)
      else:
        self._errorMsg("Invalid paired command.")
    return is_processed

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
    expansion = []
    line, line_type = self._extractor.do()
    statements = []
    while line is not None:
      if self._processCommand():
        expansion.append(cls._makeComment(line))
      # No command being processed
      else:
        # Transparent line (comment)
        if line_type == LINE_TRAN:
          expansion.append(line)
        elif line_type == LINE_NONE:
          pass
        # Line to be substituted
        elif line_type == LINE_SUBS:
          # Do the variable substitutions
          try:
            substitutions = self._expander.do(line)
          except Exception as err:
            msg = "Runtime error in expression"
            self._errorMsg(msg)
          if len(substitutions) > 1:
            expansion.append(cls._makeComment(line))
          expansion.extend(substitutions)
        else:
          import pdb; pdb.set_trace()
          raise RuntimeError("Unexepcted state")
      line, line_type = self._extractor.do()
    if self._command is not None:
      msg = "Still processing command %s at EOF" % str(self._command)
      self._errorMsg(msg)
    return "\n".join(expansion)
