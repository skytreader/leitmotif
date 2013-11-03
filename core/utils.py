"""
Utility functions for these algorithms. I haven't found anything that provide
these yet.
"""

import re
import unittest

# Cache so we don't have to construct at every function call
non_word_regex = re.compile(r"\W+")

def sanitize(s):
    """
    Assumes that we are given a string with no spaces. Then, remove an
    punctuation, etc. that may be in the beginning or end of the string.
    """
    sanitized = s
    non_word_match = non_word_regex.search(sanitized)

    while non_word_match is not None:
        match_span = non_word_match.span()

        if match_span[0] == 0:
            sanitized = sanitized[match_span[1]:len(sanitized)]
        else:
            sanitized = sanitized[0:match_span[0]]

        non_word_match = non_word_regex.search(sanitized)

    return sanitized

class FunctionsTest(unittest.TestCase):
    
    # TODO More unit tests!
    def test_sanitize(self):
        tests = {"...xkcd":"xkcd", "xkcd...":"xkcd", "...xkcd...":"xkcd"}

        for test in tests.keys():
            self.assertEqual(sanitize(test), tests[test])

if __name__ == "__main__":
    unittest.main()
