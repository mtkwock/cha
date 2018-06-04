from enum import Enum

class Token(object):
  def __init__(self, value):
    self._value = value

  def GetValue(self):
    return self._value

  def Translate(self):
    return self._value

class StringToken(Token):
  """A defined string (not multiline).
  Includes the beginning and ending quotation.
  """
  def Translate(self):
    unescape = self._value.replace('\\“', '"').replace('\\”', '"')
    return '"%s"' % self._value[1:-1]

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
  pass

class NumberFormat(Enum):
  ARABIC = 1
  SHORTHAND = 2
  FULLNAME = 3
  NARY = 4


class NumberToken(Token):
  """A number token, can be of various forms:
  e.g. 0b10101010, 0x01afb, 123 -123 0.0052 122.2
  """
  def __init__(self, value, format=NumberFormat.ARABIC):
      super().__init__(value)
      self.format = format

  def Translate(self):
      if self.format == NumberFormat.ARABIC:
          pass
      elif self.format == NumberFormat.SHORTHAND:
          pass
      elif self.format == NumberFormat.FULLNAME:
          pass
      elif self.format == NumberFormat.NARY:
          pass
      raise Exception('Format not supported: %s' % self.format)

class SymbolToken(Token):
  """A single symbol:
  e.g. +, -, &, &=, "
  """
  pass

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
  pass

class ReservedWordToken(Token):
  """Python words such as class, def, True, and False."""
  pass
