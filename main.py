from state import StateManager
from game import Gameplay
from menu import Menu


if __name__ == "__main__":
    state_manager = StateManager()
    menu = Menu(state_manager)
    state_manager.state_stack.append(menu)

    while True:
        response = state_manager.run()
        if response is not None and response == "retry":
            state_manager.state_stack.append(Gameplay(state_manager))
