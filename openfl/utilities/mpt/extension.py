from typing import List

from rlp import encode

from openfl.utilities.mpt.crypto import keccak256
from openfl.utilities.mpt.nibbles import Nibble
from openfl.utilities.mpt.nodes import Node, serialize


class ExtensionNode(Node):
    def __init__(self, nibbles: List[Nibble], next_: Node):
        self.path = nibbles
        self.next_ = next_

    def hash(self) -> bytes:
        return keccak256(self.serialize())

    def raw(self):
        hashes = [None] * 2
        hashes[0] = Nibble.to_bytes(Nibble.to_prefixed(self.path, False))
        if len(serialize(self.next_)) >= 32:
            hashes[1] = self.next_.hash()
        else:
            hashes[1] = self.next_.raw()
        return hashes

    def serialize(self) -> bytes:
        return encode(self.raw())
