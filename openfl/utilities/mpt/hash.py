from typing import List

from openfl.utilities.mpt.crypto import keccak256
from openfl.utilities.mpt.nodes import Node, serialize


class HashNode(Node):
    def __init__(self, hash_value: bytes):
        self.hash_value = hash_value

    @staticmethod
    def new_hash_node(hash_value: bytes) -> "HashNode":
        return HashNode(hash_value=hash_value)

    def hash(self) -> bytes:
        return keccak256(self.serialize())

    def raw(self) -> List[bytes]:
        raw = [self.hash_value]
        return raw

    def serialize(self) -> bytes:
        return serialize(self)
