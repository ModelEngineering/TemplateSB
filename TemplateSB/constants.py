'''Constants used in TemplateSB.'''

COMMAND_START = "{{"
COMMAND_END = "}}"
COMMENT_STG = "#"
CONTINUED_STG = "\\"  # Indicates a continuation follows
EXPRESSION_START = "{"
EXPRESSION_END = "}"
LINE_TRAN = 1  # Transparent - nothing to process (comment line, no template variable)
LINE_COMMAND = 2  # Command line
LINE_SUBS = 3  # Line to be processed for substitutions
LINE_NONE = -1 # No more lines
SPLIT_STG = "\n"
