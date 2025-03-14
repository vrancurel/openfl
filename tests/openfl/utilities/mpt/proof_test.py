from openfl.utilities.mpt.proof import Proof
from openfl.utilities.mpt.trie import Trie
from openfl.utilities.mpt.extension import ExtensionNode
from openfl.utilities.mpt.branch import BranchNode
from openfl.utilities.mpt.proof_mem_db import ProofMemDB
from openfl.utilities.mpt.proof import verify_proof
import unittest

class TestProof(unittest.TestCase):
    def test_trie(self):
        trie = Trie()
        trie.put(bytes([1, 2, 3]), b"hello")
        trie.put(bytes([1, 2, 3, 4, 5]), b"world")

        root = trie.rootp.get_pointed_value()
        self.assertIsInstance(root, ExtensionNode)
        branch = root.next_.get_pointed_value()
        self.assertIsInstance(branch, BranchNode)

        proof = ProofMemDB()
        ok = trie.prove(bytes([1, 2, 3]), proof)
        self.assertTrue(ok)

        root_hash = trie.hash()

        try:
            val = verify_proof(root_hash, bytes([1, 2, 3]), proof)
        except Exception as e:
            self.fail(f"verify_proof raised exception: {e}")
        else:
            self.assertEqual(val, b"hello")

    def test_not_generate_proof_for_nonexistent_key(self):
        trie = Trie()
        trie.put(bytes([1, 2, 3]), b"hello")
        trie.put(bytes([1, 2, 3, 4, 5]), b"world")
        not_exist_key = bytes([1, 2, 3, 4])
        proof = ProofMemDB()
        ok = trie.prove(not_exist_key, proof)
        self.assertFalse(ok)

    def test_generate_proof_for_existing_key_then_verify_with_merkle_root_hash(self):
        trie = Trie()
        trie.put(bytes([1, 2, 3]), b"hello")
        trie.put(bytes([1, 2, 3, 4, 5]), b"world")
        key = bytes([1, 2, 3])
        proof = ProofMemDB()
        ok = trie.prove(key, proof)
        self.assertTrue(ok)

        root_hash = trie.hash()

        try:
            val = verify_proof(root_hash, key, proof)
        except Exception as e:
            self.fail(f"verify_proof raised an exception: {e}")
        else:
            self.assertEqual(val, b"hello")

    def test_fail_verification_if_trie_was_updated(self):
        trie = Trie()
        trie.put(bytes([1, 2, 3]), b"hello")
        trie.put(bytes([1, 2, 3, 4, 5]), b"world")

        # The root hash is taken before the trie is updated
        root_hash = trie.hash()

        # The proof is generated after the trie is updated
        trie.put(bytes([5, 6, 7]), b"trie")
        key = bytes([1, 2, 3])
        proof = ProofMemDB()
        ok = trie.prove(key, proof)
        self.assertTrue(ok)

        # Test should fail the verification since the merkle root hash doesn't match
        try:
            _ = verify_proof(root_hash, key, proof)
        except Exception:
            pass
        else:
            self.fail("Expected an exception from verify_proof")


if __name__ == "__main__":
    unittest.main()
