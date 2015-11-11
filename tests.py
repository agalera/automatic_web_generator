import unittest
import awg


class TestMethods(unittest.TestCase):
    def test_all(self):
        awg.generate()
        
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()

