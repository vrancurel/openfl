from Crypto.Hash import keccak


def keccak256(s: str) -> str:
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(s)
    return keccak_hash.digest()
