import cha_token


t1 = cha_token.NumberToken('三亿零三十三', cha_token.NumberFormat.FULLNAME)
print(t1.Translate())
t2 = cha_token.NumberToken('十三', cha_token.NumberFormat.FULLNAME)
print(t2.Translate())
t3 = cha_token.NumberToken('十', cha_token.NumberFormat.FULLNAME)
print(t3.Translate())
t4 = cha_token.NumberToken('五千五百二十', cha_token.NumberFormat.FULLNAME)
print(t4.Translate())
t5 = cha_token.NumberToken('三千五百万', cha_token.NumberFormat.FULLNAME)
print(t5.Translate())
t5 = cha_token.NumberToken('一万', cha_token.NumberFormat.FULLNAME)
print(t5.Translate())
t5 = cha_token.NumberToken('七百五十五万零三千四百九十九', cha_token.NumberFormat.FULLNAME)
print(t5.Translate())
