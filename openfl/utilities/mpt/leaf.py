from typing import List

from openfl.utilities.mpt.crypto import keccak256
from openfl.utilities.mpt.nibbles import Nibble
from openfl.utilities.mpt.nodes import Node, serialize


class LeafNode(Node):
    def __init__(self, path: List[Nibble], value: bytes):
        self.path: List[Nibble] = path
        self.value: bytes = value

    def hash(self) -> bytes:
        return keccak256(self.serialize())

    def raw(self) -> List[bytes]:
        path = Nibble.to_bytes(Nibble.to_prefixed(self.path, True))
        return [bytes(path), self.value]

    def serialize(self) -> bytes:
        return serialize(self)
