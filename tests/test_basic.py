from regex import get_match_complete_strings
import unittest

class TestRegexSearch(unittest.TestCase):

    # check if all the basic cases
    # Dot, Literal, Closure, OneOrMore, ZeroOrOne, Concatenation, Union)

    alphabet = ["a", "b"]

    def test_literal(self):
        result = get_match_complete_strings("a", self.alphabet, test_strings=["a", "b", ""])
        self.assertEqual(result["a"], True)
        self.assertEqual(result["b"], False)
        self.assertEqual(result[""], False)

    def test_dot(self):
        result = get_match_complete_strings(".", self.alphabet, test_strings=["a", "b", ""])
        self.assertEqual(result["a"], True)
        self.assertEqual(result["b"], True)
        self.assertEqual(result[""], False)

    def test_closure(self):
        # a*
        result = get_match_complete_strings("a*", self.alphabet, test_strings=["", "a", "aa", "b", "ab"])
        self.assertEqual(result[""], True)
        self.assertEqual(result["a"], True)
        self.assertEqual(result["aa"], True)
        self.assertEqual(result["b"], False)
        self.assertEqual(result["ab"], False)

    def test_one_or_more(self):
        # a+
        result = get_match_complete_strings("a+", self.alphabet, test_strings=["", "a", "aa", "b"])
        self.assertEqual(result[""], False)
        self.assertEqual(result["a"], True)
        self.assertEqual(result["aa"], True)
        self.assertEqual(result["b"], False)

    def test_zero_or_one(self):
        # a?
        result = get_match_complete_strings("a?", self.alphabet, test_strings=["", "a", "aa", "b"])
        self.assertEqual(result[""], True)
        self.assertEqual(result["a"], True)
        self.assertEqual(result["aa"], False)
        self.assertEqual(result["b"], False)

    def test_concatenation(self):
        # ab
        result = get_match_complete_strings("ab", self.alphabet, test_strings=["ab", "a", "b", "aba"])
        self.assertEqual(result["ab"], True)
        self.assertEqual(result["a"], False)
        self.assertEqual(result["b"], False)
        self.assertEqual(result["aba"], False)

    def test_union(self):
        # a|b
        result = get_match_complete_strings("a|b", self.alphabet, test_strings=["a", "b", "", "ab"])
        self.assertEqual(result["a"], True)
        self.assertEqual(result["b"], True)
        self.assertEqual(result[""], False)
        self.assertEqual(result["ab"], False)
        

if __name__ == "__main__":
    unittest.main()