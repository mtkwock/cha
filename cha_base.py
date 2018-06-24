
dǎyìn = print
dōu = all
rènhé = any
zì = str
dǎkāi = open

class ChaObject(object):
  def __init__(self, *args, **kwargs):
    self.__chūshǐ__(*args, **kwargs)

  def __chūshǐ__(self, *args, **kwargs):
    """Replacement for __init__ when called. Override."""
    pass
