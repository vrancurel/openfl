import unittest
from openfl.utilities.mpt.pointer import PointerFactory


class TestPointer(unittest.TestCase):
    def test_simple(self):
        pf = PointerFactory()
        p1 = pf.new(42)
        self.assertEqual(1, p1)
        self.assertEqual(42, pf.get_value_at(p1))
        p2 = pf.new(43)
        self.assertEqual(2, p2)
        self.assertEqual(43, pf.get_value_at(p2))
        p2 = p1
        self.assertEqual(1, p2)
        self.assertEqual(42, pf.get_value_at(p2))
        pf.assign(p2, 44)
        self.assertEqual(1, p1)
        self.assertEqual(44, pf.get_value_at(p1))


if __name__ == '__main__':
    unittest.main()
