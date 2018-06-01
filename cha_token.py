class Token(object):
  def __init__(self, value):
    self._value = value

  def GetValue(self):
    return self._value

class StringToken(Token):
  """A defined string (not multiline).
  Includes the beginning and ending quotation.
  """
  pass

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

class NumberToken(Token):
  """A number token, can be of various forms:
  e.g. 0b10101010, 0x01afb, 123 -123 0.0052 122.2
  """
  pass

class SymbolToken(Token):
  """A single symbol:
  e.g. +, -, &, &=, "
  """
  pass


class VariableToken(Token):
  """Variable names for classes, functions, and so on."""
  pass

class ReservedWordToken(Token):
  """Python words such as class, def, True, and False."""
  pass
