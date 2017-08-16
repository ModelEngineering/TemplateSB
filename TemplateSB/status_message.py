'''Generates Warning and Error Messages.'''

import warnings


class StatusMessage(object):

  def __init__(self, extractor):
    """
    :param LineExtractor extractor:
    """
    self._extractor = extractor

  def error(self, msg):
    """
    :param str msg:
    :raises ValueError:
    """
    error = "on line %d.\n'%s'\nError message: %s"  \
        % (self._extractor.getCurrentSourceLineNumber(), 
           self._extractor.getCurrentLine(), msg)
    raise ValueError(error)
  
  def warning(self, msg):
    """
    :param str msg:
    """
    warning_msg = "on line %d.\n'%s'\nError message: %s"  \
        % (self._extractor.getCurrentSourceLineNumber(), 
           self._extractor.getCurrentLine(), msg)
    warnings.warn(warning_msg)
