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
