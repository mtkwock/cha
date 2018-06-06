"""Tests number_variable_dfa.py."""

import unittest
from number_variable_dfa import NumberVariableDfa, DfaException
from cha_token import Token, NumberFormat, NumberToken, VariableToken, ReservedWordToken, WhitespaceToken, SymbolToken

def tokenize(string):
  """Creates an array from an iterable."""
  return [c for c in string]

class NumberVariableDfaTest(unittest.TestCase):
  """Tests the functionality of NumberVariableDfa"""
  def setUp(self):
    self.dfa = NumberVariableDfa()

  def tearDown(self): pass

  def RunTestCase(self, source, expected, tokenized=False):
    """Compares the output of source with the expected input."""
    source = source if tokenized else tokenize(source)
    output = self.dfa.ReplaceTokens(source)
    self.assertEqual(len(expected), len(output), 'Expected:\n%s\nGot:\n%s' % (expected, output))

    for i in range(len(expected)):
      expected_i = expected[i]
      output_i = output[i]
      if isinstance(output_i, Token):
        output_value = output_i.GetValue()
        expected_value = expected_i.GetValue()
      else:
          expected_value = expected_i
          output_value = output_i        
      self.assertEqual(expected_value, output_value)
      if isinstance(output_value, NumberToken):
        self.assertEqual(expected_i.format, output_i.format)


  res = my.ReplaceTokens([ReservedWordToken('每'), '茶','茶', ReservedWordToken('当'),'水', ReservedWordToken('里')])
  print(res)
  r2 = my.ReplaceTokens([WhitespaceToken(' '), '我', SymbolToken('是'),'零','一','二','三','点','三',WhitespaceToken(' ')])
  print(r2)
  r3 = my.ReplaceTokens([WhitespaceToken(' '), '我', SymbolToken('是'),'三','七','三','E','三','九',WhitespaceToken(' ')])
  print(r3)
  r4 = my.ReplaceTokens([WhitespaceToken(' '), '我', SymbolToken('是'),'三','十','三','万','五','千',WhitespaceToken(' ')])
  print(r4)
  r5 = my.ReplaceTokens([WhitespaceToken(' '), '我', SymbolToken('是'),'二','进','一','零','一','零',WhitespaceToken(' ')])
  print(r5)
  # r6 should fail
  r6 = my.ReplaceTokens([WhitespaceToken(' '), '我', SymbolToken('是'),'三','三','进','Z','A','B',WhitespaceToken(' ')])
  print(r6)

  def testEmpty(self):
    self.RunTestCase('', [])

  def testNoString(self):
    self.RunTestCase([WhitespaceToken(' '), '我', SymbolToken('是'),'零','一','二','三','点','三',WhitespaceToken(' ')],
    [WhitespaceToken(' '), VariableToken('我'), SymbolToken('是'), NumberToken('零一二三点三'), WhitespaceToken(' ')])
  def testEmptyString(self):
    self.RunTestCase('""', ['""'])

  def testSetEmptyString(self):
    self.RunTestCase('a = ""', tokenize('a = ') + ['""'])

  def testWholeString(self):
    self.RunTestCase('"Whole String"', ['"Whole String"'])

  def testInnerString(self):
    self.RunTestCase('abc = "def"', tokenize('abc = ') + ['"def"'])

  def testMultipleStrings(self):
    self.RunTestCase('a = "a" + "b"',
        tokenize('a = ') + ['"a"'] + tokenize(' + ') + ['"b"'])

  def testEscapedString(self):
    self.RunTestCase('"abc \\" def"', ['"abc \\" def"'])

  def testAlmostEscapedString(self):
    self.RunTestCase('"abc\\\\"', ['"abc\\\\"'])

  def testOddQuotes(self):
    self.assertRaises(DfaException, self.dfa.ReplaceTokens, 'a = "" "')

  def testReallyLargeString(self):
    case = 'a = "abc" + "def" + ("ghi\\"  12478sajkf你好")'
    output = (tokenize('a = ') +
        ['"abc"'] + tokenize(' + ') +
        ['"def"'] + tokenize(' + (') +
        ['"ghi\\"  12478sajkf你好"', ')'])
    self.RunTestCase(case, output)

  def testHandlesValidMultilineToken(self):
    """Happens when adding multiline string to a regular string."""
    case = [MultilineStringToken('end of line"""')] + tokenize(' + "abc"')
    output = ['end of line"""'] + tokenize(' + ') + ['"abc"']
    self.RunTestCase(case, output)

  def testMultilineTokenInvalid_RaisesException(self):
    """In the case that a multiline is already defined.
    case:
      abc = ' not ended '''multiline stuff here
    """
    case = tokenize('abc = " not ended') + [MultilineStringToken('"""multiline stuff here')]
    self.assertRaises(DfaException, self.dfa.ReplaceTokens, case)
