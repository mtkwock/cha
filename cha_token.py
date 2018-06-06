from enum import Enum

from cha_translation import reserved_symbols, reserved_beginning_words
from pinyin import get as ToPinyin

class Token(object):
  def __init__(self, value):
    self._value = value

  def GetValue(self):
    return self._value

  def Translate(self):
    return self._value

  def __eq__(self, other):
    return self.__class__ == other.__class__ and self.GetValue() == other.GetValue()

  def __str__(self):
    return '%s(%s)' % (self.__class__, self.GetValue())

  def __repr__(self):
    return self.__str__()

class StringToken(Token):
  """A defined string (not multiline).
  Includes the beginning and ending quotation.
  """
  def Translate(self):
    unescape = self._value.replace('\\“', '"').replace('\\”', '"')
    return '"%s"' % unescape[1:-1]

class MultilineStringToken(Token):
  """A part of a multiline string.
  Can begin or end with triple quotes, but can be an entire line without.

  e.g.:

  '''abc
    OR
  abc
    OR
  abc'''
  """
  def Translate(self):
    return self._value.replace('“““', '"""').replace('”””', '"""').replace('\\“', '"').replace('\\”', '"')

class NumberFormat(Enum):
  ARABIC = 1
  SHORTHAND = 2
  FULLNAME = 3
  NARY = 4
  SCIENTIFIC = 5


class NumberToken(Token):
  """A number token, can be of various forms:
  e.g. 0b10101010, 0x01afb, 123 -123 0.0052 122.2
  """
  def __init__(self, value, format=NumberFormat.ARABIC):
    super().__init__(value)
    self.format = format

  def Translate(self):
      #TO_DO
      if self.format == NumberFormat.ARABIC:
          pass
      elif self.format == NumberFormat.SHORTHAND:
          pass
      elif self.format == NumberFormat.FULLNAME:
          pass
      elif self.format == NumberFormat.NARY:
          pass
      elif self.format == NumberFormat.SCIENTIFIC: # potentially remove if included in arabic
          pass
      raise Exception('Format not supported: %s' % self.format)

class SymbolToken(Token):
  """A single symbol:
  e.g. +, -, &, &=, "
  """
  def Translate(self):
      return reserved_symbols[self.GetValue()]

class WhitespaceToken(Token):
  """Whitespace formatting comprised of only tabs or spaces."""
  def Translate(self):
    val = self.GetValue()
    return val.replace(' ', '  ').replace('\t', '  ')

class EndToken(Token):
    """End of Line Token. Holds no value."""
    def __init__(self):
        super().__init__('')

class VariableToken(Token):
  """Variable names for classes, functions, and so on."""
  def Translate(self, c2v=None, v2c=None):
    c2v = c2v or {}
    v2c = v2c or {}
    if self.GetValue() in c2v:
      return c2v[self.GetValue()]
    pinyin = ToPinyin(self.GetValue())
    o_pinyin = pinyin
    offset = 0
    while o_pinyin in v2c:
      offset += 1
      o_pinyin = '%s%d' % (pinyin, offset)
    c2v[self.GetValue()] = o_pinyin
    v2c[o_pinyin] = self.GetValue()
    return o_pinyin

class ReservedWordToken(Token):
  """Python words such as class, def, True, and False."""
  def Translate(self):
    return reserved_beginning_words[self.GetValue()]

class ParseToken(Token):
  """Special tokens for parsing special parts."""
