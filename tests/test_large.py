import re
import random
import unittest

from regex import match_substring

import unittest

class TestRegexProperty(unittest.TestCase):


    def run_property_test(self, regex, alphabet):

        
        for i in range(1000):
            if i == 0: # test first on empty string
                s = ""
            else:
                length = random.randint(1, 20)
                s = "".join(random.choice(alphabet) for _ in range(length))

            expected = re.search(regex, s) is not None
            actual = match_substring(regex, s, alphabet)

            self.assertEqual(
                actual,
                expected,
                msg=f"Regex: {regex} failed on string: {s}"
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