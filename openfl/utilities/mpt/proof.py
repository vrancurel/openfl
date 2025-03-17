import abc
from typing import List

from openfl.utilities.mpt.branch import BranchNode
from openfl.utilities.mpt.deser import deserialize
from openfl.utilities.mpt.extension import ExtensionNode
from openfl.utilities.mpt.hash import HashNode
from openfl.utilities.mpt.leaf import LeafNode
from openfl.utilities.mpt.nibbles import Nibble
from openfl.utilities.mpt.nodes import Node
from openfl.utilities.mpt.pointer import PointerFactory
from openfl.utilities.mpt.value import ValueNode
from openfl.utilities.mpt.dump import dump_node


class Proof(abc.ABC):
    @abc.abstractmethod
    def put(self, key: bytes, value: bytes) -> None:
        pass

    @abc.abstractmethod
    def delete(self, key: bytes) -> None:
        pass

    @abc.abstractmethod
    def has(self, key: bytes) -> bool:
        pass

    @abc.abstractmethod
    def get(self, key: bytes) -> bytes:
        pass

    @abc.abstractmethod
    def serialize(self) -> list[bytes]:
        pass

    @abc.abstractmethod
    def dump(self) -> None:
        pass


def verify_proof(root_hash: bytes, key: bytes, proof: Proof):
    pf = PointerFactory()

    path = Nibble.from_bytes(key)
    want_hash = root_hash

    i = 0
    while True:
        buf = proof.get(want_hash)
        if buf is None:
            raise Exception(f"proof node {i} (hash {want_hash.hex()}) missing")
        try:
            n = deserialize(pf, buf)
        except Exception as err:
            raise Exception(f"bad proof node {i}: {err}")

        path, child = get_child(pf, n, path)

        if child is None:
            return None
        elif isinstance(child, HashNode):
            path = path
            want_hash = child.hash_value
        elif isinstance(child, LeafNode):
            return child.value
        elif isinstance(child, ValueNode):
            return child.value
        i += 1


def get_child(pf: PointerFactory, node: Node, path: List[Nibble]):
    while True:
        if isinstance(node, ExtensionNode):
            if Nibble.prefix_matched_len(path, node.path) != len(node.path):
                return None, None

            path = path[len(node.path) :]
            node = node.next_.get_pointed_value()

        elif isinstance(node, BranchNode):
            if len(path) == 0:
                return Node, ValueNode(node.value)

            node = node.branches[path[0].to_int()].get_pointed_value()
            path = path[1:]

        elif isinstance(node, HashNode):
            return path, node
        elif isinstance(node, LeafNode):
            return None, node
        elif node is None:
            return path, None
        else:
            raise Exception(f"{type(node)}: invalid node: {node}")
