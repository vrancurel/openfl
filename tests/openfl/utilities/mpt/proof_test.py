from openfl.utilities.mpt.proof import Proof
from openfl.utilities.mpt.trie import Trie
from openfl.utilities.mpt.extension import ExtensionNode
from openfl.utilities.mpt.branch import BranchNode
from openfl.utilities.mpt.proof_mem_db import ProofMemDB
from openfl.utilities.mpt.proof import verify_proof
import random
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

    def test_proof_multi(self):
        # Instantiate Trie
        trie = Trie()

        # List for storing paths and values
        data = []

        # Generate a common prefix
        common_prefix = bytes(random.sample(range(97, 122), 3))

        for _ in range(100):
            # Generate a unique suffix for each path: a byte string of 2 random numbers each between 1 and 100
            path_suffix = bytes(random.sample(range(97, 122), 20))
            # Combine the common prefix with the unique suffix to get the path
            path = common_prefix + path_suffix
    
            value = bytes(random.sample(range(97, 122), 5))
            trie.put(path, value)

            data.append((path, value))

        # Then prove all keys
        root_hash = trie.hash()
        for path, original_value in data:

            proof = ProofMemDB()
            ok = trie.prove(path, proof)
            self.assertTrue(ok)

            try:
                value_from_proof = verify_proof(root_hash, path, proof)
            except Exception as e:
                self.fail(f"verify_proof raised an exception: {e} {path}")
            else:
                self.assertEqual(value_from_proof, original_value)

if __name__ == "__main__":
    unittest.main()
