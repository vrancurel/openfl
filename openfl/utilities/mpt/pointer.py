from collections import deque
from typing import Any


class PointerFactory:
    def __init__(self):
        self.pointer_storage = deque()
        self.pointer_storage.append(None)  # reserve nil pointer
        self.pointer_address = 1

    def new(self, value: Any = None) -> int:
        self.pointer_storage.append(value)
        address = self.pointer_address
        self.pointer_address += 1
        return address

    def get_value_at(self, address: int) -> Any:
        return self.pointer_storage[address]

    def assign(self, address: int, value: Any):
        self.pointer_storage[address] = value
