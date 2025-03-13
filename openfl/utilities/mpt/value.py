from openfl.utilities.mpt.crypto import keccak256
from openfl.utilities.mpt.nodes import Node, serialize

class ValueNode:
    def __init__(self, value: bytes):
        self.value: bytes = value

    @classmethod
    def from_hash(cls, value_hash):
        return cls(value_hash)

    def hash(self) -> bytes:
        return keccak256(self.serialize())

    def raw(self):
        return [self.value]

    def serialize(self):
        return serialize(self)
