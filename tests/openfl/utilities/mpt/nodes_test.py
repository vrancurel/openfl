import unittest
from rlp import encode
from openfl.utilities.mpt.nodes import EMPTY_NODE_RAW, EMPTY_NODE_HASH
from openfl.utilities.mpt.crypto import keccak256

class TestEmptyNodeHash(unittest.TestCase):

    def test_empty_node_hash(self):
        empty_rlp = encode(EMPTY_NODE_RAW)
        self.assertEqual(EMPTY_NODE_HASH, keccak256(empty_rlp))


if __name__ == '__main__':
    unittest.main()
