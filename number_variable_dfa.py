#!bin/bash/env python3

"""Utility to extract Number and Variable Tokens from an array of tokens already parsed for other Tokens."""

from cha_token import NumberFormat, NumberToken, VariableToken
#from string_dfa import Dfa

class DfaException(Exception):
    """Raised when bad strings are created."""
    pass

class State(object):
    """A single state used by StringDfa."""
    def __init__(self, state_name):
        # The name given to this State, only for cosmetic purposes.
        self.name = state_name
        # Array of (function, State) tuples.
        # Function returns True if the given character should go to State.
        self.deltas = []
        # Occurs on transition from Start to Inside.
        self.just_started = False

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
            if fn(char):
                if self.name == 'Start':
                    self.just_started = True
                return ns
        raise DfaException('No transition for %s with %s' % (self.name, char))

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

class Number_Variable_Dfa(Dfa):
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
        self.FULLNAME = State('Fullname') # End state
        self.FULL = State('Full')
        self.SCIENTIFIC = State('Scientific')

        self.START.AddDelta(lambda c: isinstance(c, Token), self.READY)
        self.READY.AddDelta(lambda c: c == '负', self.NEGATIVE)
        self.READY.AddDelta(lambda c: c == '点', self.DOT)
        self.READY.AddDelta(self.isdigit, self.D1)
        self.READY.AddDelta(self.ischaracter, self.VARIABLE)

        self.VARIABLE.AddDelta(lambda c: isinstance(c, Token), self.VAR)
        self.VARIABLE.AddDelta(lambda c: not isinstance(c, Token), self.VARIABLE)

        self.NEGATIVE.AddDelta()

        self.INSIDE.AddDelta(lambda c: c == escape, self.ESCAPE)
        self.INSIDE.AddDelta(lambda c: c == end_quote, self.END)
        self.INSIDE.AddDelta(lambda c: c not in [end_quote, escape], self.INSIDE)
        self.ESCAPE.AddDelta(lambda c: True, self.INSIDE)


    def isdigit(self, char):
        return char in '零一二三四五六七八九'

    def ischaracter(self, char):
        return char not in '零一二三四五六七八九点十百千万亿E'

    def transition(self, char):
        """Transition the Dfa's current state given a charself.

        Args:
            char: string of a single character.
        """
        if self.state != self.START and not isinstance(char, str):
            raise DfaException('Cannot transition with a non string character.')
        self.state = self.state.GetNextState(char)

    def ReplaceTokens(self, tokens):
        """Search through the tokens and combine string tokens.

        e.g.
        .ReplaceTokens(['"', 'a', 'b', 'c', '"'])
            => [StringToken('"abc"')]

        Args:
            tokens: Array[string|MultilineStringToken]
        Raises:
            DfaException on an uneven number of strings
        Returns:
            Array[string|StringToken|MultilineStringToken]
        """
        res = []
        s = ''
        for token in tokens:
            self.transition(token)
            if self.state == self.START:
                res.append(token)
            elif self.START.just_started:
                s = token
                self.START.just_started = False
            elif self.state == self.END:
                s+= token
                res.append(StringToken(s))
                self.state = self.START
            else: # When the state is inside and escape.
                s += token
        # In the case of uneven quotes, the state will not be .START at the end.
        if self.state != self.START:
            self.state = self.START
            raise DfaException('String parsing not completed before EOL, uneven number of quotes')
        return res
