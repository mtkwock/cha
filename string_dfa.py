#!bin/bash/env python3

"""Utility to extract String Tokens from an array of tokens."""

from cha_token import StringToken, MultilineStringToken

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

class StringDfa(Dfa):
    """Finds strings in a line of Python."""
    def __init__(self, start_quote='"', end_quote='"', escape='\\'):
        """
        Args:
            quote: Optional[string] The quote character to use.
            escape: Optional[string] The escape character to use.
        """
        super().__init__()
        self.INSIDE = State('Inside')
        self.ESCAPE = State('Escape')

        self.START.AddDelta(lambda c: c == start_quote, self.INSIDE)
        self.START.AddDelta(lambda c: c != start_quote, self.START)
        self.INSIDE.AddDelta(lambda c: c == escape, self.ESCAPE)
        self.INSIDE.AddDelta(lambda c: c == end_quote, self.END)
        self.INSIDE.AddDelta(lambda c: c not in [end_quote, escape], self.INSIDE)
        self.ESCAPE.AddDelta(lambda c: True, self.INSIDE)

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

class MultilineStringDfa(Dfa):
    def __init__(self, start_quote='"', end_quote='"', escape='\\'):
        super().__init__()
        # Single Quote found
        self.Q1 = State('Q1')
        # Double Quote found
        self.Q2 = State('Q2')
        # Triple Quote found
        self.INSIDE = State('Inside')
        self.ESCAPE = State('Escape')
        # One quote found to maybe end the multiline.
        self.U1 = State('U1')
        # Two quotes found to maybe end the multiline.
        self.U2 = State('U2')
        # Three quotes found to end the multiline

        self.inside = False

        is_start_quote = lambda c: c == start_quote
        not_start_quote = lambda c: c != start_quote
        is_end_quote = lambda c: c == end_quote
        not_end_quote = lambda c: c != end_quote
        default = lambda c: True

        self.START.AddDelta(is_start_quote, self.Q1)
        self.START.AddDelta(default, self.START)
        self.Q1.AddDelta(is_start_quote, self.Q2)
        self.Q1.AddDelta(default, self.START)
        self.Q2.AddDelta(is_start_quote, self.INSIDE)
        self.Q2.AddDelta(default, self.START)
        self.INSIDE.AddDelta(lambda c: c == escape, self.ESCAPE)
        self.INSIDE.AddDelta(is_end_quote, self.U1)
        self.INSIDE.AddDelta(default, self.INSIDE)
        self.ESCAPE.AddDelta(default, self.INSIDE)
        self.U1.AddDelta(is_end_quote, self.U2)
        self.U1.AddDelta(default, self.INSIDE)
        self.U2.AddDelta(is_end_quote, self.END)
        self.U2.AddDelta(default, self.INSIDE)

    def ReplaceTokens(self, tokens, inside=False):
        """Replaces tokens with MultilineStringToken for valid syntaxes.

        Args:
            tokens: Array[string] An array of characters to replace.
            inside: Optional[bool] Whether this line starts as part of a multiline.
        """
        self.state = self.INSIDE if inside else self.START

        res = []
        s = ''
        for token in tokens:
            self.transition(token)

            if self.state == self.START:
                if s:
                    res += [c for c in s]
                    s = ''
                res.append(token)
            elif self.state == self.END:
                res.append(MultilineStringToken(s + token))
                s = ''
                self.state = self.START
            else:
                s += token

        # Handles rest of line assuming the multiline hasn't ended yet.
        if self.state in [self.INSIDE, self.ESCAPE, self.U1, self.U2]:
            self.inside = True
            res += [MultilineStringToken(s)]
        else:
            if s:
                res += [c for c in s]
            self.inside = False

        return res


if __name__ == '__main__':
    my = StringDfa()
    res = my.ReplaceTokens([c for c in '"def" class 12345'])
    print(res)
