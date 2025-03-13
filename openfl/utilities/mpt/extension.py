from typing import List

from rlp import encode

from openfl.utilities.mpt.crypto import keccak256
from openfl.utilities.mpt.nibbles import Nibble
from openfl.utilities.mpt.nodes import Node, serialize
from openfl.utilities.mpt.pointer import Pointer, PointerFactory


class ExtensionNode(Node):
    def __init__(self, pf: PointerFactory, nibbles: List[Nibble], next_: Node):
        self.pf: PointerFactory = pf
        self.path: List[Nibble] = nibbles
        self.next_: Pointer = self.pf.create_pointer(next_)

    def hash(self) -> bytes:
        return keccak256(self.serialize())

    def raw(self):
        hashes = [None] * 2
        hashes[0] = Nibble.to_bytes(Nibble.to_prefixed(self.path, False))
        next_ = self.next_.get_pointed_value()
        if len(serialize(next_)) >= 32:
            hashes[1] = next_.hash()
        else:
            hashes[1] = next_.raw()
        return hashes

    def serialize(self) -> bytes:
        return encode(self.raw())
