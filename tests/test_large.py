import re
import random
import unittest

from regex import match_substrings

import unittest

class TestRegexProperty(unittest.TestCase):

    def run_property_test(self, regexstr_input, alphabet):

        test_strings = []

        for i in range(1000):
            if i == 0: # test first on empty string
                s = ""
            else:
                length = random.randint(1, 100)
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