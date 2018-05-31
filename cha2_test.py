# Initial test setup for cha2.py

import unittest

from cha2 import ChaParser

class TestParseLine(unittest.TestCase):
  """Tests the ParseLine function in ChaParser."""
  def setUp(self):
    """Create a new parser to use for each test."""
    self.parser = ChaParser()
    self.ParseLine = self.parser.ParseLine

  def tearDown(self):
    self.parser.destroy()
    self.ParseLine = None

  def case(self, source_line, expected_output):
    """Tests a basic input and output case."""
    output = self.ParseLine(source_line)
    self.assertEqual(expected_output, output)

  def testBasicClass(self):
    self.case('种类人:', 'class ren2(ChaObject):')

  def testHandlesBasicSymbols(self):
    self.case('一加一', '1 + 1')

  def testDistinguishesNumberFromVariable(self):
    """Numbers can be used as variable names if they aren't at the beginning."""
    self.case('第一是一', 'dìyī = 1')

  def testSetsNewVariable(self):
    # ren2, a new class, should be created and stored
    case = '种类人:'
    self.assertNotIn('人', self.parser.char_to_var)
    self.ParseLine(case)
    self.assertIn('人', self.parser.char_to_var)
    self.assertEqual('ren2', self.parser.char_to_var['人'])
