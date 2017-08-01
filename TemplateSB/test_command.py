"""
Tests for Command
"""
from command import Command
from constants import COMMAND_START, COMMAND_END
import unittest

IGNORE_TEST = False
DUMMY_VERSION = '1.4'
DEFINE_VARIABLES_START = "%s %s Start %s" % (COMMAND_START, Command.DEFINE_VARIABLES, COMMAND_END)
DEFINE_VARIABLES_END = "%s %s End %s" % (COMMAND_START, Command.DEFINE_VARIABLES, COMMAND_END)
DEFINE_CONSTRAINTS_START = "%s %s Start %s" % (COMMAND_START, Command.DEFINE_CONSTRAINTS, COMMAND_END)
ENDDEFINE_CONSTRAINTS_ = "%s %s End %s" % (COMMAND_START, Command.DEFINE_CONSTRAINTS, COMMAND_END)
SET_VERSION = "%s %s %s %s"   \
    % (COMMAND_START, Command.SET_VERSION, DUMMY_VERSION, COMMAND_END)


#############################
# Tests
#############################
# pylint: disable=W0212,C0111,R0904
class TestCommand(unittest.TestCase):

  def setUp(self):
    self.command = Command(DEFINE_VARIABLES_START)

  def _testConstructor(self, command_line, command_verb, arguments):
    """
    :param str command_line: command as it appears in input
    :param int command_verb: Command class variable
    :param list arguments: None if list is empty
    """
    if IGNORE_TEST:
      return
    self.assertEqual(command_line, self.command._command_line)
    self.assertEqual(command_verb,
        self.command._command_verb)
    if not arguments  == self.command._arguments:
      import pdb; pdb.set_trace()
      pass
    self.assertEqual(arguments, self.command._arguments)

  def testConstructor(self):
    if IGNORE_TEST:
      return
    self.command = Command(DEFINE_VARIABLES_START)
    self._testConstructor(DEFINE_VARIABLES_START, Command.DEFINE_VARIABLES, [])
    self.assertTrue(self.command.isStart())
    self.assertFalse(self.command.isEnd())
    self.command = Command(DEFINE_VARIABLES_END)
    self._testConstructor(DEFINE_VARIABLES_END, Command.DEFINE_VARIABLES, [])
    self.command = Command(SET_VERSION)
    self._testConstructor(SET_VERSION, Command.SET_VERSION,
        [DUMMY_VERSION])

  def testIsDefineConstraints(self):
    if IGNORE_TEST:
      return
    self.command = Command(DEFINE_CONSTRAINTS_START)
    self.assertTrue(self.command.isDefineConstraints())

  def testIsDefineVariables(self):
    if IGNORE_TEST:
      return
    self.command = Command(DEFINE_VARIABLES_START)
    self.assertTrue(self.command.isDefineVariables())

  def testIsSetVersion(self):
    if IGNORE_TEST:
      return
    self.command = Command(SET_VERSION)
    self.assertTrue(self.command.isSetVersion())

  def testIsStart(self):
    if IGNORE_TEST:
      return
    self.command = Command(DEFINE_VARIABLES_START)
    self.assertTrue(self.command.isStart())

  def testIsEnd(self):
    if IGNORE_TEST:
      return
    self.command = Command(DEFINE_VARIABLES_END)
    self.assertTrue(self.command.isEnd())

  def testStr(self):
    if IGNORE_TEST:
      return
    self.command = Command(DEFINE_VARIABLES_START)
    self.assertEqual(str(self.command), DEFINE_VARIABLES_START)

  def testInvalidCommandLine(self):
    if IGNORE_TEST:
      return
    with self.assertRaises(ValueError):
      command = Command("{{ This is Junk }}")
    with self.assertRaises(ValueError):
      command = Command(" This is Junk ")
    with self.assertRaises(ValueError):
      command = Command("{{ This is Junk }}")

  def testInvalidDefineVariables(self):
    if IGNORE_TEST:
      return
    with self.assertRaises(ValueError):
      command = Command("{{ DefineVariables }}")
    with self.assertRaises(ValueError):
      command = Command("{{ DefineVariables Dummy }}")

  def testInvalidSetVersion(self):
    if IGNORE_TEST:
      return
    with self.assertRaises(ValueError):
      command = Command("{{ SetVersion }}")


if __name__ == '__main__':
  unittest.main()
