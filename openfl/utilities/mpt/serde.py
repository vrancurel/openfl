from typing import Optional, Any
from openfl.utilities.mpt.pointer import PointerFactory
from openfl.utilities.mpt.nibbles import Nibble
from openfl.utilities.mpt.nodes import Node
from openfl.utilities.mpt.extension import ExtensionNode

from rlp import decode


def deserialize(pf: PointerFactory, buf: bytes):
    if len(buf) == 0:
        raise ValueError("Unexpected EOF")

    elem = decode(buf)

    return deserialize_internal(pf, elem)


def deserialize_internal(pf: PointerFactory, elem: Any) -> Node:
    if isinstance(elem, list):
        c = len(elem)
        if c == 2:
            try:
                node = deserialize_extension(pf, elem)
            except Exception as err:
                raise ValueError(f"deserialize extension error: {err}")
            return node
        elif c == 17:
            try:
                node = deserialize_branch(pf, elem)
            except Exception as err:
                raise ValueError(f"deserialize branch error: {err}")
            return node
        else:
            return ValueError("invalid number of elements")


def deserialize_extension(pf: PointerFactory, elem: Any) -> Node:
    print(type(elem[0]))
    if not type(elem[0]) is bytes:
        raise Exception("deserialize extension expecting bytes")
    b = elem[0]
    path, is_leaf_node = Nibble.from_prefixed(b)
    if is_leaf_node:
        try:
            val = bytes.fromhex(elem[1])
        except Exception as err:
            raise Exception(f"deserializing string error: {str(err)}")
        return LeafNode(path, val)
    try:
        node = deserialize_ref(elem[1])
    except Exception as err:
        raise Exception(f"deserializing ref error: {str(err)}")
    return ExtensionNode(pf, path, node)


def deserialize_branch(elem: Any) -> Node:
    # ...
    # Define this function based on how to handle branch nodes in your codebase
    pass


def deserialize_ref(elem: Any) -> Node:
    # ...
    # Define this function based on how to handle branch nodes in your codebase
    pass
