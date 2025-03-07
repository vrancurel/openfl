import unittest
from openfl.utilities.mpt.branch import BranchNode
from openfl.utilities.mpt.leaf import LeafNode
from openfl.utilities.mpt.nibbles import Nibble

class TestBranch(unittest.TestCase):
    def test_branch(self):
        nibbles, value = bytes([5, 0, 6]), bytes("coin", 'utf-8')
        leaf = LeafNode(Nibble.from_nibble_bytes(nibbles), value)

        b = BranchNode()
        b.set_branch(Nibble(0), leaf)
        b.set_value(bytes("verb", 'utf-8'))  # set the value for verb

        print("test 1")
        self.assertEqual("ddc882350684636f696e8080808080808080808080808080808476657262",
                         b.serialize().hex())
        print("test 2")
        self.assertEqual("d757709f08f7a81da64a969200e59ff7e6cd6b06674c3f668ce151e84298aa79",
                         b.hash().hex())


if __name__ == '__main__':
    unittest.main()
