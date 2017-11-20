import unittest

from .dafsa import BaseDAFSA

word_test_file = "/home/jed/Develop/PycharmProjects/topolang/dafsa/words_test.txt"


class TestDAFSAMethods(unittest.TestCase):
    def test_addfind(self):
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

    def test_load(self):
        l = []

        with open(word_test_file, "r") as file:
            for w in file.readlines():
                l.append(w.strip('\n'))

        d = BaseDAFSA()
        d.load(word_test_file)

        for w in l:
            self.assertEquals(d.find_word(w), True)

        for w in l:
            self.assertEquals(d.find_word(w + "notword"), False)


if __name__ == '__main__':
    unittest.main()
