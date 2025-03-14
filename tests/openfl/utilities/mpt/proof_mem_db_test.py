import unittest
from openfl.utilities.mpt.proof_mem_db import ProofMemDB

class TestProofMemDB(unittest.TestCase):
    def setUp(self):
        self.proof_db = ProofMemDB()

    def test_put(self):
        self.proof_db.put(b'key', b'value')
        self.assertEqual(self.proof_db.get(b'key'), b'value')

    def test_has(self):
        self.proof_db.put(b'key', b'value')
        self.assertTrue(self.proof_db.has(b'key'))
        self.assertFalse(self.proof_db.has(b'non-existent-key'))

    def test_delete(self):
        self.proof_db.put(b'key', b'value')
        self.assertTrue(self.proof_db.has(b'key'))
        self.proof_db.delete(b'key')
        self.assertFalse(self.proof_db.has(b'key'))

    def test_serialize(self):
        self.proof_db.put(b'key', b'value')
        self.proof_db.serialize()
        # Check the serialized_db structure

if __name__ == "__main__":
    unittest.main()
