import unittest
from openfl.utilities.mpt.pointer import PointerFactory


class TestPointer(unittest.TestCase):
    def test_null(self):
        pf = PointerFactory()
        self.assertEqual(0, pf.Null.get_address())
        with self.assertRaises(Exception):
            pf.get_pointed_value(pf.Null)
        
    def test_simple(self):
        pf = PointerFactory()
        p1 = pf.create_pointer(42)
        self.assertEqual(1, p1.get_address())
        self.assertEqual(42, p1.get_pointed_value())
        p2 = pf.create_pointer(43)
        self.assertEqual(2, p2.get_address())
        self.assertEqual(43, p2.get_pointed_value())
        p2 = p1
        self.assertEqual(1, p2.get_address())
        self.assertEqual(42, p2.get_pointed_value())
        p2.set_pointed_value(44)
        self.assertEqual(1, p1.get_address())
        self.assertEqual(44, p1.get_pointed_value())


if __name__ == '__main__':
    unittest.main()
