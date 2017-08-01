'''Class that objectifies a TemplateSB command'''

"""
These commands are indicated by a line that begins
with {{ and ends with }}.
Supported commands are:
  {{ DefineVariables Begin }}
  {{ DefineVariables End }}
  {{ DefineConstraints Begin }}
  {{ DefineConstraints End }}
  {{ SetVersion <version #> }} - Specifies the version number
"""

from constants import COMMAND_START, COMMAND_END

class Command(object):
  """
  Knows how to parse command lines for the template processor.
  Provides an interface to determine the command.
  """
  DEFINE_VARIABLES = "DefineVariables"
  DEFINE_CONSTRAINTS = "DefineConstraints"
  SET_VERSION = "SetVersion"
  
  def __init__(self, command_line):
    """
    :param str command_line: line with the command
    """
    self._command_line = command_line
    self._start = False
    self._end = False
    self._arguments = []  # List of arguments following the command
    self._tokens = []
    parsed_line = command_line.split()
    if (parsed_line[0] == COMMAND_START)  \
        and (parsed_line[-1] == COMMAND_END):
      self._tokens = parsed_line[1:-1]
      self._parseCommand()
    else:
      raise ValueError("Invalid command line")

  @classmethod
  def _extractArguments(cls, tokens, pos, count):
    """
    Extracts the number of arguments from the tokens
    :param list-of-str tokens:
    :param int pos: position to start finding arguments
    :param int count:
    :return list_of_str:
    """
    arguments = []
    msg = None
    if len(tokens) != pos + count:
      msg = "Expected %d argument(s)" % count
    else:
      if len(tokens[pos:]) == count:
        arguments = tokens[1:count+1]
      else:
        msg = "Expected %d argument(s)" % count
    if msg is not None:
      raise ValueError(msg)
    return arguments

  def _parsePairedCommands(self, command_verb, num_args=0):
    """
    Parses commands that are paired with Start and End
    :param str command_verb:
    :param int num_args: number of arguments in command
    """
    cls = Command
    if self._tokens[0] == command_verb:
      self._command_verb = command_verb
      if len(self._tokens) < 2:
        raise ValueError("Exactly qualifier is required for %s"
            % self._tokens[0])
      if self._tokens[1] == "Start":
        self._start = True
      elif self._tokens[1] == "End":
        self._end = True
      else:
        raise ValueError("Unknown command qualifier %s"  \
            % self._tokens[1])
      self._arguments = cls._extractArguments(self._tokens,
          2, num_args)
      is_parsed = True
    else:
      is_parsed = False
    return is_parsed

  def _parseUnpairedCommands(self, command_verb, num_args):
    """
    Parses commands that are paired with Start and End
    :param str command_verb:
    :param int num_args: number of arguments in command
    """
    cls = Command
    if self._tokens[0] == command_verb:
      self._command_verb = command_verb
      self._arguments = cls._extractArguments(self._tokens,
         1, num_args)
      is_parsed = True
    else:
      is_parsed = False
    return is_parsed

  def _parseCommand(self):
    """
    Populates the state for the command
    """
    cls = Command
    if self._parsePairedCommands(cls.DEFINE_VARIABLES):
      pass
    elif self._parsePairedCommands(cls.DEFINE_CONSTRAINTS):
      pass
    elif self._parseUnpairedCommands(cls.SET_VERSION, 1):
      pass
    else:
      raise ValueError("Unknown command %s" % self._tokens[0])

  def __str__(self):
    return self._command_line

  def isDefineVariables(self):
    cls = Command
    return self._command_verb == cls.DEFINE_VARIABLES

  def isDefineConstraints(self):
    cls = Command
    return self._command_verb == cls.DEFINE_CONSTRAINTS

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
