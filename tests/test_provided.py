import re
import random
import unittest

from regex import match_substring

import unittest

class TestRegexProperty(unittest.TestCase):

    alphabet = ["a", "b", "c", "d", "e"]

    def run_property_test(self, regex, alphabet):
        for _ in range(1000):
            length = random.randint(0, 20)
            s = "".join(random.choice(alphabet) for _ in range(length))

            expected = re.search(regex, s) is not None
            actual = match_substring(regex, s, alphabet)

            self.assertEqual(
                actual,
                expected,
                msg=f"Regex: {regex} failed on string: {s}"
            )

    def test_regex_1(self):
        self.run_property_test("abab", self.alphabet)

    def test_regex_2(self):
        self.run_property_test("ab|cde", self.alphabet)

    def test_regex_3(self):
        self.run_property_test("a*bc*(ab)+", self.alphabet)

    def test_regex_4(self):
        self.run_property_test("a+.+b?a+.+b+", self.alphabet)

    def test_regex_5(self):
        self.run_property_test(
            "abcd*|cba(abc)+|(abc)+(bdb)(abc)?|a.b.c.d|(((abc)+)+)+", 
            self.alphabet
        )
        
if __name__ == "__main__":
    unittest.main()