# Default implementation of DAFSA. Will abstract later

# TODO: add BaseDAFSA.add_word_incr to maintain minimal DAFSA
# TODO: add BaseDAFSA.load_incr method to use add_word to incrementally construct minimal DAFSA

# TODO: add BaseDFSA methods for structural exposition
from typing import Optional


class BaseDAFSA:
    class _State:
        _transitions = {}

        def __init__(self):
            self.is_final = False
            self.children = []

        # TODO: Override BaseDAFSA._State.__eq__
        # To be used for determining state equivalency
        # Precondition: all children of both states must be registered already
        def __eq__(self, other):
            return self.__str__() == str(other)

        # Should represent itself as a concatenation of each of the
        # 3 byte ID of its children along with their associated transition symbol
        def __str__(self):
            ...

        # Note: equivalent states will hash to same bucket (maybe useful?)
        def __hash__(self):
            return self.__str__().__hash__()

        # 3 byte ID of state
        def _id(self):
            ...

    def __init__(self):
        self._initial_state = BaseDAFSA._State()
        self._current_state = self._initial_state
        self._transitions = {}
        self._register = []

    def add_word(self, word: str):
        if not word:
            raise ValueError("cannot accept empty string")

        self.restart()
        self._check(word)

        word = self._follow(word)
        self._finish(word)

    def load(self, filename: str):
        with open(filename, "r") as file:
            for line in file.readlines():
                self.add_word(line.strip('\n'))

    def minimize(self):
        self._minimize(self._initial_state)

    def _minimize(self, state: _State):
        for c in state.children:
            p = self.apply(state, c)

            self._minimize(p)
            q = self._find_equivalent(p)

            if q:
                self.remove_transition(state, c, p)
                self.add_transition(state, c, q)
            else:
                self._register.append(p)

    def apply(self, state: _State, c: str) -> _State:
        return self._transitions[(state, c)]

    def add_transition(self, state_from: _State, symbol: str, state_to: _State):
        # This should be changed for production, as duplicate transition keys should never be passed
        if (state_from, symbol) in self._transitions:
            raise LookupError(f"transition from state {state_from} on symbol {symbol} already exists")

        self._transitions[(state_from, symbol)] = state_to

    def remove_transition(self, state_from: _State, symbol: str, state_to: _State):
        try:
            mapped_state = self._transitions[(state_from, symbol)]
            if mapped_state is not state_to:
                raise LookupError(f"({state_from}, {symbol}) maps to {mapped_state}, not {state_to}. Cannot delete")
            del self._transitions[(state_from, symbol)]
        except KeyError:
            pass

    def find_word(self, word: str) -> bool:
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

    def _follow(self, word: str) -> str:
        """Follows word up to preexisting prefix and returns remaining suffix"""
        if word:
            try:
                self._current_state = self.apply(self._current_state, word[0])
                return self._follow(word[1:])
            except KeyError:
                return word

    # Precondition: there are no more existing paths on this suffix
    def _finish(self, suffix: str):
        """Adds remaining suffix to dafsa"""
        for c in suffix:
            new_state = BaseDAFSA._State()
            self.add_transition(self._current_state, c, new_state)
            self._current_state.children.append(c)
            self._current_state = new_state

        self._current_state.is_final = True

    def _find_equivalent(self, p: _State) -> Optional[_State]:
        for q in self._register:
            if q == p:
                return q

        return None
