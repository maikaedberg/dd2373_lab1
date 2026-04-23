from regex import match_string
import unittest

class TestRegexSearch(unittest.TestCase):

    # check if all the basic cases
    # Dot, Literal, Closure, OneOrMore, ZeroOrOne, Concatenation, Union)

    alphabet = ["a", "b"]

    def test_literal(self):
        self.assertTrue(match_string("a", "a", self.alphabet))
        self.assertFalse(match_string("a", "b", self.alphabet))
        self.assertFalse(match_string("a", "", self.alphabet))

    def test_dot(self):
        self.assertTrue(match_string(".", "a", self.alphabet))
        self.assertTrue(match_string(".", "b", self.alphabet))
        self.assertFalse(match_string(".", "", self.alphabet))
        self.assertFalse(match_string(".", "aa", self.alphabet))

    def test_closure(self):
        # a*
        self.assertTrue(match_string("a*", "", self.alphabet))
        self.assertTrue(match_string("a*", "a", self.alphabet))
        self.assertTrue(match_string("a*", "aa", self.alphabet))
        self.assertFalse(match_string("a*", "b", self.alphabet))
        self.assertFalse(match_string("a*", "ab", self.alphabet))

    def test_one_or_more(self):
        # a+
        self.assertFalse(match_string("a+", "", self.alphabet))
        self.assertTrue(match_string("a+", "a", self.alphabet))
        self.assertTrue(match_string("a+", "aa", self.alphabet))
        self.assertFalse(match_string("a+", "b", self.alphabet))

    def test_zero_or_one(self):
        # a?
        self.assertTrue(match_string("a?", "", self.alphabet))
        self.assertTrue(match_string("a?", "a", self.alphabet))
        self.assertFalse(match_string("a?", "aa", self.alphabet))
        self.assertFalse(match_string("a?", "b", self.alphabet))

    def test_concatenation(self):
        # ab
        self.assertTrue(match_string("ab", "ab", self.alphabet))
        self.assertFalse(match_string("ab", "a", self.alphabet))
        self.assertFalse(match_string("ab", "b", self.alphabet))
        self.assertFalse(match_string("ab", "aba", self.alphabet))

    def test_union(self):
        # a|b
        self.assertTrue(match_string("a|b", "a", self.alphabet))
        self.assertTrue(match_string("a|b", "b", self.alphabet))
        self.assertFalse(match_string("a|b", "", self.alphabet))
        self.assertFalse(match_string("a|b", "ab", self.alphabet))
        

if __name__ == "__main__":
    unittest.main()