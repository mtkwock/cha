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

  def testParseLine_BasicClass(self):
    case = '种类人:'
    output = self.ParseLine(case)
    self.assertEqual('class ren2(ChaObject):', output)

  def testParseLine_SetsNewVariable(self):
    # ren2, a new class, should be created and stored
    case = '种类人:'
    self.assertNotIn('人', self.parser.char_to_var)
    self.ParseLine(case)
    self.assertIn('人', self.parser.char_to_var)
    self.assertEqual('ren2', self.parser.char_to_var['人'])

  def testParseLine_HandlesBasicSymbols(self):
    case = '一加一'
    output = self.ParseLine(case)
    self.assertEqual('1 + 1', output)