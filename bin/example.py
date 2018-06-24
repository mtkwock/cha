from cha_base import *
from rénrén import wǒmen
import time

class fāngxiàngjí(ChaObject):
  běi = 0
  nán = 1
  dōng = 2
  xī = 3

class rén(ChaObject):
  def __chūshǐ__(zìjǐ):
    zìjǐ.sùdù = 2
    zìjǐ.yòu = 0
    zìjǐ.shàng = 0
    zìjǐ.qùguòdìfāng = []
    zìjǐ.dìtú = {}

  def zǒu(zìjǐ, jùlí, fāngxiàng):
    """向一个方向移动人。

  价值：
   距离：整数，步行距离。
   方向：方向集，去哪里。
  """
    zìjǐ.qùguòdìfāng += [zìjǐ.yòu, zìjǐ.shàng, time.time()]
    zìjǐ.dìtú[(zìjǐ.yòu, zìjǐ.shàng)] = 1
    if fāngxiàng == fāngxiàngjí.běi:
      zìjǐ.shàng += jùlí
    elif fāngxiàng == fāngxiàngjí.nán:
      zìjǐ.shàng -= jùlí
    elif fāngxiàng == fāngxiàngjí.dōng:
      zìjǐ.yòu += jùlí
    elif fāngxiàng == fāngxiàngjí.xī:
      zìjǐ.yòu -= jùlí
    else: dǎyìn("不好")

dàmíng = rén()
dàmíng.zǒu(30, fāngxiàngjí.běi)

dǎyìn(dàmíng.shàng)
dǎyìn("我是" + str(wǒmen.wǒ))
dǎyìn("你是" + str(wǒmen.nǐ))
dǎyìn("他是" + str(wǒmen.tā))
