import re
import random
import unittest

from regex import build_minimal_dfa

import unittest

class TestRegexProperty(unittest.TestCase):

    def run_property_test(self, regexstr, alphabet):

        dfa = build_minimal_dfa(regexstr, alphabet)

        for i in range(1000):
            if i == 0: # test first on empty string
                s = ""
            else:
                length = random.randint(1, 20)
                s = "".join(random.choice(alphabet) for _ in range(length))

            expected = re.search(regexstr, s) is not None
            actual = dfa.partial_match(s)

            self.assertEqual(
                actual,
                expected,
                msg=f"Regex: {regexstr} failed on string: {s}"
            )

    def test_regex_1(self):
        self.run_property_test("(a|b)*abb(a|b)*", ["a", "b"])

    def test_regex_2(self):
        self.run_property_test("(ab)*|(cd)+(ef)?(gh|ij)*kl+", list("abcdefghijkl"))

    def test_regex_3(self):
        self.run_property_test("a+b*c+d?e+f*g+h?i+j*", list("abcdefghij"))

    def test_regex_4(self):
        self.run_property_test("a+.+b?a+.+b+", ["a", "b"])

    def test_regex_5(self):
        self.run_property_test(
            "((ab|cd)*(ef|gh)+)|(((ij)+|(kl)?)(mn|op)+(qr)*st+)", 
            list("abcdefghijklmnopqrst")
        )
        
if __name__ == "__main__":
    unittest.main()