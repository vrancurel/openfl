from openfl.utilities.mpt.crypto import keccak256
from openfl.utilities.mpt.nibbles import Nibble
from openfl.utilities.mpt.nodes import EMPTY_NODE_RAW, Node, serialize


class BranchNode(Node):
    def __init__(self):
        self.branches = [None] * 16
        self.value = bytes()

    def hash(self):
        return keccak256(self.serialize())

    def set_branch(self, nibble: Nibble, node: Node):
        self.branches[int(nibble._value)] = node

    def remove_branch(self, nibble: Nibble):
        self.branches[int(nibble._value)] = None

    def set_value(self, value: bytes):
        self.value = value

    def remove_value(self):
        self.value = None

    def raw(self):
        hashes = [None] * 17
        for i in range(16):
            if self.branches[i] is None:
                hashes[i] = EMPTY_NODE_RAW
            else:
                node = self.branches[i]
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
