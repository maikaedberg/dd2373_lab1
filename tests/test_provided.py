import re
import random
import unittest

from regex import build_minimal_dfa
from typing import List
import unittest

class TestRegexProperty(unittest.TestCase):

    alphabet = ["a", "b", "c", "d", "e"]

    def run_property_test(self, regexstr:str, alphabet:List[str]):
        dfa = build_minimal_dfa(regexstr, alphabet)
        for _ in range(1000):
            length = random.randint(0, 20)
            s = "".join(random.choice(alphabet) for _ in range(length))

            expected = re.search(regexstr, s) is not None
            actual = dfa.partial_match(s)

            self.assertEqual(
                actual,
                expected,
                msg=f"Regex: {regexstr} failed on string: {s}"
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