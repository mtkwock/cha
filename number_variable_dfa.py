#!bin/bash/env python3

"""Utility to extract Number and Variable Tokens from an array of tokens already parsed for other Tokens."""

from cha_token import Token, NumberFormat, NumberToken, VariableToken, ReservedWordToken, WhitespaceToken, SymbolToken

from cha_translation import number_symbols
#from string_dfa import Dfa

class DfaException(Exception):
    """Raised when bad strings are created."""
    pass

class State(object):
    """A single state used by NumberVariableDfa."""
    def __init__(self, state_name):
        # The name given to this State, only for cosmetic purposes.
        self.name = state_name
        # Array of (function, State) tuples.
        # Function returns True if the given character should go to State.
        self.deltas = []
        # Occurs on transition from Ready to other state.
        self.just_started = False
        # for D1 and D2 state
        self.d = None
        # For NARY state
        self.base_s = ''
        self.base_i = None

    def GetNextState(self, char):
        """Returns the first state that accepts the given character.

        Args:
            char: string A string of length 1 with the next char to check.
        Raises:
            DfaException when no transition is defined.
        Returns:
            State a state representing the next object.
        """
        for (fn, ns) in self.deltas:
            if self.name != 'Nary':
                if fn(char):
                    if self.name == 'Ready' and ns.name != 'Ready':
                        self.just_started = True
                    elif ns.name == 'NARY':
                        ns.base_i = int(self.base_s)
                        print('setting base to ' + ns.base_i)
                    elif ns.name == 'D1' or ns.name =='D2':
                        ns.base_s = self.base_s + number_symbols[char]
                    return ns
            else:
                if fn(char, self.base_i):
                    return ns
        raise DfaException('No transition for %s with %s. Invalid Format' % (self.name, char))

    def AddDelta(self, fn, next_state):
        """Adds a new delta to deltas.

        Args:
            fn: function(string): bool A function that takes a single character and returns True or False
            next_state: State The next state to go to with this delta if fn(c) is true.
        """
        self.deltas.append((fn, next_state))

class Dfa(object):
    def __init__(self):
        self.START = State('Start')
        self.END = State('End')
        self.state = self.START

    def transition(self, char):
        self.state = self.state.GetNextState(char)

    def ReplaceTokens(self, tokens):
        raise DfaException('Not Implemented')

