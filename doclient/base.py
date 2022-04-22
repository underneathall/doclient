from typing import Callable


class CommandView:
    def __init__(self, parent: Callable, *arg, **kwargs):
        self.parent = parent

    def go_to_parent(self):
        return self.parent()
