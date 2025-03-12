import unittest
from rlp import encode
from openfl.utilities.mpt.nibbles import Nibble
from openfl.utilities.mpt.leaf import LeafNode

class TestLeaf(unittest.TestCase):
    def test_leaf_hash(self):
        self.assertEqual("01020304", bytes([1, 2, 3, 4]).hex())
        self.assertEqual("76657262", bytes("verb", 'utf-8').hex())
        self.assertEqual("01020304", Nibble.list_to_str(Nibble.from_bytes(bytes([1, 2, 3, 4]))))
        self.assertEqual("2001020304", Nibble.list_to_str(Nibble.to_prefixed(Nibble.from_bytes(bytes([1, 2, 3, 4])), True)))
        self.assertEqual(bytes([32, 1, 2, 3, 4]), Nibble.to_bytes(Nibble.to_prefixed(Nibble.from_bytes(bytes([1, 2, 3, 4])), True)))
        self.assertEqual("636f696e", bytes("coin", 'utf-8').hex())

    def test_leaf_node(self):
        l = LeafNode(Nibble.from_bytes(bytes([1, 2, 3, 4])), bytes("verb", 'utf-8'))
        self.assertEqual("2bafd1eef58e8707569b7c70eb2f91683136910606ba7e31d07572b8b67bf5c6", l.hash().hex())

    def test_leaf_node2(self):
        l = LeafNode(Nibble.from_nibble_bytes([5, 0, 6]), bytes("coin", 'utf-8'))
        self.assertEqual("c37ec985b7a88c2c62beb268750efe657c36a585beb435eb9f43b839846682ce", l.hash().hex())

if __name__ == '__main__':
    unittest.main()
