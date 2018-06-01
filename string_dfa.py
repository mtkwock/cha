#!bin/bash/env python3

"""Utility to extract String Tokens from an array of tokens."""

from cha_token import StringToken

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

class StringDfa(object):
    """Finds strings in a line of Python."""
    def __init__(self, quote='"', escape='\\'):
        """
        Args:
            quote: Optional[string] The quote character to use.
            escape: Optional[string] The escape character to use.
        """
        self.START = State('Start')
        self.INSIDE = State('Inside')
        self.ESCAPE = State('Escape')
        self.END = State('End')
        self.state = self.START

        self.START.AddDelta(lambda c: c == quote, self.INSIDE)
        self.START.AddDelta(lambda c: c != quote, self.START)
        self.INSIDE.AddDelta(lambda c: c == escape, self.ESCAPE)
        self.INSIDE.AddDelta(lambda c: c == quote, self.END)
        self.INSIDE.AddDelta(lambda c: c not in [quote, escape], self.INSIDE)
        self.ESCAPE.AddDelta(lambda c: True, self.INSIDE)
        self.quote = quote

    def transition(self, char):
        """Transition the Dfa's current state given a charself.

        Args:
          char: string of a single character.
        """
        if self.state != self.START and not isinstance(char, str):
            raise DfaException('Cannot transition with a non string character.')
        self.state = self.state.GetNextState(char)

    def RunString(self, tokens):
        """Search through the tokens and combine string tokens.

        e.g.
        .RunString(['"', 'a', 'b', 'c', '"'])
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
            raise DfaException('String parsing not completed before EOL, uneven number of quotes')
        return res

if __name__ == '__main__':
    my = StringDfa()
    res = my.RunString([c for c in '"def" class 12345'])
    print(res)
