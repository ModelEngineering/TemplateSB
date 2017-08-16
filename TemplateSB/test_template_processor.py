"""
Tests for TemplateProcessor
"""
from template_processor import TemplateProcessor
from constants import COMMAND_START, COMMAND_END, LINE_COMMAND,  \
    LINE_NONE

import copy
import unittest
import numpy as np
import os


IGNORE_TEST = False
DEFINITIONS = {'a': ['a', 'b', 'c'], 
               'm': [1, 2, 3],
               'c': ['c', '']}
COMMAND = \
'''%s DefineVariables Begin %s
DEFINITIONS = %s
api.addDefinitions(DEFINITIONS)
%s DefineVariables End %s '''  \
    %(COMMAND_START, COMMAND_END, str(DEFINITIONS),
    COMMAND_START, COMMAND_END)
SUBSTITUTION1 = "J1: S1 -> S2; k1*S1"
SUBSTITUTION2 = "J{a}1: S{a}1 -> S{a}2; k1*S{a}1"
SUBSTITUTION3 = "J{c}1: S{c}1 -> S{c}2; k1*S{c}1"
SUBSTITUTION4 = "J{m}: S{m} -> S{m+1}; k1*S{m}"
TEMPLATE_STG1 = '''
%s
%s
''' % (COMMAND, SUBSTITUTION1)
TEMPLATE_BAD = '''%s
%s''' % (COMMAND_START, SUBSTITUTION1)
TEMPLATE_STG2 = '''%s
%s''' % (COMMAND, SUBSTITUTION2)
TEMPLATE_STG3 = '''%s
%s''' % (COMMAND, SUBSTITUTION3)
TEMPLATE_NO_DEFINITION = SUBSTITUTION3
TEMPLATE_STG4 = '''%s
%s''' % (COMMAND, SUBSTITUTION4)
TEMPLATE_NO_DEFINITION = SUBSTITUTION4


def isSubDict(dict_super, dict_sub):
  """
  Tests if the second dictonary is a subset of the first.
  :param dict dict_super:
  :param dict dict_sub:
  :return bool:
  """
  for key in dict_sub.keys():
    if not key in dict_super:
      return False
    if not dict_sub[key] == dict_super[key]:
      return False
  return True


#############################
# Tests
#############################
# pylint: disable=W0212,C0111,R0904
class TestTemplateProcessor(unittest.TestCase):

  def setUp(self):
    self.processor = TemplateProcessor(TEMPLATE_STG2)

  def testConstructor(self):
    if IGNORE_TEST:
      return
    self.assertIsNotNone(self.processor._extractor)

  def _testExpand(self, template, variable):
    """
    :param str template: template to expand
    :param str variable: variable to check
    """
    self.processor = TemplateProcessor(template)
    lines = self.processor.do()
    try:
      for val in DEFINITIONS[variable]:
        str_val = "J%s" % str(val)
        if not str_val in lines:
          import pdb; pdb.set_trace()
        self.assertTrue(str_val in lines)
    except Exception as exp:
      import pdb; pdb.set_trace()
      pass
    

  def testDo(self):
    if IGNORE_TEST:
      return
    self._testExpand(TEMPLATE_STG2, 'a')
    self._testExpand(TEMPLATE_STG3, 'c')
    self._testExpand(TEMPLATE_STG4, 'm')

  def testDo2(self):
    template = '''
%s DefineVariables Begin %s
api.addDefinitions({'s':  ['a', 'b'], 
                    't':  ['x', 'y']
                  })
%s DefineVariables End %s
J{s}{t}: S1{s}{t} -> S2{s}{t}; k1*S1{s}{t}'''  %  \
        (COMMAND_START, COMMAND_END, COMMAND_START, COMMAND_END)
    self.processor = TemplateProcessor(template)
    lines = self.processor.do()
    actual_lines = 1 + lines.count('\n')
    expected_lines = 4 + template.count('\n')
    self.assertEqual(actual_lines, expected_lines)
    self.assertTrue("addDefinitions" in lines)
    substitutions = ["Jax", "Jbx", "Jay", "Jby"]
    result = all([s in lines for s in substitutions])
    self.assertTrue(result)
    
 

  def testExpandErrorInDefinition(self):
    if IGNORE_TEST:
      return
    with self.assertRaises(ValueError):
      processor = TemplateProcessor(TEMPLATE_BAD)
      result = processor.do()

  def testNoDefinintion(self):
    if IGNORE_TEST:
      return
    self.processor = TemplateProcessor(TEMPLATE_NO_DEFINITION)
    with self.assertRaises(ValueError):
      lines = self.processor.do()

  def testFile(self):
    if IGNORE_TEST:
      return
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_path = os.path.dirname(dir_path)
    src_path = os.path.join(parent_path, "Example")
    src_path = os.path.join(src_path, "sample.tmpl")
    TemplateProcessor.processFile(src_path, "/tmp/out.mdl")

  def _testProcessCommand(self, template, is_processed, is_command, processor=None):
    """
    Evaluates the processing of a template line
    :return TemplateProcessor:
    """
    if processor is None:
      processor = TemplateProcessor(template)
    line, line_type = processor._extractor.do()
    self.assertEqual(processor._processCommand(), is_processed)
    is_not_none = processor._command is not None
    self.assertEqual(is_command, line_type == LINE_COMMAND)
    return processor

  def testProcessCommand(self):
    if IGNORE_TEST:
      return
    self._testProcessCommand("line 1", False, False)
    self._testProcessCommand("%s DefineVariables Begin %s" 
        % (COMMAND_START, COMMAND_END), True, True)
    line = '''%s DefineVariables Begin %s
a = 32
%s DefineVariables End %s
aa{a} + bb{d}'''  \
        % (COMMAND_START, COMMAND_END, COMMAND_START, COMMAND_END)
    processor = self._testProcessCommand(line, True, True)
    self._testProcessCommand(line, True, False, processor=processor)
    self._testProcessCommand(line, True, True, processor=processor)
    self._testProcessCommand(line, False, False, processor=processor)
    

if __name__ == '__main__':
  unittest.main()
