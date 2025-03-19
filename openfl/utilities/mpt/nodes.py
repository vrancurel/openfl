from abc import ABC, abstractmethod
from typing import Optional

from rlp import encode

EMPTY_NODE_RAW = b""
EMPTY_NODE_HASH = bytes.fromhex("56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421")


class Node(ABC):
    def __init__(self):
        self._callback = None

    @abstractmethod
    def hash(self):
        pass

    @abstractmethod
    def raw(self):
        pass

    def set_callback(self, callback):
        self._callback = callback


def is_empty_node(node: Optional[Node]) -> bool:
    return node is None


def hash(node):
    if is_empty_node(node):
        return EMPTY_NODE_HASH
    return node.hash()


def serialize(node):
    raw = EMPTY_NODE_RAW if is_empty_node(node) else node.raw()

    try:
        return encode(raw)
    except Exception as err:
        raise RuntimeError("Fail to encode.") from err
