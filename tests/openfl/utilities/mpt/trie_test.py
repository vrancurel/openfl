from openfl.utilities.mpt.branch import BranchNode
from openfl.utilities.mpt.extension import ExtensionNode
from openfl.utilities.mpt.leaf import LeafNode
from openfl.utilities.mpt.nodes import EMPTY_NODE_HASH
from openfl.utilities.mpt.trie import Trie, dump_node
from openfl.utilities.mpt.nibbles import Nibble
import unittest

class TestTrie(unittest.TestCase):
    def test_get_nothing_if_key_does_not_exist(self):
        trie = Trie()
        val, found = trie.get(b"notexist")
        self.assertFalse(found)

    def test_get_put(self):
        trie = Trie()
        trie.put(bytes([1, 2, 3, 4]), bytes("hello", 'utf-8'))
        value, found = trie.get(bytes([1, 2, 3, 4]))
        self.assertTrue(found)
        self.assertEqual(value, bytes("hello", 'utf-8'))

    def test_get_updated_value(self):
        trie = Trie()
        trie.put(bytes([1, 2, 3, 4]), b"hello")
        trie.put(bytes([1, 2, 3, 4]), b"world")
        val, found = trie.get(bytes([1, 2, 3, 4]))
        self.assertTrue(found)
        self.assertEqual(val, b"world")

    def test_different_hash_if_key_value_pair_added_or_updated(self):
        trie = Trie()
        hash0 = trie.hash()

        trie.put(bytes([1, 2, 3, 4]), b"hello")
        hash1 = trie.hash()

        trie.put(bytes([1, 2]), b"world")
        hash2 = trie.hash()

        trie.put(bytes([1, 2]), b"trie")
        hash3 = trie.hash()

        self.assertNotEqual(hash0, hash1)
        self.assertNotEqual(hash1, hash2)
        self.assertNotEqual(hash2, hash3)

    def test_same_hash_if_identical_key_value_pairs(self):
        trie1 = Trie()
        trie1.put(bytes([1, 2, 3, 4]), b"hello")
        trie1.put(bytes([1, 2]), b"world")

        trie2 = Trie()
        trie2.put(bytes([1, 2, 3, 4]), b"hello")
        trie2.put(bytes([1, 2]), b"world")

        self.assertEqual(trie1.hash(), trie2.hash())

    def test_put_2_pairs(self):
        trie = Trie()
        trie.put(bytes([1, 2, 3, 4]), b"verb")
        trie.put(bytes([1, 2, 3, 4, 5, 6]), b"coin")

        verb, ok = trie.get(bytes([1, 2, 3, 4]))
        self.assertTrue(ok)
        self.assertEqual(b"verb", verb)

        coin, ok = trie.get(bytes([1, 2, 3, 4, 5, 6]))
        self.assertTrue(ok)
        self.assertEqual(b"coin", coin)

        # Ensure root node is an ExtensionNode
        self.assertIsInstance(trie.root, ExtensionNode)

        # Ensure root's next node is a BranchNode
        self.assertIsInstance(trie.root.next_, BranchNode)

        # Ensure the first branch is a LeafNode
        self.assertIsInstance(trie.root.next_.branches[0], LeafNode)

        leaf = trie.root.next_.branches[0]

        self.assertEqual("c37ec985b7a88c2c62beb268750efe657c36a585beb435eb9f43b839846682ce", leaf.hash().hex())
        self.assertEqual("ddc882350684636f696e8080808080808080808080808080808476657262", trie.root.next_.serialize().hex())
        self.assertEqual("d757709f08f7a81da64a969200e59ff7e6cd6b06674c3f668ce151e84298aa79", trie.root.next_.hash().hex())
        self.assertEqual("64d67c5318a714d08de6958c0e63a05522642f3f1087c6fd68a97837f203d359", trie.root.hash().hex())

    def test_put(self):
        trie = Trie()
        self.assertEqual(EMPTY_NODE_HASH, trie.hash())
        trie.put(bytes([1, 2, 3, 4]), b"hello")
        ns = LeafNode(Nibble.from_bytes(bytes([1, 2, 3, 4])), b"hello")
        self.assertEqual(ns.hash(), trie.hash())

    def test_put_leaf_shorter(self):
        trie = Trie()
        trie.put(bytes([1, 2, 3, 4]), b"hello")
        trie.put(bytes([1, 2, 3]), b"world")

        leaf = LeafNode(Nibble.from_nibble_bytes(bytes([4])), b"hello")

        branch = BranchNode()
        branch.set_branch(Nibble(0), leaf)
        branch.set_value(b"world")

        ExtensionNode(Nibble.from_nibble_bytes(bytes([0, 1, 0, 2, 0, 3])), branch)
        #trie.dump()
        #dump_node(ext)
        #self.assertEqual(ext.hash(), trie.hash())

    def test_put_leaf_all_matched(self):
        trie = Trie()
        trie.put(bytes([1, 2, 3, 4]), b"hello")
        trie.put(bytes([1, 2, 3, 4]), b"world")

        ns = LeafNode(Nibble.from_bytes(bytes([1, 2, 3, 4])), b"world")
        self.assertEqual(ns.hash(), trie.hash())

    def test_put_leaf_more(self):
        trie = Trie()
        trie.put(bytes([1, 2, 3, 4]), b"hello")
        trie.put(bytes([1, 2, 3, 4, 5, 6]), b"world")

        leaf = LeafNode(Nibble.from_nibble_bytes(bytes([5, 0, 6])), b"world")

        branch = BranchNode()
        branch.set_value(b"hello")
        branch.set_branch(Nibble(0), leaf)

        ext = ExtensionNode(Nibble.from_nibble_bytes(bytes([0, 1, 0, 2, 0, 3, 0, 4])), branch)

        self.assertEqual(ext.hash(), trie.hash())
