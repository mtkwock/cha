#!/usr/bin/env python

from pinyin import get as pget
from number_variable_dfa import NumberVariableDfa
from string_dfa import StringDfa, MultilineStringDfa
from cha_token import Token, WhitespaceToken, EndToken, SymbolToken, ReservedWordToken, VariableToken, ParseToken, StringToken, MultilineStringToken
from cha_translation import reserved_symbols, symbol_order, reserved_beginning_words, NeedsSpace, PyToCha
import sys
from pathlib import Path

import os

def LastModifiedTime(path):
  # https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
  return os.path.getmtime(path)

# To check if the files need any updating.
_CHA2_MODIFIED_TIME = LastModifiedTime(sys.argv[0])

_OVERRIDE_ALL = any(a == '-y' for a in sys.argv)
_UPDATE_ALL = any(a == '-u' for a in sys.argv)

class ChaParseException(Exception): pass
class ChaNotImplementedException(Exception):
  def __init__(self, name):
    super().__init__(name + ' not implemented')

CHAR_TO_VAR_BASE = {
  '艹艹初始艹艹': '__chūshǐ__', # __init__
  '自己': 'zìjǐ', # self
  '都': 'dōu', # all
  '任何': 'rènhé', # any
  '打印': 'dǎyìn', # print
  '字': 'zì', # str
  '打开': 'dǎkāi', # open
}

VAR_TO_CHAR_BASE = {
  CHAR_TO_VAR_BASE[key]: key for key in CHAR_TO_VAR_BASE
}

# Symbols which should not be seen in the script.
unsupported_symbols = {
  reserved_symbols[key].strip(): key for key in reserved_symbols
}

WHITESPACE_CHARS = frozenset((' ', '\n', '\t'))

def _DefinesClass(tokens):
  """Determines if a line of tokens is attempting to define a class."""
  return tokens[1].GetValue() == PyToCha['class']

def _AddChaObjectToClass(tokens):
  """All classes must inherit from ChaObject, this adds the inherit."""
  if tokens[3].Translate() == '(':
    tokens.insert(4, ParseToken('ChaObject, '))
  else:
    tokens.insert(3, ParseToken('(ChaObject)'))

def HandleClassDefinitions(tokens):
  """Workflow to handle class definition changes."""
  if _DefinesClass(tokens):
    _AddChaObjectToClass(tokens)

def ShouldOverride(source, dest):
  """Determines if a given file and destination file should be overridden."""
  if (not _UPDATE_ALL and
      LastModifiedTime(dest) > LastModifiedTime(source) and
      LastModifiedTime(dest) > _CHA2_MODIFIED_TIME):
    print('File up to date: ' + dest)
    return False
  if _OVERRIDE_ALL:
    return True
  user_input = input('%s already exists, proceed and overwrite? [y|N]: ' % dest_file)
  if not user_input.lower().startswith('y'):
     print('Not overriding file, stopping this conversion')
     return False
  return True

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

def PrettyPrintTokens(tokens):
  string = ''
  for token in tokens:
    token_class = type(token)
    s = token.GetValue()
    if token_class == ReservedWordToken:
      string += bcolors.HEADER + s + bcolors.ENDC
    elif token_class == SymbolToken:
      string += bcolors.OKGREEN + s + bcolors.ENDC
    elif token_class == StringToken or token_class == MultilineStringToken:
      if '\n' in s: s = s.replace('\n', '')
      string += bcolors.WARNING + s + bcolors.ENDC
    else:
        string += s
    print(string)

