#!bin/bash/env python

from pinyin import get as pget
import sys
from pathlib import Path

class ChaParseException(Exception): pass
class ChaNotImplementedException(Exception):
  def __init__(self, name):
    super().__init__(name + ' not implemented')

CHAR_TO_VAR_BASE = {
  '艹艹初始艹艹': '__chūshǐ__',
  '自己': 'zìjǐ',
  '都': 'dōu',
  '任何': 'rènhé',
}

VAR_TO_CHAR_BASE = {
  CHAR_TO_VAR_BASE[key]: key for key in CHAR_TO_VAR_BASE
}

# These words are reserved Python words and symbols
reserved_symbols = {
  # Symbols based on https://docs.python.org/3/genindex-Symbols.html
  '的': '.',
  '是': ' = ',  # Assign
  '': ' # ', # Commenting
  '（': '(', '）': ')',
  '【': '[', '】': ']',
  '「': '{', '」': '}',
  '': ' % ', '': ' %= ',
  '': '\'',
  '': '"',

  # Numbers
  '': '0x',
  '零': '0',
  '一': '1',
  '二': '2',
  '三': '3',
  '四': '4',
  '五': '5',
  '六': '6',
  '七': '7',
  '八': '8',
  '九': '9',

  # Arithmetic operations
  '加':   ' + ',   '加是':   ' += ',
  '减':   ' - ',   '减是':   ' -= ',
  '乘':   ' * ',   '乘是':   ' *= ',
  '除':  ' / ',  '除是':  ' /= ',
  '整除': ' // ', '整除是': ' //= ',
  '幂': ' ** ', '幂是': ' **= ',  # Exponent

  # Binary operations
  '': ' ~',  # Negation operator
  '': ' & ',  '': ' &= ',
  '': ' | ',  '': ' |= ',
  '': ' ^ ',  '': ' ^= ',
  '': ' >> ', '': ' >>= ',
  '': ' << ', '': ' <<= ',
  
  # Comparators
  '': ' > ',
  '': ' >= ',
  '等于': ' == ',
  '': ' <= ',
  '': ' < ',
}

# 
unsupported_symbols = {
  reserved_symbols[key].strip(): key for key in reserved_symbols
}

# Reserved words based on
# https://www.programiz.com/python-programming/keywords-identifier#key
reserved_words = {
  # A line can only start with this is if it is declaring a class.
  # Variables, class names, and functions can start with this.
  '种类': 'class',
  '定义': 'def',
  '如果': 'if',
  '否则如果': 'elif',
  '否则': 'else',
  '': 'True',
  '': 'False',
  '': 'None',
  '': 'and',
  '': 'or',
  '': 'not',
  '': 'break',
  '继续': 'continue', # ji4xu4
}

def ToPinyin(string):
  return pget(string)
  # return pget(string, format='numerical')

class ChaParser:
  def __init__(self):
    self.char_to_var = dict(CHAR_TO_VAR_BASE)
    self.var_to_char = dict(VAR_TO_CHAR_BASE)

  def destroy(self):
    self.char_to_var = None
    self.var_to_char = None

  def ParseLine(self, line):
    """Parses a single line of .cha to python.

    As a side effect, modifies char_to_var and var_to_char with new
    variable names if applicable.

    Args:
      line: string a line of cha.
    Raises:
      ChaParseException
    Returns:
      str: a string of .py code
    """
    output_string = line
    for symbol in unsupported_symbols:
      if symbol not in line: continue

      raise ChaParseException('Invalid symbol: "%s", replace with "%s"' %
                              (symbol, unsupported_symbols[symbol]))

    # TODO: handle strings
    for symbol in reserved_symbols:
      if not symbol: continue
      output_string = output_string.replace(symbol, reserved_symbols[symbol])
    # TODO: handle reserved words
    # TODO: handle variables, new and old
    return output_string

  def Convert(self, source, dest, space_per_indent=2, use_tabs=False):
    """Open and convert a single .cha file to the equivalent .py file

    Args:
      source: string a Filename to convert to py.
      dest: string a filename to write to.
      space_per_indent: number How many spaces to convert each space to.
      use_tabs: boolean Whether to use tabs instead of spaces. Overrides space_per_indent

    Raises:
      Exception: An exception if something goes wrong with the conversion
    """
    raise ChaNotImplementedException('ChaParser.Convert')
    with open(filename) as f:
      for line in f.readlines():
        # Convert and export to './example.py'
        # First figure out strings
        # Then figure out special symbols such as +/-
        # Determine which variables exist already
        # Add new variable names to char_to_var
        # Convert variable names to pinyin
        # Append string to output file.
        pass



filename_to_convert = './example.cha'
outputfile = filename_to_convert[:-3] + '.py'

def help_command():
  print("""Converts a given .cha file into a (roughly) equivalent .py file

To use:
cha2.py FILE_TO_CONVERT EXPORT_FILENAME
""")

if __name__ == '__main__':
  args = sys.argv
  if len(args) < 2:
    help_command()
    exit(0)

  source_file = args[1]
  if not file.endswith('.cha'):
    raise Exception('Must end with .cha')

  dest_file = source_file[:-3] + 'py' if len(args) < 3 else args[2]
  if Path(dest_file).is_file():
    user_input = input('%s already exists, proceed and overwrite? [y|N]: ' % dest_file)
    if not user_input.lower().startswith('y'):
      print('Not overriding file, aborting')
      exit(0)
  if len(args) < 3:
    print('Exporting to default: %s' % (dest_file))
  else:
    print('Exporting to %s' % dest_file)

  parser = ChaParser()
  parser.Convert(source_file, dest_file)
