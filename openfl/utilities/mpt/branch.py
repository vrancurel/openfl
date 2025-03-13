from typing import List

from openfl.utilities.mpt.crypto import keccak256
from openfl.utilities.mpt.nibbles import Nibble
from openfl.utilities.mpt.nodes import EMPTY_NODE_RAW, Node, serialize
from openfl.utilities.mpt.pointer import Pointer, PointerFactory


class BranchNode(Node):
    def __init__(self, pf: PointerFactory):
        self.pf = pf
        self.branches: List[Pointer] = [self.pf.create_pointer(None) for _ in range(16)]
        self.value = bytes()

    def hash(self):
        return keccak256(self.serialize())

    def set_branch(self, nibble: Nibble, node: Node):
        self.branches[int(nibble._value)].set_pointed_value(node)

    def remove_branch(self, nibble: Nibble):
        self.branches[int(nibble._value)].set_pointed_value(None)

    def set_value(self, value: bytes):
        self.value = value

    def remove_value(self):
        self.value = None

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
