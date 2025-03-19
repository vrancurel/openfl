from functools import lru_cache
from typing import List

from openfl.utilities.mpt.crypto import keccak256
from openfl.utilities.mpt.nodes import serialize


class ValueNode:
    def __init__(self, value: bytes):
        self.value: bytes = value

    @classmethod
    def from_hash(cls, value_hash):
        return cls(value_hash)

    @lru_cache(maxsize=None)  # noqa: B019
    def hash(self) -> bytes:
        return keccak256(self.serialize())

    @lru_cache(maxsize=None)  # noqa: B019
    def raw(self) -> List[bytes]:
        return [self.value]

    def serialize(self):
        return serialize(self)
