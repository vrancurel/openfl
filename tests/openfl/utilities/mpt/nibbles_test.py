from openfl.utilities.mpt.nibbles import Nibble
import unittest

class TestNibble(unittest.TestCase):
    def test_is_nibble(self):
        for i in range(20):
            is_nibble = 0 <= i <= 15
            self.assertEqual(is_nibble, Nibble.is_nibble(i), i)

    def test_to_prefixed(self):
        cases = [
            {'ns': [Nibble(1)], 'isLeafNode': False, 'expected': [Nibble(1), Nibble(1)]},
            {'ns': [Nibble(1), Nibble(2)], 'isLeafNode': False, 'expected': [Nibble(0), Nibble(0), Nibble(1), Nibble(2)]},
            {'ns': [Nibble(1)], 'isLeafNode': True, 'expected': [Nibble(3), Nibble(1)]},
            {'ns': [Nibble(1), Nibble(2)], 'isLeafNode': True, 'expected': [Nibble(2), Nibble(0), Nibble(1), Nibble(2)]},
            {'ns': [Nibble(5), Nibble(0), Nibble(6)], 'isLeafNode': True, 'expected': [Nibble(3), Nibble(5), Nibble(0), Nibble(6)]},
            {'ns': [Nibble(14), Nibble(3)], 'isLeafNode': False, 'expected': [Nibble(0), Nibble(0), Nibble(14), Nibble(3)]},
            {'ns': [Nibble(9), Nibble(3), Nibble(6), Nibble(5)], 'isLeafNode': True, 'expected': [Nibble(2), Nibble(0), Nibble(9), Nibble(3), Nibble(6), Nibble(5)]},
            {'ns': [Nibble(1), Nibble(3), Nibble(3), Nibble(5)], 'isLeafNode': True, 'expected': [Nibble(2), Nibble(0), Nibble(1), Nibble(3), Nibble(3), Nibble(5)]},
            {'ns': [Nibble(7)], 'isLeafNode': True, 'expected': [Nibble(3), Nibble(7)]},
        ]
        for case in cases:
            self.assertEqual(case["expected"], Nibble.to_prefixed(case["ns"], case["isLeafNode"]))

    def test_from_bytes(self):
        self.assertEqual([Nibble(0), Nibble(1), Nibble(6), Nibble(4)], Nibble.from_bytes([1, 100]))

    def test_to_bytes(self):
        bytes_ = bytes([0, 1, 2, 3])
        self.assertEqual(bytes_, Nibble.to_bytes(Nibble.from_bytes(bytes_)))

    def test_prefix_matched_len(self):
        self.assertEqual(3, Nibble.prefix_matched_len([Nibble(0), Nibble(1), Nibble(2), Nibble(3)], [Nibble(0), Nibble(1), Nibble(2)]))
        self.assertEqual(4, Nibble.prefix_matched_len([Nibble(0), Nibble(1), Nibble(2), Nibble(3)], [Nibble(0), Nibble(1), Nibble(2), Nibble(3)]))
        self.assertEqual(4, Nibble.prefix_matched_len([Nibble(0), Nibble(1), Nibble(2), Nibble(3)], [Nibble(0), Nibble(1), Nibble(2), Nibble(3), Nibble(4)]))


if __name__ == '__main__':
    unittest.main()
