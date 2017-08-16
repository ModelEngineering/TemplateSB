'''Constants used in TemplateSB.'''

COMMAND_START = "{{"
COMMAND_END = "}}"
COMMENT_STG = "#"
CONTINUED_STG = "\\"  # Indicates a continuation follows
EXPRESSION_START = "{"
EXPRESSION_END = "}"
LINE_COMMAND = 2  # Command line
LINE_NONE = -1  # Command line
LINE_SUBS = 3  # Line to be processed for substitutions
LINE_TRAN = 1  # Transparent - nothing to process (comment line, no template variable)
LINE_NONE = -1 # No more lines
SPLIT_STG = "\n"
# Number of definitions before a warning is generated
WARNING_ASSIGNMENTS = 10000
# Version of code
VERSION = "1.2"
