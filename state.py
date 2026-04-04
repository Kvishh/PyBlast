class State:
    """This is a class used to represent which state the player is currently in.
    There are only two implementations of this for this game: Gameplay and Menu."""

    def __init__(self, state_manager):
        self.state_manager = state_manager

    def update(self):
        """To be overridden by inheritors"""
        pass

class StateManager:
    """This class is used to manage state. It has its only sole attribute which
    is a stack that stores State object and it is represented as a list. This way
    the last State object is the only object that is run."""

    def __init__(self):
        self.state_stack = []

    def run(self):
        """The method only calls the update method of last State object of the stack"""
        if len(self.state_stack) > 1:
            response = self.state_stack[-1].update()
            if response is not None:
                return "retry"
        else:
            response = self.state_stack[0].update()
            if response is not None:
                return "retry"