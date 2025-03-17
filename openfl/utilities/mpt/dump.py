from typing import Optional, Tuple

from openfl.utilities.mpt.branch import BranchNode
from openfl.utilities.mpt.extension import ExtensionNode
from openfl.utilities.mpt.hash import HashNode
from openfl.utilities.mpt.leaf import LeafNode
from openfl.utilities.mpt.nibbles import Nibble
from openfl.utilities.mpt.nodes import Node, is_empty_node


def dump_node(node: Node, level: int = 0, idx: int = 0):
    if is_empty_node(node):
        print(f"{level * ' '}{idx} EmptyNode")
        return

    if isinstance(node, LeafNode):
        print(
            f"{level * ' '}{idx} LeafNode Path={Nibble.list_to_str(node.path)} Value={node.value.hex()}"  # noqa: E501
        )
        return

    if isinstance(node, HashNode):
        print(f"{level * ' '}{idx} HashNode Hash={node.hash_value.hex()}")
        return

    if isinstance(node, BranchNode):
        print(f"{level * ' '}{idx} BranchNode Value={node.value.hex()}")
        for i in range(16):
            dump_node(node.branches[i].get_pointed_value(), level + 2, i)
        return

    if isinstance(node, ExtensionNode):
        print(f"{level * ' '}{idx} ExtensionNode Path={Nibble.list_to_str(node.path)}")
        dump_node(node.next_.get_pointed_value(), level + 2, 0)
        return

    raise Exception("Unknown type")
