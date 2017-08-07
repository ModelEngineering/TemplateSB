'''Class for extracting a line from a template.'''

from command import COMMAND_START, COMMAND_END
from constants import SPLIT_STG, COMMENT_STG, CONTINUED_STG,  \
    LINE_TRAN, LINE_COMMAND, LINE_SUBS, LINE_NONE,  \
    EXPRESSION_START, EXPRESSION_END


class LineExtractor(object):
  """
  Transforms the source lines into lines processed by TemplateProcessor.
    -Handles continuation lines.
    -Classifies the line obtained.
  """

  def __init__(self, input_lines):
    """
    :param str template_string: string containing template variables
        and template escape statements to execute
    """
    self._lines = input_lines.split(SPLIT_STG)
    self._source_line_number = 0
    self._current_line = None  # Complete line extracted from input
    self._current_line_type = None

  def _classifyLine(self):
    """
    Classifies a line as:
      LINE_TRAN: Transparent - nothing to process (comment line, no template variable)
      LINE_SUBS: Substitution line
      LINE_COMMAND: Template processor command
    State used:
      reads: _current_line
    """
    if self._current_line is None:
      result = LINE_NONE
    else:
      text = self._current_line.strip()
      if len(text) == 0:
        result = LINE_NONE
      elif text[0] == COMMENT_STG or len(text) == 0:
        result = LINE_TRAN
      elif len(text) < 2:
        result = LINE_TRAN
      elif text[0:2] == COMMAND_START:
        result = LINE_COMMAND
      elif text.count(EXPRESSION_START) == 0 and  \
          text.count(EXPRESSION_END) == 0:
        result = LINE_TRAN
      else:
        result = LINE_SUBS
    self._current_line_type = result

  def _getNextLine(self, strip=True):
    """
    Gets the next line, handling continued lines.
    State used:
      references: _source_line_number, _lines
      updates: _current_line, _source_line_number
    :parm bool strip: flag to indicate if white space should be stripped
    """
    self._current_line = None
    while self._source_line_number < len(self._lines):
      if self._current_line is None:
        self._current_line = ''
      if strip:
        text = self._lines[self._source_line_number].strip()
      else:
        text = self._lines[self._source_line_number]
      self._source_line_number += 1
      if len(text) == 0:
        continue
      if text[-len(CONTINUED_STG)] == CONTINUED_STG:
        self._current_line = self._current_line  \
            + text[0:-len(CONTINUED_STG)]
      else:
        self._current_line = self._current_line + text
        break

  def do(self, strip=True):
    """
    Process the next line.
    :return str, int: Current line, line classification
    """
    self._getNextLine(strip=strip)
    if self._current_line is None:
      line_type = LINE_NONE
    else:
      self._classifyLine()
    return self._current_line, self._current_line_type

  def getCurrentLine(self):
    return self._current_line

  def getCurrentSourceLineNumber(self):
    return self._source_line_number

  def getCurrentLineType(self):
    return self._current_line_type
