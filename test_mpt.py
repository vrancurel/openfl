import os
from openfl.utilities.mpt.trie import Trie
from openfl.utilities.mpt.proof import verify_proof
from openfl.utilities.mpt.proof_mem_db import ProofMemDB
from hashlib import sha384

directory = './data'

trie = Trie()

def _compute_file_hash(file_path: str) -> str:
    """Compute the hash of the file. Return hash on hexstring format."""
    sha384_hash = sha384()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha384_hash.update(byte_block)
        return sha384_hash.hexdigest()


i=0
for dirpath, dirnames, filenames in os.walk(directory):
    print(f'Found directory: {dirpath}')
    for file_name in filenames:
        full_path = os.path.join(dirpath, file_name)
        print(full_path)
        hash = _compute_file_hash(full_path)
        trie.put(bytes(full_path, 'utf-8'), bytes(hash, 'utf-8'))
        i += 1

#trie.dump()
root_hash = trie.hash()
print('root hash', root_hash)
print('proof')
for dirpath, dirnames, filenames in os.walk(directory):
    print(f'Found directory: {dirpath}')
    for file_name in filenames:
        full_path = os.path.join(dirpath, file_name)
        print(full_path)
        hash = _compute_file_hash(full_path)
        proof = ProofMemDB()
        ok = trie.prove(bytes(full_path, 'utf-8'), proof)
        if not ok:
            raise Exception(f"invalid path {full_path}")
        val = verify_proof(root_hash, bytes(full_path, 'utf-8'), proof)
        if val != bytes(hash, 'utf-8'):
            raise Exception(f"invalid hash {val} != {hash}")
