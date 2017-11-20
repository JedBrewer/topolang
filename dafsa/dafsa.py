# Default implementation of DAFSA. Will abstract later
# TODO: modify BaseDAFSA.add_word to maintain minimal DAFSA
# TODO: add BaseDAFSA.load method to use add_word to incrementally construct minimal DAFSA
# TODO: add BaseDFSA methods for structural exposition

class BaseDAFSA:
    class _State:
        _transitions = {}

        def __init__(self):
            self.is_final = False
            self.is_nonfinal = True

        def apply(self, symbol):
            return BaseDAFSA._State._transitions[(self, symbol)]

        @classmethod
        def new(cls):
            new_state = cls.__new__(cls)
            new_state.__init__()
            return new_state

        @staticmethod
        def add_transition(state_from, symbol, state_to):
            # This should be changed for production, as duplicate transition keys should never be passed
            if (state_from, symbol) in BaseDAFSA._State._transitions:
                raise LookupError(f"transition from state {state_from} on symbol {symbol} already exists")

            BaseDAFSA._State._transitions[(state_from, symbol)] = state_to

    def __init__(self):
        self._initial_state = BaseDAFSA._State.new()
        self._current_state = self._initial_state

    def add_word(self, word: str):
        if not word:
            raise ValueError("cannot accept empty string")

        self.restart()
        self._check(word)

        word = self._follow(word)
        self._finish(word)

    def find_word(self, word: str):
        if not word:
            return False

        self.restart()
        self._check(word)

        word = self._follow(word)
        return not word and self._current_state.is_final

    def restart(self):
        self._current_state = self._initial_state

    @staticmethod
    def _check(word: str):
        if not (word.isalpha() and word.islower()):
            raise ValueError("can only accept lower-case letters")

    class Transition:
        def __init__(self, state_from, symbol, state_to):
            self._state_from = state_from
            self._symbol = symbol
            self._state_to = state_to

    def _follow(self, word):
        """Follows word up to preexisting prefix and returns remaining suffix"""
        if word:
            try:
                self._current_state = self._current_state.apply(word[0])
                return self._follow(word[1:])
            except KeyError:
                return word

    # Precondition: there are no more existing paths on this suffix
    def _finish(self, suffix):
        """Adds remaining suffix to dafsa"""
        if suffix:
            self._current_state.is_nonfinal = True

        for c in suffix:
            new_state = BaseDAFSA._State.new()
            self._current_state.add_transition(self._current_state, c, new_state)
            self._current_state = new_state

        self._current_state.is_final = True
        self._current_state.is_nonfinal = False