class ChaParser:
  def __init__(self, directory=''):
    self.char_to_var = dict(CHAR_TO_VAR_BASE)
    self.var_to_char = dict(VAR_TO_CHAR_BASE)
    self.multiline_string_dfa = MultilineStringDfa('“', '”')
    self.string_dfa = StringDfa('“', '”')
    self.number_variable_dfa = NumberVariableDfa()
    self.cwd = directory
    self.imported_files = set()

  def destroy(self):
    self.char_to_var = None
    self.var_to_char = None

  def WhitespaceReplaceTokens(self, tokens):
    """Brings together beginning whitespace and removes all extra whitespace.

    Also adds an EndToken to the end of the token list. Optionally contains comments.
    """
    whitespace = ''
    for token in tokens:
      if token == ' ' or token == '\t':
        whitespace += token
      else:
        break
    token = WhitespaceToken(whitespace)
    if PyToCha['#'] in tokens:
      # import pdb; pdb.set_trace()
      idx = tokens.index(PyToCha['#'])
      comment_tokens = tokens[idx:]
      if any(isinstance(t, Token) for t in comment_tokens):
        import pdb; pdb.set_trace()
      tokens = [*tokens[:idx], EndToken(''.join(comment_tokens))]
    else:
      tokens.append(EndToken())

    f = filter(lambda t: not isinstance(t, str) or t not in WHITESPACE_CHARS, tokens[len(whitespace):])
    return [token, *[t for t in f]]

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
    return [t for t in filter(lambda t: bool(t), tokens)]

  def Tokenize(self, line):
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
    return tokens

  def Translate(self, t):
    if isinstance(t, VariableToken):
      return t.Translate(self.char_to_var, self.var_to_char)
    return t.Translate()

  def HandleImports(self, tokens):
    seen_from = False
    for i in range(1, len(tokens) - 1):
      piece = self.Translate(tokens[i])
      next = tokens[i + 1]
      if piece == 'from' or (not seen_from and piece == 'import'):
        seen_from = piece == 'from'
        if next.GetValue() != self.Translate(next):
          other_file = next.GetValue()
          self.Convert(self.cwd + next.GetValue() + '.cha',
                       self.cwd + self.Translate(next) + '.py')
        # Translate the file defined by right
      elif piece == 'import':
        seen_from = False

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
    tokens = self.Tokenize(line)

    HandleClassDefinitions(tokens)

    self.HandleImports(tokens)

    # Bring tokens together.
    translation = self.Translate(tokens[0])
    for i in range(1, len(tokens) - 1):
      if i == len(tokens) - 2:
        left = tokens[i]
        piece = self.Translate(left)
        translation += piece
        continue
      left, right = tokens[i], tokens[i + 1]
      translation += self.Translate(left)
      if NeedsSpace(left, right):
        translation += ' '
    # TODO: Perhaps also add newline separation for semicolons?
    end = self.Translate(tokens[-1])
    if end:
      if translation.strip():
        translation += '  '
      translation += end
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
    if not Path(source).is_file():
      raise ChaParseException('File does not exist! %s' % source)

    # Do not do duplicate parsing.
    if source in self.imported_files:
      print('Already imported, ignoring: %s' % source)
      return
    self.imported_files.add(source)

    # If it looks like it already exists, determine if it should be handled.
    if Path(dest).is_file() and not ShouldOverride(source, dest):
      return

    with open(source, 'r') as f:
      with open(dest, 'w') as write_file:
        print('Exporting to ' + dest)
        write_file.write('from cha_base import *\n')
        for line in f.readlines():
          l = self.ParseLine(line)
          if not l.endswith('\n'):
            l += '\n'
          write_file.write(l)
    print('Finished converting %s to %s' % (source, dest))

def help_command():
  print("""Converts a given .cha file into a (roughly) equivalent .py file

To use:
$> cha2.py FILE_TO_CONVERT

Optionals:
  -y  Override all values
  -u  Update all files encountered regardless of age.
""")

if __name__ == '__main__':
  args = sys.argv
  if len(args) < 2:
    help_command()
    exit(0)

  source_file = args[1]
  if not source_file.endswith('.cha'):
    raise Exception('Must end with .cha')

  dest_file = source_file[:-3] + 'py'

  directory = '/'.join(source_file.split('/')[:-1])
  if directory: directory += '/'

  parser = ChaParser(directory)
  parser.Convert(source_file, dest_file)
