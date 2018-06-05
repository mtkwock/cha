#!bin/bash/env python

from pinyin import get as pget
from string_dfa import StringDfa, MultilineStringDfa
from cha_token import Token, WhitespaceToken, EndToken, SymbolToken, ReservedWordToken, VariableToken, ParseToken
from cha_translation import reserved_symbols, symbol_order, reserved_beginning_words
import sys
from pathlib import Path

class ChaParseException(Exception): pass
class ChaNotImplementedException(Exception):
  def __init__(self, name):
    super().__init__(name + ' not implemented')

# TODO: Implement and replace.
class NumberVariableDfa():
  def ReplaceTokens(self, tokens):
    result = []
    s = ''
    for t in tokens:
      if isinstance(t, Token):
        if s:
          result.append(VariableToken(s))
          s = ''
        result.append(t)
      else:
        s += t
    print('NumberVariableDfa needs to be implemented!!!')
    return result

CHAR_TO_VAR_BASE = {
  '艹艹初始艹艹': '__chūshǐ__', # __init__
  '自己': 'zìjǐ', # Self
  '都': 'dōu', # All
  '任何': 'rènhé', # Any
}

VAR_TO_CHAR_BASE = {
  CHAR_TO_VAR_BASE[key]: key for key in CHAR_TO_VAR_BASE
}

# Symbols which should not be seen in the script.
unsupported_symbols = {
  reserved_symbols[key].strip(): key for key in reserved_symbols
}

WHITESPACE_CHARS = frozenset((' ', '\n', '\t'))

class ChaParser:
  def __init__(self):
    self.char_to_var = dict(CHAR_TO_VAR_BASE)
    self.var_to_char = dict(VAR_TO_CHAR_BASE)
    self.multiline_string_dfa = MultilineStringDfa('“', '”')
    self.string_dfa = StringDfa('“', '”')
    self.number_variable_dfa = NumberVariableDfa()

  def destroy(self):
    self.char_to_var = None
    self.var_to_char = None

  def WhitespaceReplaceTokens(self, tokens):
    """Brings together beginning whitespace and removes all extra whitespace.

    Also adds an EndToken to the end of the token list.

    """
    whitespace = ''
    for token in tokens:
      if token == ' ' or token == '\t':
        whitespace += token
      else:
        break
    token = WhitespaceToken(whitespace)
    f = filter(lambda t: t not in WHITESPACE_CHARS, tokens[len(whitespace):])

    return [token, *[t for t in f], EndToken()]

  def SymbolsReplaceTokens(self, tokens):
      """Replaces symbol characters symbol tokens."""
      result = list(tokens)
      for symbol in symbol_order:
        if not symbol: continue
        for i in range(len(result) - len(symbol) + 1):
          found = True
          for j in range(len(symbol)):
            if symbol[j] != result[i + j]:
              found = False
              break
          if not found:
            continue
          # import pdb; pdb.set_trace()
          result[i] = SymbolToken(symbol)
          for j in range(len(symbol) - 1):
            result[i + j + 1] = False
      # ReplaceSymbols(reserved_symbols)
      return [t for t in filter(lambda x: bool(x), result)]
  def ReservedWordsReplaceTokens(self, tokens):
    """Replaces reserved names such as class, def, and so on."""
    for word in reserved_beginning_words:
      if not word: continue
      found = True
      for i in range(len(word)):
        # These only need to be checked at the beginning.
        if tokens[i + 1] != word[i]:
          found = False
          break
      if not found: continue
      tokens[1] = ReservedWordToken(word)
      for i in range(1, len(word)):
        tokens[i + 1] = False
    # for word in reserved_words:
    #   if not word: continue # Word not defined.
    #   for i in range(1 + len(tokens) - len(word)):
    #     found = True
    #     for j in range(len(word)):
    #       if tokens[i + j] != word[j]:
    #         found = False
    #         break
    #     if not found: continue
    #     tokens[i] = ReservedWordToken(word)
    #     for j in range(1, len(word)):
    #       tokens[i + j] = False
    return [t for t in filter(lambda t: bool(t), tokens)]

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
    tokens = [c for c in line]
    tokens = self.multiline_string_dfa.ReplaceTokens(
        tokens,
        self.multiline_string_dfa.inside)
    # print('1: %s', tokens)
    tokens = self.string_dfa.ReplaceTokens(tokens)
    # print('2: %s', tokens)
    tokens = self.WhitespaceReplaceTokens(tokens)
    # print('3: %s', tokens)
    tokens = self.ReservedWordsReplaceTokens(tokens)
    # print('4: %s', tokens)
    tokens = self.SymbolsReplaceTokens(tokens)
    # print('5: %s', tokens)
    tokens = self.number_variable_dfa.ReplaceTokens(tokens)
    # print('6: %s', tokens)
    for t in tokens:
      if isinstance(t, str):
        raise ChaParseException('Character not parsed: %s' % t)
    print(tokens)
    # Handle class representation.
    if tokens[1].Translate() == 'class ':
      if tokens[3].Translate() == '(':
        tokens = [*tokens[:4], ParseToken('ChaObject, '), *tokens[4:]]
      else:
        tokens = [*tokens[:3], ParseToken('(ChaObject)'), *tokens[3:]]

    # Bring tokens together.
    translation = ''
    avoid_next = True
    def translate(t):
      if isinstance(t, VariableToken):
        return t.Translate(self.char_to_var, self.var_to_char)
      return t.Translate()
    for t in tokens:
      if any(isinstance(t, token_class) for token_class in [WhitespaceToken, SymbolToken, ReservedWordToken, ParseToken, EndToken]):
        translation += t.Translate()
        avoid_next = True
      elif avoid_next:
        translation += translate(t)
        avoid_next = False
      else:
        translation += ' ' + translate(t)
        avoid_next = False
    return translation

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
