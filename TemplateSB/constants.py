'''Constants used in TemplateSB.'''

import os
import yaml


# The following constants are specified in the config file
COMMAND_START = None
COMMAND_END = None
COMMENT_STG = None
CONTINUED_STG = None
EXPRESSION_START = None
EXPRESSION_END = None
# Number of definitions before a warning is generated
WARNING_ASSIGNMENTS = 10000

# The following constants are internal
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE_PATH = os.path.join(PARENT_DIR, "config.yaml")
LINE_COMMAND = 2  # Command line
LINE_NONE = -1  # Command line
LINE_SUBS = 3  # Line to be processed for substitutions
LINE_TRAN = 1  # Transparent - nothing to process (comment line, no template variable)
LINE_NONE = -1 # No more lines
# Version of code
VERSION = "1.2"
# YAML keywords and their internal counterparts
PAIRS = {"command_start": "COMMAND_START",
         "command_end": "COMMAND_END",
         "comment_character": "COMMENT_STG",
         "continuation_string": "CONTINUED_STG",
         "expression_start": "EXPRESSION_START",
         "expression_end": "EXPRESSION_END",
         "warn_assignments": "WARNING_ASSIGNMENTS",
        }
SPLIT_STG = '\n'


def setConstantsFromConfig(path=CONFIG_FILE_PATH):
  fd = open(path, "r")
  lines = ''.join(fd.readlines())
  fd.close()
  namespace = globals()
  config_dict = yaml.load(lines)
  for key, value in config_dict.items():
    if key in PAIRS.keys():
      namespace[PAIRS[key]] = value
    else:
      raise ValueError("Invalid configuration parameter: %s" % key)
  # Check that all values have been assigned
  for name in PAIRS.values():
    if not name in namespace:
    # FIND THE VALUE
      raise ValueError("No configuration parameter: %s" % key)

def getGlobals():
  return globals()

setConstantsFromConfig()
