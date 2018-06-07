"""Tests string_dfa.py."""

import unittest
from string_dfa import StringDfa, MultilineStringDfa, DfaException
from cha_token import Token, MultilineStringToken, StringToken

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
    self.assertEqual(expected, output)

  def testEmpty(self):
    self.RunTestCase('', [])

  def testNoString(self):
    self.RunTestCase('abc', tokenize('abc'))

  def testEmptyString(self):
    self.RunTestCase('""', [StringToken('""')])

  def testSetEmptyString(self):
    self.RunTestCase('a = ""', [*tokenize('a = '), StringToken('""')])

  def testWholeString(self):
    self.RunTestCase('"Whole String"', [StringToken('"Whole String"')])

  def testInnerString(self):
    self.RunTestCase('abc = "def"', [*tokenize('abc = '), StringToken('"def"')])

  def testMultipleStrings(self):
    self.RunTestCase('a = "a" + "b"',
        [*tokenize('a = '), StringToken('"a"'), *tokenize(' + '), StringToken('"b"')])

  def testEscapedString(self):
    self.RunTestCase('"abc \\" def"', [StringToken('"abc \\" def"')])

  def testAlmostEscapedString(self):
    self.RunTestCase('"abc\\\\"', [StringToken('"abc\\\\"')])

  def testOddQuotes(self):
    self.assertRaises(DfaException, self.dfa.ReplaceTokens, 'a = "" "')

  def testReallyLargeString(self):
    case = 'a = "abc" + "def" + ("ghi\\"  12478sajkf你好")'
    output = [*tokenize('a = '),
        StringToken('"abc"'), *tokenize(' + '),
        StringToken('"def"'), *tokenize(' + ('),
        StringToken('"ghi\\"  12478sajkf你好"'), ')']
    self.RunTestCase(case, output)

  def testHandlesValidMultilineToken(self):
    """Happens when adding multiline string to a regular string."""
    case = [MultilineStringToken('end of line"""'), *tokenize(' + "abc"')]
    output = [MultilineStringToken('end of line"""'), *tokenize(' + '), StringToken('"abc"')]
    self.RunTestCase(case, output)

  def testMultilineTokenInvalid_RaisesException(self):
    """In the case that a multiline is already defined.
    case:
      abc = ' not ended '''multiline stuff here
    """
    case = [*tokenize('abc = " not ended'), MultilineStringToken('"""multiline stuff here')]
    self.assertRaises(DfaException, self.dfa.ReplaceTokens, case)

class MultilineDfaTest(unittest.TestCase):
  def setUp(self):
    self.dfa = MultilineStringDfa()

  def RunTestCase(self, source, expected, inside=False, tokenized=False):
    """Compares the output of source with the expected input."""
    source = source if tokenized else tokenize(source)
    output = self.dfa.ReplaceTokens(source, inside)
    self.assertEqual(expected, output)

  def testEmptyString(self):
    self.RunTestCase('', [])

  def testNoQuotes(self):
    self.RunTestCase('"', tokenize('"'))
    self.RunTestCase('""', tokenize('""'))
    # Theoretically, this is already invalid syntax.
    # self.RunTestCase('\\"""', tokenize('\\"""'))
    self.RunTestCase('"\\""', tokenize('"\\""'))

  def testQuoteStart_Basic(self):
    self.RunTestCase('"""', [MultilineStringToken('"""')])
    self.assertTrue(self.dfa.inside)

  def testQuoteStart_Indented(self):
    self.RunTestCase('  """', tokenize('  ') + [MultilineStringToken('"""')])

  def testQuoteStart_WithExtra(self):
    self.RunTestCase('"""abcdefg', [MultilineStringToken('"""abcdefg')])

  def testInsideQuote_Empty(self):
    self.RunTestCase('', [MultilineStringToken('')], True)

  def testInsideQuote_Nonempty(self):
    self.RunTestCase('abc', [MultilineStringToken('abc')], True)
    self.assertTrue(self.dfa.inside)

  def testInsideQuote_DoesNotExist(self):
    self.RunTestCase('"a', [MultilineStringToken('"a')], True)
    self.RunTestCase('""a', [MultilineStringToken('""a')], True)
    self.RunTestCase('\\"""a', [MultilineStringToken('\\"""a')], True)
    self.RunTestCase('""\\"a', [MultilineStringToken('""\\"a')], True)

  def testInsideQuote_EndsQuote(self):
    self.RunTestCase('"""', [MultilineStringToken('"""')], True)
    self.assertFalse(self.dfa.inside)

  def testInsideQuote_EndsQuoteWithValues(self):
    self.RunTestCase('abc""" afterwards', [MultilineStringToken('abc"""')] + tokenize(' afterwards'), True)

  def testHandlesFullMultiline(self):
    self.RunTestCase(
      'a = """This is a big quote."""',
      tokenize('a = ') + [MultilineStringToken('"""This is a big quote."""')])

  def testHandlesMultipleQuotes(self):
    self.RunTestCase(
      'a = """b""" + """d"""',
      tokenize('a = ') + [MultilineStringToken('"""b"""')] + tokenize(' + ') + [MultilineStringToken('"""d"""')])
    self.assertFalse(self.dfa.inside)

  def testOddQuotes_EndsInside(self):
    self.RunTestCase('a = """b""" + """d',
      tokenize('a = ') + [MultilineStringToken('"""b"""')] + tokenize(' + ') + [MultilineStringToken('"""d')])
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
      [*tokenize('  '), MultilineStringToken('"""This is my function. Returns double a')],
      [MultilineStringToken('')],
      [MultilineStringToken('  Args:')],
      [MultilineStringToken('  a: number The number to double')],
      [MultilineStringToken('  Returns:')],
      [MultilineStringToken('  number Double a')],
      [MultilineStringToken('  """')],
      tokenize('  return 2 * a')
    ]
    for i in range(len(expecteds)):
      self.RunTestCase(lines[i], expecteds[i], self.dfa.inside)

  def testStringAddition(self):
    lines = '''a = """This is
across two lines""" + "!"'''.split('\n')
    expecteds = [
      tokenize('a = ') + [MultilineStringToken('"""This is')],
      [MultilineStringToken('across two lines"""')] + tokenize(' + "!"')
    ]
    for i in range(len(expecteds)):
      self.RunTestCase(lines[i], expecteds[i], self.dfa.inside)
