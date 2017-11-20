import unittest

from .dafsa import BaseDAFSA


class TestDAFSAMethods(unittest.TestCase):
    def test_init(self):
        words = ["car", "carp", "carton", "carbide", "cartoon", "cat", "dad", "house"]

        d = BaseDAFSA()
        for word in words:
            d.add_word(word)
        for word in words:
            self.assertEquals(d.find_word(word), True)

        self.assertEquals(d.find_word("cart"), False)
        self.assertEquals(d.find_word("dog"), False)
        self.assertEquals(d.find_word(""), False)
        with self.assertRaises(ValueError):
            d.add_word("")


if __name__ == '__main__':
    unittest.main()
