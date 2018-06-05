# Valid whole name numbers.
cases = [
  ('零', 0),
  ('零点', 0),
  ('零点一', 0.1),
  ('一', 1),
  ('一二', 12),
  ('十二', 12),
  ('三十二', 32),
  ('百', 100),
  ('两百', 200),
  ('百零二', 102),
  ('一百零二', 102),
  ('一百二十三', 123),
  ('一百二', 120), # 120
  ('二百五', 0), # 250 = idiot
  ('千', 1000),
  ('两千', 2000),
  ('两千一', 2100), # Shorthand
  ('两千两百二十二', 2222),
  ('二千零零七', 2007),
  # Weird, but allowable
  ('两十', 20),
  ('二千', 2000),
  ('二万', 20000),
  ('二进一零一零一零一', '0b1010101'), # Direct binary support
  ('八进一二三四五六七零', '0o12345670'), # Direct octal support
  ('一六进FF00FF', '0xff00ff'), # Direct hexadecimal support.
  ('一二进BB', 143), # Supports other bases, but is calculated.
  ('三六进ZZ', 1295), # Supports up to base 36 using English letters, but is calculated (35 * 36 + 35)
  ('', 0),
  ('', 0),
]

not_numbers = [
  '十十',
  '亿亿',
  '七亿二亿',
  '十二百', # 100 after 10 is nonsensical without 万 or 亿 between them.
  '二进一零一零一零二', # Cannot support numbers greater than the base.
  '一二进BC', # Does not support C as part of the extended alphabet.
  '三七进一零一', # Does not support > base 36.
]
