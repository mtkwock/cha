"""Tests string_dfa.py."""

import unittest
from string_dfa import StringDfa, DfaException
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
        output = self.dfa.RunString(source)
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
        self.assertRaises(DfaException, self.dfa.RunString, 'a = "" "')

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
        self.assertRaises(DfaException, self.dfa.RunString, case)
