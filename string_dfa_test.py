"""Tests string_dfa.py."""

import unittest
from string_dfa import StringDfa, MultilineStringDfa, DfaException
from cha_token import Token, MultilineStringToken

def tokenize(string):
  """Creates an array from an iterable."""
  return [c for c in string]

class StringDfaTest(unittest.TestCase):
  """Tests the functionality of StringDfa"""
  def setUp(self):
    self.dfa = StringDfa()

  def tearDown(self): pass

  def RunTestCase(self, source, expected, tokenized=False):
    """Compares the output of source with the expected input."""
    source = source if tokenized else tokenize(source)
    output = self.dfa.ReplaceTokens(source)
    self.assertEqual(len(expected), len(output), 'Expected:\n%s\nGot:\n%s' % (expected, output))

    for i in range(len(expected)):
      expected_value = expected[i]
      output_value = output[i]
      if isinstance(output_value, Token):
        output_value = output_value.GetValue()

      self.assertEqual(expected_value, output_value)

  def testEmpty(self):
    self.RunTestCase('', [])

  def testNoString(self):
    self.RunTestCase('abc', tokenize('abc'))

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

class MultilineDfaTest(unittest.TestCase):
  def setUp(self):
    self.dfa = MultilineStringDfa()

  def RunTestCase(self, source, expected, inside=False, tokenized=False):
    """Compares the output of source with the expected input."""
    source = source if tokenized else tokenize(source)
    output = self.dfa.ReplaceTokens(source, inside)
    self.assertEqual(len(expected), len(output), 'Expected:\n%s\nGot:\n%s' % (expected, output))

    for i in range(len(expected)):
      expected_value = expected[i]
      output_value = output[i]
      if isinstance(output_value, Token):
        output_value = output_value.GetValue()

      self.assertEqual(expected_value, output_value)

  def testEmptyString(self):
    self.RunTestCase('', [])

  def testNoQuotes(self):
    self.RunTestCase('"', tokenize('"'))
    self.RunTestCase('""', tokenize('""'))
    # Theoretically, this is already invalid syntax.
    # self.RunTestCase('\\"""', tokenize('\\"""'))
    self.RunTestCase('"\\""', tokenize('"\\""'))

  def testQuoteStart_Basic(self):
    self.RunTestCase('"""', ['"""'])
    self.assertTrue(self.dfa.inside)

  def testQuoteStart_Indented(self):
    self.RunTestCase('  """', tokenize('  ') + ['"""'])

  def testQuoteStart_WithExtra(self):
    self.RunTestCase('"""abcdefg', ['"""abcdefg'])

  def testInsideQuote_Empty(self):
    self.RunTestCase('', [''], True)

  def testInsideQuote_Nonempty(self):
    self.RunTestCase('abc', ['abc'], True)
    self.assertTrue(self.dfa.inside)

  def testInsideQuote_DoesNotExist(self):
    self.RunTestCase('"', ['"'], True)
    self.RunTestCase('""', ['""'], True)
    self.RunTestCase('\\"""', ['\\"""'], True)
    self.RunTestCase('""\\"', ['""\\"'], True)

  def testInsideQuote_EndsQuote(self):
    self.RunTestCase('"""', ['"""'], True)
    self.assertFalse(self.dfa.inside)

  def testInsideQuote_EndsQuoteWithValues(self):
    self.RunTestCase('abc""" afterwards', ['abc"""'] + tokenize(' afterwards'), True)

  def testHandlesFullMultiline(self):
    self.RunTestCase(
      'a = """This is a big quote."""',
      tokenize('a = ') + ['"""This is a big quote."""'])

  def testHandlesMultipleQuotes(self):
    self.RunTestCase(
      'a = """b""" + """d"""',
      tokenize('a = ') + ['"""b"""'] + tokenize(' + ') + ['"""d"""'])
    self.assertFalse(self.dfa.inside)

  def testOddQuotes_EndsInside(self):
    self.RunTestCase('a = """b""" + """d',
      tokenize('a = ') + ['"""b"""'] + tokenize(' + ') + ['"""d'])
    self.assertTrue(self.dfa.inside)

  def testTypicalDocumentation(self):
    lines = '''def MyFunction(a):
  """This is my function. Returns double a

  Args:
  a: number The number to double
  Returns:
  number Double a
  """
  return 2 * a'''.split('\n')
    expecteds = [
      tokenize('def MyFunction(a):'),
      tokenize('  ') + ['"""This is my function. Returns double a'],
      [''],
      ['  Args:'],
      ['  a: number The number to double'],
      ['  Returns:'],
      ['  number Double a'],
      ['  """'],
      tokenize('  return 2 * a')
    ]
    for i in range(len(expecteds)):
      self.RunTestCase(lines[i], expecteds[i], self.dfa.inside)

  def testStringAddition(self):
    lines = '''a = """This is
across two lines""" + "!"'''.split('\n')
    expecteds = [
      tokenize('a = ') + ['"""This is'],
      ['across two lines"""'] + tokenize(' + "!"')
    ]
    for i in range(len(expecteds)):
      self.RunTestCase(lines[i], expecteds[i], self.dfa.inside)
