"""Tests number_variable_dfa.py."""

import unittest
from number_variable_dfa import NumberVariableDfa, DfaException
from cha_token import Token, NumberFormat, NumberToken, VariableToken, ReservedWordToken, WhitespaceToken, SymbolToken, EndToken

def tokenize(string):
  """Creates an array from an iterable."""
  return [c for c in string]

def CreateTestCase(case):
  return [WhitespaceToken(' '), '我', SymbolToken('是'), *tokenize(case), EndToken()]

def CreateExpectedValue(token):
  return [WhitespaceToken(' '), VariableToken('我'), SymbolToken('是'), token, EndToken()]

class NumberVariableDfaTest(unittest.TestCase):
  """Tests the functionality of NumberVariableDfa"""
  def setUp(self):
    self.dfa = NumberVariableDfa()

  def tearDown(self): pass

  def RunTestCase(self, source, expected, tokenized=False):
    """Compares the output of source with the expected input."""
    source = source if tokenized else tokenize(source)
    output = self.dfa.ReplaceTokens(source)
    # self.assertEqual(len(expected), len(output), 'Expected:\n%s\nGot:\n%s' % (expected, output))
    self.assertListEqual(expected, output)

  def testCombinesStringsForVariables(self):
    self.RunTestCase(
        [ReservedWordToken('每'),             '茶','茶', ReservedWordToken('当'),               '水',  ReservedWordToken('里')],
        [ReservedWordToken('每'), VariableToken('茶茶'), ReservedWordToken('当'), VariableToken('水'), ReservedWordToken('里')])

  def testCreatesArabicNumberWithDecimals(self):
    self.RunTestCase(CreateTestCase('一二三点三'),
        CreateExpectedValue(NumberToken('一二三点三')))

  def testCreatesArabicNumbersWithExponents(self):
    self.RunTestCase(
        CreateTestCase('三七三E三九'),
        CreateExpectedValue(NumberToken('三七三E三九')))

  def testParsesFullname(self):
    self.RunTestCase(
        CreateTestCase('三十三万五千'),
        CreateExpectedValue(NumberToken('三十三万五千', NumberFormat.FULLNAME)))

  def testParsesBinary(self):
    self.RunTestCase(
        CreateTestCase('二进一零一零'),
        CreateExpectedValue(NumberToken('二进一零一零', NumberFormat.NARY))
    )

  def testRejectsUnsuitableBinary(self):
    self.assertRaises(DfaException, self.dfa.ReplaceTokens, CreateTestCase('三三进ZAB'))