class NumberVariableDfa(Dfa):
    """Finds variables and numbers in a list of tokens."""
    def __init__(self):
        super().__init__()
        self.READY = State('Ready')
        self.NEGATIVE = State('Negative')
        self.D1 = State('D1')
        self.D2 = State('D2')
        self.DOT = State('Dot')
        self.VARIABLE = State('Variable')
        self.VAR = State('Var') # END state
        self.ARABIC = State('Arabic') # END state
        self.NARY = State('Nary')
        self.NAR = State('Nar') # END state
        self.FULLNAME = State('Fullname')
        self.FULL = State('Full') # End state
        self.SCIENTIFIC = State('Scientific')

        self.START.AddDelta(lambda c: isinstance(c, Token), self.READY)
        self.READY.AddDelta(lambda c: isinstance(c, Token), self.READY)
        self.READY.AddDelta(lambda c: c == '负', self.NEGATIVE)
        self.READY.AddDelta(lambda c: c == '点', self.DOT)
        self.READY.AddDelta(self.isdigit, self.D1)
        self.READY.AddDelta(self.ischaracter, self.VARIABLE)
        self.READY.AddDelta(self.iss, self.FULLNAME)

        self.VARIABLE.AddDelta(lambda c: isinstance(c, Token), self.VAR)
        self.VARIABLE.AddDelta(lambda c: not isinstance(c, Token), self.VARIABLE)

        self.NEGATIVE.AddDelta(self.iss, self.FULLNAME)
        self.NEGATIVE.AddDelta(self.isdigit, self.D1)

        self.FULLNAME.AddDelta(lambda c: isinstance(c, Token), self.FULL)
        self.FULLNAME.AddDelta(lambda c: self.isdigit(c) or self.iss(c), self.FULLNAME)

        self.D1.AddDelta(lambda c: isinstance(c, Token), self.ARABIC)
        self.D1.AddDelta(self.iss, self.FULLNAME)
        self.D1.AddDelta(lambda c: c == '进', self.NARY)
        self.D1.AddDelta(lambda c: c == 'E', self.SCIENTIFIC)
        self.D1.AddDelta(self.isdigit, self.D2)
        self.D1.AddDelta(lambda c: c == '点', self.DOT)
        self.D1.AddDelta(self.ischaracter, self.VARIABLE)

        self.NARY.AddDelta(lambda c, b: isinstance(c, Token), self.NAR)
        self.NARY.AddDelta(self.ischaracter, self.VARIABLE)
        self.NARY.AddDelta(self.isvaliddigit, self.NARY)

        self.SCIENTIFIC.AddDelta(lambda c: isinstance(c, Token), self.ARABIC)
        self.SCIENTIFIC.AddDelta(self.isdigit, self.SCIENTIFIC)

        self.D2.AddDelta(lambda c: isinstance(c, Token), self.ARABIC)
        self.D2.AddDelta(self.isdigit, self.D2)
        self.D2.AddDelta(lambda c: c == '进', self.NARY)
        self.D2.AddDelta(lambda c: c == '点', self.DOT)
        self.D2.AddDelta(lambda c: c == 'E', self.SCIENTIFIC)
        self.D2.AddDelta(self.ischaracter, self.VARIABLE)

        self.DOT.AddDelta(lambda c: isinstance(c, Token), self.ARABIC)
        self.DOT.AddDelta(self.isdigit, self.DOT)
        self.DOT.AddDelta(self.ischaracter, self.VARIABLE)


    def isdigit(self, char):
        return char in '零一二三四五六七八九'

    def isvaliddigit(self, char, base):
        assert base < 36 and base > 0
        ds = '零一二三四五六七八九ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return ds.find(char) < base

    def ischaracter(self, char, base = 10):
        return char not in '零一二三四五六七八九点十百千万亿E'

    def iss(self, char):
        return char in '十百千万亿'

    def transition(self, char):
        """Transition the Dfa's current state given a charself.

        Args:
            char: string of a single character.
        """
        self.state = self.state.GetNextState(char)
        print(self.state.name)

    def ReplaceTokens(self, tokens):
        """Search through the tokens and combine number and variable tokens.

        e.g.
        .ReplaceTokens([' ', 'a', 'b', 'c', ' '])
            => [VariableToken('abc')]

        .ReplaceTokens([' ', '一', '二', '三', '点',‘四’])
            => [NumberToOken('123.4', format = arabic)]

        Args:
            tokens: Array[char|Token]
        Raises:
            DfaException on invalid number formats
        Returns:
            Array[Token]
        """
        res = []
        s = ''
        for token in tokens:
            self.transition(token)
            if isinstance(token, Token):
                if self.state == self.ARABIC:
                    res.append(NumberToken(s, format = NumberFormat.ARABIC))
                    self.state = self.READY
                elif self.state == self.NAR:
                    res.append(NumberToken(s, format = NumberFormat.NARY))
                    self.state = self.READY
                elif self.state == self.FULL:
                    res.append(NumberToken(s, format = NumberFormat.FULLNAME))
                    self.state = self.READY
                elif self.state == self.VAR:
                    res.append(VariableToken(s))
                    self.state = self.READY
                res.append(token)
            elif self.READY.just_started:
                s = token
                self.READY.just_started = False
            else:
                s += token
        return res

if __name__ == '__main__':
    my = NumberVariableDfa()
    res = my.ReplaceTokens([ReservedWordToken('每'), '茶','茶', ReservedWordToken('当'),'水', ReservedWordToken('里')])
    print(res)
    r2 = my.ReplaceTokens([WhitespaceToken(' '), '我', SymbolToken('是'),'零','一','二','三','点','三',WhitespaceToken(' ')])
    print(r2)
    r3 = my.ReplaceTokens([WhitespaceToken(' '), '我', SymbolToken('是'),'三','七','三','E','三','九',WhitespaceToken(' ')])
    print(r3)
    r4 = my.ReplaceTokens([WhitespaceToken(' '), '我', SymbolToken('是'),'三','十','三','万','五','千',WhitespaceToken(' ')])
    print(r4)
    r5 = my.ReplaceTokens([WhitespaceToken(' '), '我', SymbolToken('是'),'二','进','一','零','一','零',WhitespaceToken(' ')])
    print(r5)
    # r6 should fail
    r6 = my.ReplaceTokens([WhitespaceToken(' '), '我', SymbolToken('是'),'三','三','进','Z','A','B',WhitespaceToken(' ')])
    print(r6)
