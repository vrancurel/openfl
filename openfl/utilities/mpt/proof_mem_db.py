from collections import OrderedDict

from openfl.utilities.mpt.proof import Proof


class ProofMemDB(Proof):
    def __init__(self):
        self.kv: OrderedDict = OrderedDict()

    def put(self, key: bytes, value: bytes) -> None:
        self.kv[key.hex()] = value
        # print(f"put key: {key.hex()}, value: {value.hex()}")

    def delete(self, key: bytes) -> None:
        del self.kv[key.hex()]

    def has(self, key: bytes) -> bool:
        return key.hex() in self.kv

    def get(self, key: bytes) -> bytes:
        if not (key := self.kv.get(key.hex())):
            raise KeyError("not found")
        return key

    def serialize(self) -> list[bytes]:
        return list(self.kv.values())

    def dump(self):
        print("Proof")
        for key, value in self.kv.items():
            print(f"- {key}:{value.hex()}")
