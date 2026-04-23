import re
import random
import unittest

from regex import match_substrings
from typing import List
import unittest

class TestRegexProperty(unittest.TestCase):

    alphabet = ["a", "b", "c", "d", "e"]

    def run_property_test(self, regexstr_input:str, alphabet:List[str]):
        
        test_strings = []
        for _ in range(1000):
            length = random.randint(0, 20)
            s = "".join(random.choice(alphabet) for _ in range(length))
            test_strings.append(s)

        result = match_substrings(regexstr_input, alphabet, test_strings=test_strings)

        for s in test_strings:
            expected = re.search(regexstr_input, s) is not None
            actual = result[s]

            self.assertEqual(
                actual,
                expected,
                msg=f"Regex: {regexstr_input} failed on string: {s}"
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
        self.run_property_test("abcd*|cba(abc)+|(abc)+(bdb)(abc)?|a.b.c.d|(((abc)+)+)+", self.alphabet)
        
if __name__ == "__main__":
    unittest.main()