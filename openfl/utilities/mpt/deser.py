from typing import Optional, Any
from openfl.utilities.mpt.pointer import PointerFactory
from openfl.utilities.mpt.nibbles import Nibble
from openfl.utilities.mpt.nodes import Node
from openfl.utilities.mpt.extension import ExtensionNode
from openfl.utilities.mpt.branch import BranchNode
from openfl.utilities.mpt.hash import HashNode
from openfl.utilities.mpt.leaf import LeafNode

from rlp import decode


def deserialize(pf: PointerFactory, buf: bytes):
    if len(buf) == 0:
        raise ValueError("Unexpected EOF")

    elem = decode(buf)

    return deserialize_internal(pf, elem)


def deserialize_internal(pf: PointerFactory, elem: Any) -> Node:
    print('deserialize_internal', type(elem), elem)
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
    print('deserialize_extension', type(elem[0]), elem[0], type(elem[1]), elem[1])
    if not type(elem[0]) is bytes:
        raise Exception("deserialize extension expecting bytes")
    b = elem[0]
    path, is_leaf_node = Nibble.from_prefixed(b)
    if is_leaf_node:
        return LeafNode(path, elem[1])
    try:
        node = deserialize_ref(pf, elem[1])
    except Exception as err:
        raise Exception(f"deserializing ref error: {str(err)}")
    print('found extension', Nibble.list_to_str(path), node)
    return ExtensionNode(pf, path, node)


def deserialize_branch(pf: PointerFactory, elem: Any) -> Node:
    print('deserialize_branch', type(elem), elem)
    branch_node = BranchNode(pf)
    for index, subelem in enumerate(elem):
        if index < 16:
            try:
                node = deserialize_ref(pf, subelem)
            except Exception as e:
                raise Exception(f"Error deserializing subelem: {str(e)}")
            branch_node.set_branch(Nibble(index), node)
        else:
            branch_node.set_value(subelem)

    return branch_node


def deserialize_ref(pf: PointerFactory, elem: Any) -> Node:
    print('deserialize_ref', type(elem), elem)
    if isinstance(elem, list):
        try:
            node = deserialize_internal(pf, elem)
        except Exception as e:
            raise Exception(f"Deserializing embedded node ref error: {str(e)}")
        return node
    else:
        b = elem
        sz = len(b)
        if sz == 0:
            return None
        elif sz == 32:
            return HashNode(b)
        else:
            raise ValueError(f"Invalid RLP string size: {sz}")
