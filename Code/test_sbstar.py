import unittest
import numpy as np
from sbstar import Sbstar, PROCESSOR_NAME, Substituter


IGNORE_TEST = False
DEFINITIONS = {'a': ['A', 'a'], 'm': ['1', '2', '3']}
DEFINITIONS_LINE =  "#! %s Version 1.0 %s" %  \
    (PROCESSOR_NAME, str(DEFINITIONS))
template_stg1 = '''
%s
# No substitution
J1: S1 -> S2; k1*S1 
''' % DEFINITIONS_LINE
template_stg2 = '''
%s
# Substitution
J{a}1: S{a}1 -> S{a}2; k1*S{a}1
''' % DEFINITIONS_LINE
template_stg3 = '''
%s
# Missing template variable definition
J{c}1: S{c}1 -> S{c}2; k1*S{c}1
''' % DEFINITIONS_LINE



#############################
# Tests
#############################
# pylint: disable=W0212,C0111,R0904
class TestSubtituter(unittest.TestCase):

  def setUp(self):
    pass

  def testMakeSubtitutionList(self):
    substitution_list = Substituter.makeSubstitutionList(DEFINITIONS)
    expected = np.prod([len(d.keys()) for d in DEFININTIONS])
    self.assertEqual(len(substitution_list), expected)
    import pdb; pdb.set_trace()


#############################
# Tests
#############################
# pylint: disable=W0212,C0111,R0904
class TestSbstar(unittest.TestCase):

  def setUp(self):
    pass


if __name__ == '__main__':
  unittest.main()
