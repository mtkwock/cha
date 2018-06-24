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
    return '%s(\'%s\')' % (self.__class__, self.GetValue())

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
    # print('Translating: %s' + self.GetValue())
    return self.GetValue().replace('“““', '"""').replace('”””', '"""').replace('\\“', '"').replace('\\”', '"')

class NumberFormat(Enum):
  ARABIC = 1
  SHORTHAND = 2
  FULLNAME = 3
  NARY = 4
  SCIENTIFIC = 5

SCIENTIFIC_CHAR_TO_NUM = {
  '负': '-',
  '零': '0',
  '一': '1',
  '二': '2',
  '两': '2',
  '三': '3',
  '四': '4',
  '五': '5',
  '六': '6',
  '七': '7',
  '八': '8',
  '九': '9',
  'E': 'e',
  'i': 'j',
  '点': '.',
}

class NumberToken(Token):
  """A number token, can be of various forms:
  e.g. 0b10101010, 0x01afb, 123 -123 0.0052 122.2
  """
  def __init__(self, value, format=NumberFormat.ARABIC):
    super().__init__(value)
    self.format = format

  def GetFormat(self):
    return self.format

  def Translate(self):
    #TO_DO
    value = self.GetValue()
    if self.format == NumberFormat.ARABIC:
        return ''.join(SCIENTIFIC_CHAR_TO_NUM[c] for c in value)
    elif self.format == NumberFormat.SHORTHAND:
        pass
    elif self.format == NumberFormat.FULLNAME:
        ds = ['0','0','0','0']
        a = '1'
        added_wan = True
        for c in value:
            if c == '负':
                ds.insert(0, SCIENTIFIC_CHAR_TO_NUM[c])
            elif c not in '十百千万亿':
                a = SCIENTIFIC_CHAR_TO_NUM[c]
            elif c == '十':
                ds[-2] = a
                a = '0'
            elif c == '百':
                ds[-3] = a
                a = '0'
            elif c == '千':
                ds[-4] = a
                a = '0'
            elif c == '万':
                ds[-1] = a
                for l in range(4): ds.append('0')
                added_wan = True
                a = '0'
            elif c == '亿':
                ds[-1] = a
                for l in range(4): ds.append('0')
                added_wan = False
                a = '0'
            #print(ds)
        if value[-1] not in '十百千万亿':
            ds[-1] = a
            #print(ds)
        if not added_wan:
            for l in range(4): ds.insert(4, '0')
            added_wan = True
            #print(ds)
        while ds[0] == '0':
          ds = ds[1:]
        return ''.join(ds)


    elif self.format == NumberFormat.NARY:
      pass
    raise Exception('Format not supported: %s' % self.format)

  def __eq__(self, other):
    return super().__eq__(other) and self.GetFormat() == other.GetFormat()

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
  """End of Line Token. Holds no values."""
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
