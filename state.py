import pygame

class State:
    def __init__(self, state_manager):
        self.state_manager = state_manager

    def update(self):
        pass

class StateManager:
    def __init__(self):
        self.state_stack = []

    def run(self):
        if len(self.state_stack) > 1:
            response = self.state_stack[-1].update()
            if response is not None:
                return "retry"
        else:
            response = self.state_stack[0].update()
            if response is not None:
                return "retry"