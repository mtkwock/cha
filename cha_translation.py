
# These words are reserved Python words and symbols
reserved_symbols = {
  # Symbols based on https://docs.python.org/3/genindex-Symbols.html
  '的': '.',
  '是': ' = ',  # Assign
  '': ' # ', # Commenting
  '（': '(', '）': ')',
  '【': '[', '】': ']',
  '「': '{', '」': '}',
  '': ' % ', '': ' %= ', # TODO: figure out possible replacement.
  # '': '\'', # These will not appear since quotes are handled.
  # '': '"',

  # Arithmetic operations
  '加': ' + ',
  '减': ' - ',
  '乘': ' * ',
  '除': ' / ',
  '整除': ' // ',
  '幂': ' ** ',
  '加是': ' += ',
  '减是': ' -= ',
  '乘是': ' *= ',
  '除是': ' /= ',
  '整除是': ' //= ',
  '幂是': ' **= ',

  # Binary operations
  '位不': ' ~',  # Negation operator
  '位和': ' & ',  '位和是': ' &= ',
  '位或': ' | ',  '位或是': ' |= ',
  '异或': ' ^ ',  '异或是': ' ^= ',
  '位右': ' >> ', '位右是': ' >>= ',
  '左移': ' << ', '位左是': ' <<= ', # TODO: Make consistent after user testing.

  # Comparators
  '大于': ' > ',
  '大等于': ' >= ',
  '等于': ' == ',
  '小等于': ' <= ',
  '小于': ' < ',
}

# Symbols that should be checked for first.
first_pass_symbols = [key for key in reserved_symbols if key and key[-1] == '是'] + [
  '整除',
]

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
  '真': 'True',
  '假': 'False',
  '无': 'None',
  '和': 'and',
  '或': 'or',
  '不': 'not',
  '跳出': 'break',
  '继续': 'continue', # ji4xu4
}
