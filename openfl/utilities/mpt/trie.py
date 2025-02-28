from typing import Optional, Tuple

from openfl.utilities.mpt.branch import BranchNode
from openfl.utilities.mpt.extension import ExtensionNode
from openfl.utilities.mpt.hash import HashNode
from openfl.utilities.mpt.leaf import LeafNode
from openfl.utilities.mpt.nibbles import Nibble
from openfl.utilities.mpt.nodes import EMPTY_NODE_HASH, Node, is_empty_node


class Trie:
    def __init__(self):
        self.root = None

    def hash(self) -> bytes:
        if is_empty_node(self.root):
            return EMPTY_NODE_HASH
        return self.root.hash()

    def get(self, key: bytes) -> Tuple[Optional[bytes], bool]:
        node = self.root
        nibbles = Nibble.from_bytes(key)

        while True:
            if is_empty_node(node):
                return None, False

            if isinstance(node, LeafNode):
                matched = Nibble.prefix_matched_len(node.path, nibbles)
                if matched != len(node.path) or matched != len(nibbles):
                    return None, False
                return node.value, True

            if isinstance(node, BranchNode):
                if len(nibbles) == 0:
                    return (
                        node.value,
                        node.has_value(),
                    )

                b, remaining = nibbles[0], nibbles[1:]
                nibbles = remaining
                node = node.branches[b.to_byte()]
                continue

            if isinstance(node, ExtensionNode):
                matched = Nibble.prefix_matched_len(node.path, nibbles)
                if matched < len(node.path):
                    return None, False

                nibbles = nibbles[matched:]
                node = node.next_
                continue

            raise Exception("Not found")

    def put(self, key: bytes, value: bytes): # noqa: C901
        node = self.root
        nibbles = Nibble.from_bytes(key)

        while True:
            if is_empty_node(node):
                leaf = LeafNode.from_nibbles(nibbles, value)
                self.root = leaf
                return

            if isinstance(node, LeafNode):
                matched = Nibble.prefix_matched_len(node.path, nibbles)

                if matched == len(nibbles) and matched == len(node.path):
                    new_leaf = LeafNode.from_nibbles(node.path, value)
                    self.root = new_leaf
                    return

                branch = BranchNode()

                if matched == len(node.path):
                    branch.set_value(node.value)

                if matched == len(nibbles):
                    branch.set_value(value)

                if matched > 0:
                    ext = ExtensionNode(node.path[:matched], branch)
                    self.root = node = ext
                else:
                    self.root = node = branch

                if matched < len(node.path):
                    branch_nibble, leaf_nibbles = node.path[matched], node.path[matched + 1 :]
                    new_leaf = LeafNode.from_nibbles(leaf_nibbles, node.value)
                    branch.set_branch(branch_nibble, new_leaf)

                if matched < len(nibbles):
                    branch_nibble, leaf_nibbles = nibbles[matched], nibbles[matched + 1 :]
                    new_leaf = LeafNode.from_nibbles(leaf_nibbles, value)
                    branch.set_branch(branch_nibble, new_leaf)

                return

            if isinstance(node, BranchNode):
                if len(nibbles) == 0:
                    node.set_value(value)
                    return

                b, remaining = nibbles[0], nibbles[1:]
                nibbles = remaining
                node = node.branches[b.to_byte()]
                continue

            if isinstance(node, ExtensionNode):
                matched = Nibble.prefix_matched_len(node.path, nibbles)
                if matched < len(node.path):
                    ext_nibbles, branch_nibble, ext_remaining_nibbles = (
                        node.path[:matched],
                        node.path[matched],
                        node.path[matched + 1 :],
                    )
                    branch = BranchNode()

                    if len(ext_remaining_nibbles) == 0:
                        branch.set_branch(branch_nibble, node.next_)
                    else:
                        new_ext = ExtensionNode(ext_remaining_nibbles, node.next_)
                        branch.set_branch(branch_nibble, new_ext)

                    if matched < len(nibbles):
                        node_branch_nibble, node_leaf_nibbles = (
                            nibbles[matched],
                            nibbles[matched + 1 :],
                        )
                        remaining_leaf = LeafNode.from_nibbles(
                            node_leaf_nibbles, value
                        )
                        branch.set_branch(node_branch_nibble, remaining_leaf)
                    elif matched == len(nibbles):
                        branch.set_value(value)
                    else:
                        raise Exception(f"Too many matched ({matched} > {len(nibbles)})")

                    if len(ext_nibbles) == 0:
                        self.root = branch
                    else:
                        self.root = ExtensionNode(ext_nibbles, branch)
                    return

                nibbles = nibbles[matched:]
                node = node.next_
                continue

            raise Exception("Unknown type")

    def dump(self):
        print("Dump")
        node = self.root
        dump_node(node, 0, 0)


def dump_node(node: Node, level: int = 0, idx: int = 0):
    if is_empty_node(node):
        print(f"{level * ' '}{idx} EmptyNode")
        return

    if isinstance(node, LeafNode):
        print(f"{level * ' '}{idx} LeafNode Path={Nibble.list_to_str(node.path)} Value={node.value.hex()}")
        return

    if isinstance(node, HashNode):
        print(f"{level * ' '}{idx} HashNode Hash={node.hash_value.hex()}")
        return

    if isinstance(node, BranchNode):
        print(f"{level * ' '}{idx} BranchNode Value={node.value.hex()}")
        for i in range(16):
            dump_node(node.branches[0], level + 2, i)
        return

    if isinstance(node, ExtensionNode):
        print(f"{level * ' '}{idx} ExtensionNode Path={Nibble.list_to_str(node.path)}")
        dump_node(node.next_, level + 2, 0)
        return

    raise Exception("Unknown type")
