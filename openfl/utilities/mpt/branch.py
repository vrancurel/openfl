from functools import lru_cache
from typing import List

from openfl.utilities.mpt.crypto import keccak256
from openfl.utilities.mpt.nibbles import Nibble
from openfl.utilities.mpt.nodes import EMPTY_NODE_RAW, Node, serialize
from openfl.utilities.mpt.pointer import Pointer, PointerFactory


class BranchNode(Node):
    def __init__(self, pf: PointerFactory):
        self.pf: PointerFactory = pf
        self.branches: List[Pointer] = [self.pf.create_pointer(None) for _ in range(16)]
        self.value: bytes = bytes()
        self.set_callback(lambda: self.clear_cache())

    def notify_update(self):
        """Call this method whenever there's an update in this node."""
        if self._callback is not None:
            self._callback()

    @lru_cache(maxsize=None)  # noqa: B019
    def hash(self):
        return keccak256(self.serialize())

    def set_branch(self, nibble: Nibble, node: Node):
        if node is not None:
            node.set_callback(self.notify_update)
        self.branches[int(nibble._value)].set_pointed_value(node)
        self.clear_cache_and_notify()

    def remove_branch(self, nibble: Nibble):
        self.branches[int(nibble._value)].set_pointed_value(None)
        self.clear_cache_and_notify()

    def set_value(self, value: bytes):
        self.value = value
        self.clear_cache_and_notify()

    def remove_value(self):
        self.value = None
        self.clear_cache_and_notify()

    @lru_cache(maxsize=None)  # noqa: B019
    def raw(self):
        hashes = [None] * 17
        for i in range(16):
            if self.branches[i].get_pointed_value() is None:
                hashes[i] = EMPTY_NODE_RAW
            else:
                node = self.branches[i].get_pointed_value()
                if len(serialize(node)) >= 32:
                    hashes[i] = node.hash()
                else:
                    hashes[i] = node.raw()
        hashes[16] = self.value
        return hashes

    def serialize(self):
        return serialize(self)

    def has_value(self):
        return self.value is not None

    def clear_cache(self):
        self.hash.cache_clear()
        self.raw.cache_clear()

    def clear_cache_and_notify(self):
        self.clear_cache()
        self.notify_update()
