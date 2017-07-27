'''Class that objectifies a TemplateSB command'''

"""
These commands are indicated by a line that begins
with {{ and ends with }}.
Supported commands are:
  {{ ExecutePython Begin }} - begins a sequence of python codes to execute
  {{ ExecutePython End }} - ends a sequence of python codes to execute
  {{ SetVersion <version #> }} - Specifies the version number
"""

COMMAND_START = "{{"
COMMAND_END = "}}"

class Command(object):
  """
  Knows how to parse command lines for the template processor.
  Provides an interface to determine the command.
  """
  EXECUTE_PYTHON = 1
  SET_VERSION = 2
  
  def __init__(self, command_line):
    """
    :param str command_line: line with the command
    """
    self._command_line = command_line
    self._start = False
    self._end = False
    self._arguments = None  # List of arguments following the command
    self._tokens = []
    parsed_line = command_line.split()
    if (parsed_line[0] == COMMAND_START)  \
        and (parsed_line[-1] == COMMAND_END):
      self._tokens = parsed_line[1:-1]
      self._populateState()
    else:
      raise ValueError("Invalid command line")

  def _populateState(self):
    """
    Populates the state for the command
    """
    cls = Command
    if self._tokens[0] == "ExecutePython":
      self._command_verb = cls.EXECUTE_PYTHON
      if len(self._tokens) != 2:
        raise ValueError("Exactly one qualifier is required for %s"
            % self._tokens[0])
      if self._tokens[1] == "Start":
        self._start = True
      elif self._tokens[1] == "End":
        self._end = True
      else:
        raise ValueError("Unknown command qualifier %s"  \
            % self._tokens[1])
    elif self._tokens[0] == "SetVersion":
      self._command_verb = cls.SET_VERSION
      self._arguments = self._tokens[1:]
      if len(self._arguments) != 1:
        raise ValueError("Only one argument for SetVersion")
    else:
      raise ValueError("Unknown command %s" % self._tokens[0])

  def __str__(self):
    return self._command_line

  def isExecutePython(self):
    cls = Command
    return self._command_verb == cls.EXECUTE_PYTHON

  def isStart(self):
    return self._start

  def isEnd(self):
    return self._end

  def isSetVersion(self):
    cls = Command
    return self._command_verb == cls.SET_VERSION

  def getArguments(self):
    return self._arguments

  def getCommandVerb(self):
    return self._command_verb
