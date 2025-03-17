from typing import Optional, Tuple

from openfl.utilities.mpt.branch import BranchNode
from openfl.utilities.mpt.extension import ExtensionNode
from openfl.utilities.mpt.hash import HashNode
from openfl.utilities.mpt.leaf import LeafNode
from openfl.utilities.mpt.nibbles import Nibble
from openfl.utilities.mpt.nodes import EMPTY_NODE_HASH, Node, hash, is_empty_node, serialize
from openfl.utilities.mpt.dump import dump_node
from openfl.utilities.mpt.pointer import Pointer, PointerFactory
from openfl.utilities.mpt.proof import Proof


class Trie:
    def __init__(self):
        self.pf: PointerFactory = PointerFactory()
        self.rootp: Pointer = self.pf.create_pointer(None)

    def hash(self) -> bytes:
        root = self.rootp.get_pointed_value()
        if is_empty_node(root):
            return EMPTY_NODE_HASH
        return root.hash()

    def get(self, key: bytes) -> Tuple[Optional[bytes], bool]:
        nodep = self.rootp
        nibbles = Nibble.from_bytes(key)

        while True:
            node = nodep.get_pointed_value()

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
                nodep = node.branches[b.to_int()]
                continue

            if isinstance(node, ExtensionNode):
                matched = Nibble.prefix_matched_len(node.path, nibbles)
                if matched < len(node.path):
                    return None, False

                nibbles = nibbles[matched:]
                nodep = node.next_
                continue

            raise Exception("Not found")

    def put(self, key: bytes, value: bytes):  # noqa: C901
        nodep = self.rootp
        nibbles = Nibble.from_bytes(key)

        while True:
            node = nodep.get_pointed_value()

            if is_empty_node(node):
                leaf = LeafNode(nibbles, value)
                nodep.set_pointed_value(leaf)
                return

            if isinstance(node, LeafNode):
                matched = Nibble.prefix_matched_len(node.path, nibbles)
                if matched == len(nibbles) and matched == len(node.path):
                    leaf = LeafNode(node.path, value)
                    nodep.set_pointed_value(leaf)
                    return

                branch = BranchNode(self.pf)

                if matched == len(node.path):
                    branch.set_value(node.value)

                if matched == len(nibbles):
                    branch.set_value(value)

                if matched > 0:
                    ext = ExtensionNode(self.pf, node.path[:matched], branch)
                    nodep.set_pointed_value(ext)
                else:
                    nodep.set_pointed_value(branch)

                if matched < len(node.path):
                    branch_nibble, leaf_nibbles = node.path[matched], node.path[matched + 1 :]
                    leaf = LeafNode(leaf_nibbles, node.value)
                    branch.set_branch(branch_nibble, leaf)

                if matched < len(nibbles):
                    branch_nibble, leaf_nibbles = nibbles[matched], nibbles[matched + 1 :]
                    leaf = LeafNode(leaf_nibbles, value)
                    branch.set_branch(branch_nibble, leaf)

                return

            if isinstance(node, BranchNode):
                if len(nibbles) == 0:
                    node.set_value(value)
                    return

                b, remaining = nibbles[0], nibbles[1:]
                nibbles = remaining
                nodep = node.branches[b.to_int()]
                continue

            if isinstance(node, ExtensionNode):
                matched = Nibble.prefix_matched_len(node.path, nibbles)
                if matched < len(node.path):
                    ext_nibbles, branch_nibble, ext_remaining_nibbles = (
                        node.path[:matched],
                        node.path[matched],
                        node.path[matched + 1 :],
                    )
                    branch = BranchNode(self.pf)

                    if len(ext_remaining_nibbles) == 0:
                        branch.set_branch(branch_nibble, node.next_.get_pointed_value())
                    else:
                        ext = ExtensionNode(
                            self.pf, ext_remaining_nibbles, node.next_.get_pointed_value()
                        )
                        branch.set_branch(branch_nibble, ext)

                    if matched < len(nibbles):
                        node_branch_nibble, node_leaf_nibbles = (
                            nibbles[matched],
                            nibbles[matched + 1 :],
                        )
                        remaining_leaf = LeafNode(node_leaf_nibbles, value)
                        branch.set_branch(node_branch_nibble, remaining_leaf)
                    elif matched == len(nibbles):
                        branch.set_value(value)
                    else:
                        raise Exception(f"Too many matched ({matched} > {len(nibbles)})")

                    if len(ext_nibbles) == 0:
                        nodep.set_pointed_value(branch)
                    else:
                        ext = ExtensionNode(self.pf, ext_nibbles, branch)
                        nodep.set_pointed_value(ext)
                    return

                nibbles = nibbles[matched:]
                nodep = node.next_
                continue

            raise Exception("Unknown type")

    def prove(self, key: bytes, proof: Proof) -> bool:
        nodep = self.rootp
        nibbles = Nibble.from_bytes(key)

        while True:
            node = nodep.get_pointed_value()
            proof.put(hash(node), serialize(node))

            if is_empty_node(node):
                return False

            if isinstance(node, LeafNode):
                matched = Nibble.prefix_matched_len(node.path, nibbles)
                if matched != len(node.path) or matched != len(nibbles):
                    return False

                return True

            if isinstance(node, BranchNode):
                if len(nibbles) == 0:
                    return node.has_value()

                b, remaining = nibbles[0], nibbles[1:]
                nibbles = remaining
                nodep = node.branches[b.to_int()]
                continue

            if isinstance(node, ExtensionNode):
                matched = Nibble.prefix_matched_len(node.path, nibbles)

                if matched < len(node.path):
                    return False

                nibbles = nibbles[matched:]
                nodep = node.next_
                continue

            raise Exception("Not Found")

    def dump(self):
        root = self.rootp.get_pointed_value()
        dump_node(root, 0, 0)
