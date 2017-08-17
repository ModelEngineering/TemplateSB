'''Constants used in TemplateSB.'''

import yaml


# The following constants are specified in the config file
COMMAND_START = None
COMMAND_END = None
COMMENT_STG = None
CONTINUED_STG = None
EXPRESSION_START = None
EXPRESSION_END = None
SPLIT_STG = None
# Number of definitions before a warning is generated
WARNING_ASSIGNMENTS = 10000

# The following constants are internal
CONFIG_FILE_PATH = "../config.yaml"
LINE_COMMAND = 2  # Command line
LINE_NONE = -1  # Command line
LINE_SUBS = 3  # Line to be processed for substitutions
LINE_TRAN = 1  # Transparent - nothing to process (comment line, no template variable)
LINE_NONE = -1 # No more lines
# Version of code
VERSION = "1.2"


def setConstantsFromConfig(path=CONFIG_FILE_PATH):
  fd = open(path, "r")
  lines = ''.join(fd.readlines())
  fd.close()
  config_dict = yaml.load(lines)
  for key, value in config_dict.items():
    if key == "command_start":
      COMMAND_START = value
    elif key == "command_end":
      COMMAND_END = value
    elif key == "comment_character":
      COMMENT_STG = value
    elif key == "continuation_string":
      CONTINUED_STG = value
    elif key == "expression_start":
      EXPRESSION_START = value
    elif key == "expression_end":
      EXPRESSION_END = value
    elif key == "warn_assignments":
      WARNING_ASSIGNMENTS = value
    else:
      raise ValueError("Invalid configuration parameter: %s" % key)

# NEED TO VERIFY ALL PARAMEERS SET
