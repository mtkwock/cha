# cha
Chinese version of Python that compiles into Python.

这是中文版的蟒蛇（python）语言
中英文对照表：
'的': '.',
 '是': ' = ',  # Assign
 '是不是': ' is ',
 '': ' # ', # Commenting
 '（': '(',
 '）': ')',
 '【': '[',
 '】': ']',
 '「': '{',
 '」': '}',
 '余数': ' % ',
 '余数等于': ' %= ',
 '：': ':',
 '，': ', ',
 # '': '\'', # These will not appear since quotes are handled.
 # '': '"',

 # Arithmetic operations
 '加': ' + ',
 '减': ' - ',
 '乘': ' * ',
 '除': ' / ',
 '整除': ' // ',
 '幂': ' ** ',
 '加等于': ' += ',
 '减等于': ' -= ',
 '乘等于': ' *= ',
 '除等于':' /= ',
 '整除等于': ' //= ',
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

 # Reserved words
 '引进': 'import ',
 '为': ' as ',
 '如果': 'if ',
 '否则': 'else',
 '没做什么': 'pass', # Maybe 过?
 '跳出': 'break',
 '继续': 'continue', # ji4xu4
 '确认': 'assert ',
 '提出': 'raise ', # To Object: 拒绝
 '真': 'True',
 '假': 'False',
 '无': 'None',
 '是不是': ' is ',
 '不是': ' is not ',
 '和': ' and ',
 '或': ' or ',
 '不': ' not ',
 # TODO: How does this handle for, for-in, for-in-if syntax?
 '每': 'for ', # Need to restructure this from B infor A to for A in B
 '在': ' in ',
 '拉姆达': 'lambda ',
 '产生': 'yield ',
 '退还': 'return ',
 '删除': 'del ',

 '从': 'from ',
 '种类': 'class ',
 '定义': 'def ',
 '试': 'try',
 '除非': 'except',
 '当': 'while ',
 '同': 'with ',
 '全面': 'global ', # Perhaps 环球?
 '非局部': 'nonlocal ',
 '最后': 'finally',
 '否则如果': 'elif ',
 '物':'object'
