# Initial test setup for cha2.py

import unittest

from cha2 import ChaParser
from cha_token import Token, WhitespaceToken, SymbolToken

class TestParseLine(unittest.TestCase):
  """Tests the ParseLine function in ChaParser."""
  def setUp(self):
    """Create a new parser to use for each test."""
    self.parser = ChaParser()
    self.ParseLine = self.parser.ParseLine

  def tearDown(self):
    self.parser.destroy()
    self.ParseLine = None

  def case(self, source_line, expected_output):
    """Tests a basic input and output case."""
    output = self.ParseLine(source_line)
    self.assertEqual(expected_output, output)

  def MultilineCase(self, source, expected):
    lines = [self.ParseLine(l) for l in source.split('\n')]
    self.assertEqual(expected, '\n'.join(lines))

  def testBasicClass(self):
    self.case('种类人：', 'class rén(ChaObject):')

  def testExtendedClass(self):
    self.case('种类人（我种类）：', 'class rén(ChaObject, wǒzhǒnglèi):')

  def testSuperExtendedClass(self):
    self.case(
        '种类人（我种类，你种类）：',
        'class rén(ChaObject, wǒzhǒnglèi, nǐzhǒnglèi):')

  def testHandlesBasicSymbols(self):
    self.case('一加一', '1 + 1')

  def testUsesShiAsEqualSign(self):
    self.case('我是不是你', 'wǒ is nǐ')

  def testHandlesFunctionDefinition(self):
    self.MultilineCase('''
 定义走（自己，距离，方向）：
  “““向一个方向移动这个人。

  价值：
   距离：整数，步行距离。
   方向：方向集，去哪里。
  ”””
  自己的去过地方的依附（【自己的右，自己的上，时间的时间（）】）
  自己的地图【（自己的x，自己的y）】是一
''', '''
  def zǒu(zìjǐ, jùlí, fāngxiàng):
    """向一个方向移动这个人。

  价值：
   距离：整数，步行距离。
   方向：方向集，去哪里。
  """
    zìjǐ.qùguòdìfāng.yīfù([zìjǐ.yòu, zìjǐ.shàng, shíjiān.shíjiān()])
    zìjǐ.dìtú[(zìjǐ.x, zìjǐ.y)] = 1
''')

  def testDistinguishesNumberFromVariable(self):
    """Numbers can be used as variable names if they aren't at the beginning."""
    self.case('第一是一', 'dìyī = 1')

  def testSetsNewVariable(self):
    # ren2, a new class, should be created and stored
    case = '种类人：'
    self.assertFalse('人' in self.parser.char_to_var)
    self.ParseLine(case)
    # print(self.parser.char_to_var)
    self.assertTrue('人' in self.parser.char_to_var)
    self.assertEqual('rén', self.parser.char_to_var['人'])
    self.assertEqual('人', self.parser.var_to_char['rén'])

  def testOverlappingPinyin_SetsDifferingVariableNames(self):
    case = '朝们是【超，抄，钞】'
    self.assertEqual('zhāomen = [chāo, chāo1, chāo2]', self.ParseLine(case))
    self.assertEqual('chāo', self.parser.char_to_var['超'])
    self.assertEqual('chāo1', self.parser.char_to_var['抄'])
    self.assertEqual('chāo2', self.parser.char_to_var['钞'])

  def testOverlappingPinyin_IsConsistent(self):
    self.case(
        '朝们是【超，抄，钞，抄，超】',
        'zhāomen = [chāo, chāo1, chāo2, chāo1, chāo]',
    )

class TestSymbolsReplaceTokens(unittest.TestCase):
  def setUp(self):
    parser = ChaParser()
    self.fn = parser.SymbolsReplaceTokens
  def case(self, source_line, expected_output):
    source_line = [t for t in source_line]
    output = self.fn(source_line)
    self.assertEqual(len(output), len(expected_output),
        'Got:\n%s\nExpected:\n%s' % (output, expected_output))
    for i in range(len(expected_output)):
      if isinstance(output[i], Token):
        self.assertEqual(expected_output[i].__class__, output[i].__class__)
        self.assertEqual(expected_output[i].GetValue(), output[i].GetValue())
      else:
        self.assertEqual(expected_output[i], output[i])

  def testEmpty(self):
    self.case('', '')
  def testWhitespaceEmpty(self):
    self.case([WhitespaceToken('')], [WhitespaceToken('')])
  def testSwapsPlus(self):
    self.case(
        [WhitespaceToken(''), '一',             '加',  '一'],
        [WhitespaceToken(''), '一', SymbolToken('加'), '一'])

  def testSwapsPlusEquals_NotPlusThenEquals(self):
    self.case(
        [WhitespaceToken(''), '啊', '加', '是',          '一'],
        [WhitespaceToken(''), '啊', SymbolToken('加是'), '一'])
