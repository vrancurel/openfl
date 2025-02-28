from abc import ABC, abstractmethod
from typing import Optional

from rlp import decode, encode

EMPTY_NODE_RAW = b""
EMPTY_NODE_HASH = bytes.fromhex("56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421")


class Node(ABC):
    @abstractmethod
    def hash(self):
        pass

    @abstractmethod
    def raw(self):
        pass


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


def deserialize(buf):
    return deserialize_unsafe(buf.copy())


def deserialize_unsafe(buf):
    if len(buf) == 0:
        raise ValueError("Unexpected EOF")

    elem = decode(buf)

    return deserialize_internal(elem)


def deserialize_internal(elem):
    # Handling for specific counts would go here
    # Placeholder values used
    # You would replace with actual classes in your codebase
    ExtensionNode = None
    BranchNode = None
    pass
    if isinstance(elem, list):
        c = len(elem)
        # More thorough instance checking would be needed for a full conversion
        if c == 2:
            try:
                return ExtensionNode(elem)
            except Exception as err:
                raise ValueError(f"deserialize extension error: {err}")
        elif c == 17:
            try:
                return BranchNode(elem)
            except Exception as err:
                raise ValueError(f"deserialize branch error: {err}")
        else:
            return ValueError("invalid number of elements")


def deserialize_extension(elem):
    # ...
    # Define this function based on how to handle extension nodes in your codebase
    pass


def deserialize_branch(elem):
    # ...
    # Define this function based on how to handle branch nodes in your codebase
    pass
