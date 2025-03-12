import unittest
from openfl.utilities.mpt.branch import BranchNode
from openfl.utilities.mpt.leaf import LeafNode
from openfl.utilities.mpt.nibbles import Nibble
from openfl.utilities.mpt.extension import ExtensionNode

class TestExtensionNode(unittest.TestCase):
    def test_extension_node(self):
        leaf = LeafNode(Nibble.from_list_int([5, 0, 6]), bytes("coin", 'utf-8'))

        b = BranchNode()
        b.set_branch(Nibble(0), leaf)
        b.set_value(bytes("verb", 'utf-8'))  # set the value for verb

        e = ExtensionNode(Nibble.from_list_int([0, 1, 0, 2, 0, 3, 0, 4]), b)

        self.assertEqual("e4850001020304ddc882350684636f696e8080808080808080808080808080808476657262", e.serialize().hex())
        self.assertEqual("64d67c5318a714d08de6958c0e63a05522642f3f1087c6fd68a97837f203d359", e.hash().hex())

if __name__ == '__main__':
    unittest.main()
