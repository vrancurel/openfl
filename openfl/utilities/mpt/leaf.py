from typing import List

from openfl.utilities.mpt.crypto import keccak256
from openfl.utilities.mpt.nibbles import Nibble
from openfl.utilities.mpt.nodes import Node, serialize


class LeafNode(Node):
    def __init__(self, path: List[Nibble], value: bytes):
        self.path = path
        self.value = value

    # nibbles contains one nibble per byte (for test functions)
    @classmethod
    def from_nibble_bytes(cls, nibbles: bytes, value: bytes) -> "LeafNode":
        return cls(Nibble.from_nibble_bytes(nibbles), value)

    @classmethod
    def from_nibbles(cls, nibbles: List[Nibble], value: bytes) -> "LeafNode":
        return cls(nibbles, value)

    @classmethod
    def from_key_value(cls, key: str, value: str) -> "LeafNode":
        return cls.from_bytes(bytes(key, "utf-8"), bytes(value, "utf-8"))

    @classmethod
    def from_bytes(cls, key: bytes, value: bytes) -> "LeafNode":
        return cls.from_nibbles(Nibble.from_bytes(key), value)

    def hash(self) -> bytes:
        return keccak256(self.serialize())

    def raw(self) -> List[bytes]:
        path = Nibble.to_bytes(Nibble.to_prefixed(self.path, True))
        return [bytes(path), self.value]

    def serialize(self) -> bytes:
        return serialize(self)
