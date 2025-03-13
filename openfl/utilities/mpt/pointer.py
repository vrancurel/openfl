from collections import deque
from typing import Any


class Pointer:
    def __init__(self, pf: "PointerFactory", address: int):
        self._pf = pf
        self._address = address

    def get_address(self) -> int:
        return self._address

    def get_pointed_value(self) -> Any:
        address = self.get_address()
        if address == 0:
            raise Exception("Null pointer")
        return self._pf.pointer_storage[address]

    def set_pointed_value(self, value: Any):
        self._pf.pointer_storage[self.get_address()] = value


class PointerFactory:
    Null = None

    def __init__(self):
        self.pointer_storage = deque()
        self.pointer_address = 0
        self.Null = self.create_pointer()

    def create_pointer(self, value: Any = None) -> Pointer:
        self.pointer_storage.append(value)
        p = Pointer(self, self.pointer_address)
        self.pointer_address += 1
        return p
