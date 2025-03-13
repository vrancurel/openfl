from typing import List


class Nibble:
    def __init__(self, nibble_byte: int):
        if not self.is_nibble(nibble_byte):
            raise ValueError("Non-nibble byte: %d" % nibble_byte)
        self._value = nibble_byte

    def __str__(self):
        return str(self._value)

    def to_int(self) -> int:
        return self._value

    @staticmethod
    def list_to_str(nibble_list: List["Nibble"]) -> str:
        return "".join(str(nibble) for nibble in nibble_list)

    @staticmethod
    def is_nibble(nibble_byte: int):
        return 0 <= int(nibble_byte) < 16

    @classmethod
    def from_int(cls, i: int) -> "Nibble":
        if not cls.is_nibble(i):
            raise ValueError(f"Non-nibble byte: {i}")
        return cls(i)

    @classmethod
    def from_list_int(cls, l_: List[int]) -> List["Nibble"]:
        return [cls.from_int(i) for i in l_]

    @classmethod
    def from_byte(cls, byte_value: int) -> "Nibble":
        high_nibble = cls(byte_value >> 4)
        low_nibble = cls(byte_value & 0x0F)
        return high_nibble, low_nibble

    @classmethod
    def from_bytes(cls, bytes_seq: bytes) -> List["Nibble"]:
        return [nibble for b in bytes_seq for nibble in cls.from_byte(b)]

    @classmethod
    def from_prefixed(cls, bytes_seq):
        ns = cls.from_bytes(bytes_seq)
        is_leaf_node = ns[0]._value > 1
        chop = 2 - ns[0]._value & 1
        return ns[chop:], is_leaf_node

    def __eq__(self, other):
        if not isinstance(other, Nibble):
            return False
        return self._value == other._value

    @staticmethod
    def to_prefixed(ns: List["Nibble"], is_leaf_node: bool) -> List["Nibble"]:
        if len(ns) % 2:
            prefix_bytes = [Nibble(1)]
        else:
            prefix_bytes = [Nibble(0), Nibble(0)]

        prefixed = prefix_bytes + ns
        if is_leaf_node:
            prefixed[0]._value += 2
        return prefixed

    @staticmethod
    def to_bytes(ns: List["Nibble"]) -> bytes:
        result = []
        for i in range(0, len(ns), 2):
            byte = (ns[i]._value << 4) | ns[i + 1]._value
            result.append(byte)
        return bytes(result)

    @staticmethod
    def prefix_matched_len(node1: List["Nibble"], node2: List["Nibble"]) -> int:
        matched = 0
        for n1, n2 in zip(node1, node2):
            if n1 == n2:
                matched += 1
            else:
                break
        return matched
