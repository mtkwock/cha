
# These words are reserved Python words and symbols
reserved_symbols = {
  # Symbols based on https://docs.python.org/3/genindex-Symbols.html
  '的': '.',
  '是': '=',  # Assign
  '是不是': 'is',
  '': '#', # Commenting
  '（': '(', '）': ')',
  '【': '[', '】': ']',
  '「': '{', '」': '}',
  '｛': '{', '｝': '}',
  '': '%', '': '%=', # TODO: figure out possible replacement.
  '：': ':',
  '，':',',
  '、': ',',
  # '': '\'', # These will not appear since quotes are handled.
  # '': '"',

  # Arithmetic operations
  '加': '+',
  '减': '-',
  '乘': '*',
  '除': '/',
  '整除': '//',
  '幂': '**',
  '加是': '+=',
  '减是': '-=',
  '乘是': '*=',
  '除是': '/=',
  '整除是': '//=',
  '幂是': '**=',

  # Binary operations
  '位不': '~',  # Negation operator
  '位和': '&',  '位和是': '&=',
  '位或': '|',  '位或是': '|=',
  '异或': '^',  '异或是': '^=',
  '位右': '>>', '位右是': '>>=',
  '左移': '<<', '位左是': '<<=', # TODO: Make consistent after user testing.

  # Comparators
  '大于': '>',
  '大等于': '>=',
  '等于': '==',
  '小等于': '<=',
  '小于': '<',

  # Reserved words
  '引进': 'import',
  '为': 'as',
  '如果': 'if',
  '否则': 'else',
  '没做什么': 'pass', # Maybe 过?
  '跳出': 'break',
  '继续': 'continue', # ji4xu4
  '确认': 'assert',
  '提出': 'raise', # To Object: 拒绝
  '真': 'True',
  '假': 'False',
  '无': 'None',
  '是不是': 'is',
  '不是': 'is not',
  '和': 'and',
  '或': 'or',
  '不': 'not',
  # TODO: How does this handle for, for-in, for-in-if syntax?
  '每': 'for', # Need to restructure this from B infor A to for A in B
  '在': 'in',
  '拉姆达': 'lambda',
  '产生': 'yield',
  '退还': 'return',
  '删除': 'del',
}

ALWAYS_NEEDS_SPACE = frozenset((
  '=',
  'is',
  '+',
  '-',
  '*',
  '/',
  '//',
  '**',
  '+=',
  '-=',
  '*=',
  '/=',
  '//=',
  '**=',

  '~', '==',
  '&', '&=',
  '|', '|=',
  '^', '^=',
  '>>','>>=',
  '<<','<<=',
  'import',
  'as',
  'if',
  'else',
  'pass',
  'break',
  'continue',
  'assert',
  'raise',
  'True',
  'False',
  'None',
  'is',
  'is not',
  'and',
  'or',
  'not',
  'for',
  'in',
  'lambda',
  'yield',
  'return',
  'del',
  'from',
  'class',
  'def',
  'try',
  'except',
  'while',
  'with',
  'global',
  'nonlocal',
  'finally',
  'elif',
))

def NeedsSpace(left, right):
  l = left.Translate()
  r = right.Translate()
  if l in ALWAYS_NEEDS_SPACE or r in ALWAYS_NEEDS_SPACE:
    if (l, r) == ('else', ':'):
      return False
    return True
  if l in {':', ','}:
    return True
  return False

# Symbols that should be checked for first.
symbol_order = sorted(reserved_symbols.keys(), key=lambda s: -len(s))

number_symbols = {
  '十六进': '0x', # Hex string representation
  '八进': '0o', # Octal string representation
  '二进': '0b', # Binary string representation
  '点': '.', # Decimal point
  '负': '-', # Negative number
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
  'E': 'e', # Allowable for scientific
  # Only for Hex representation.
  'A': 'a',
  'B': 'b',
  'C': 'c',
  'D': 'd',
  'F': 'f',
  # For unset N-Ary values, the value is changed to decimal.
}

# These words are only reserved if they are at the beginning of a line (right
# after whitespace).  A variable may use these if not at the beginning (e.g.
# 人种类, but not 种类人)
reserved_beginning_words = {
  '从': 'from',
  '种类': 'class',
  '定义': 'def',
  '试': 'try',
  '除非': 'except',
  '当': 'while',
  '同': 'with',
  '全面': 'global', # Perhaps 环球?
  '非局部': 'nonlocal',
  '最后': 'finally',
  '否则如果': 'elif', # Although these individual parts will be replaced...
}
sorted_beginning_words = sorted(reserved_beginning_words.keys(), key=lambda s: -len(s))
