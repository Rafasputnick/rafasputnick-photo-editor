from concurrent.futures.process import _threads_wakeups

CHANGE = True
NO_CHANGES = False


class UndoReundo:
    def __init__(self):
        self.current_state: int = 0
        self.state_history = []
        self.in_sequence = False
        self.count_sequence = 0

    def reset_sequence(self):
        self.in_sequence = False
        self.count_sequence = 0

    def continue_sequence(self):
        self.count_sequence += 1
        self.in_sequence = True

    def register_change(self, state):
        while len(self.state_history) > (self.current_state + 1):
            self.state_history.pop()

        self.state_history.append(state)
        self.reset_sequence()

        if len(self.state_history) > 1:
            self.current_state += 1

    def undo(self):
        if len(self.state_history) > 0 and self.current_state > 0:
            self.continue_sequence()
            self.current_state -= 1
            return self.state_history[self.current_state], CHANGE

        return self.current_state, NO_CHANGES

    def in_histoty_range(self):
        return self.current_state < (len(self.state_history) - 1)

    def reundo(self):
        if (
            len(self.state_history) > 0
            and self.current_state >= 0
            and self.in_histoty_range()
        ):
            self.continue_sequence()
            self.current_state += 1
            return self.state_history[self.current_state], CHANGE
        return self.current_state, NO_CHANGES
