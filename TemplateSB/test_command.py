"""
Tests for Command
"""
from command import Command, COMMAND_START, COMMAND_END
import unittest

IGNORE_TEST = False
DUMMY_VERSION = '1.4'
PYTHON_START = "%s ExecutePython Start %s" % (COMMAND_START, COMMAND_END)
PYTHON_END = "%s ExecutePython End %s" % (COMMAND_START, COMMAND_END)
SET_VERSION = "%s SetVersion %s %s"   \
    % (COMMAND_START, DUMMY_VERSION, COMMAND_END)


#############################
# Tests
#############################
# pylint: disable=W0212,C0111,R0904
class TestCommand(unittest.TestCase):

  def setUp(self):
    self.command = Command(PYTHON_START)

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
    self.assertEqual(arguments, self.command._arguments)

  def testConstructor(self):
    if IGNORE_TEST:
      return
    self.command = Command(PYTHON_START)
    self._testConstructor(PYTHON_START, Command.EXECUTE_PYTHON, None)
    self.assertTrue(self.command.isStart())
    self.assertFalse(self.command.isEnd())
    self.command = Command(PYTHON_END)
    self._testConstructor(PYTHON_END, Command.EXECUTE_PYTHON, None)
    self.command = Command(SET_VERSION)
    self._testConstructor(SET_VERSION, Command.SET_VERSION,
        [DUMMY_VERSION])

  def testIsExecuePython(self):
    if IGNORE_TEST:
      return
    self.command = Command(PYTHON_START)
    self.assertTrue(self.command.isExecutePython())

  def testIsSetVersion(self):
    if IGNORE_TEST:
      return
    self.command = Command(SET_VERSION)
    self.assertTrue(self.command.isSetVersion())

  def testIsStart(self):
    if IGNORE_TEST:
      return
    self.command = Command(PYTHON_START)
    self.assertTrue(self.command.isStart())

  def testIsEnd(self):
    if IGNORE_TEST:
      return
    self.command = Command(PYTHON_END)
    self.assertTrue(self.command.isEnd())

  def testStr(self):
    if IGNORE_TEST:
      return
    self.command = Command(PYTHON_START)
    self.assertEqual(str(self.command), PYTHON_START)

  def testInvalidCommandLine(self):
    if IGNORE_TEST:
      return
    with self.assertRaises(ValueError):
      command = Command("{{ This is Junk }}")
    with self.assertRaises(ValueError):
      command = Command(" This is Junk ")
    with self.assertRaises(ValueError):
      command = Command("{{ This is Junk }}")

  def testInvalidExecutePython(self):
    if IGNORE_TEST:
      return
    with self.assertRaises(ValueError):
      command = Command("{{ ExecutePython }}")
    with self.assertRaises(ValueError):
      command = Command("{{ ExecutePython Dummy }}")

  def testInvalidSetVersion(self):
    if IGNORE_TEST:
      return
    with self.assertRaises(ValueError):
      command = Command("{{ SetVersion }}")


if __name__ == '__main__':
  unittest.main()
