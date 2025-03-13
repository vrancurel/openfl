from openfl.utilities.mpt.proof import Proof
from openfl.utilities.mpt.trie import Trie
from openfl.utilities.mpt.extension import ExtensionNode
from openfl.utilities.mpt.branch import BranchNode
from openfl.utilities.mpt.proof_mem_db import ProofMemDB
from openfl.utilities.mpt.proof import verify_proof
import unittest

class TestProof(unittest.TestCase):
    def test_trie(self):
        tr = Trie()
        tr.put(bytes([1, 2, 3]), b"hello")
        tr.put(bytes([1, 2, 3, 4, 5]), b"world")

        root = tr.rootp.get_pointed_value()
        self.assertIsInstance(root, ExtensionNode)
        branch = root.next_.get_pointed_value()
        self.assertIsInstance(branch, BranchNode)

        proof = ProofMemDB()
        ok = tr.prove(bytes([1, 2, 3]), proof)
        self.assertTrue(ok)
        
        root_hash = tr.hash()
        
        try:
            val = verify_proof(root_hash, bytes([1, 2, 3]), proof)
        except Exception as e:
            self.fail(f"verify_proof raised exception: {e}")
        else:
            self.assertEqual(val, b"hello")

if __name__ == "__main__":
    unittest.main()
