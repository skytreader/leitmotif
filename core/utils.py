"""
Utility functions for these algorithms. I haven't found anything that provide
these yet.
"""

import os
import re
import unittest

from core_exceptions import UnsurePathException

# Cache so we don't have to construct at every function call
non_word_regex = re.compile(r"\W+")
wordbook_filter = re.compile(r"(\W+|\d)")

# TODO Better way to do this?
package_root = "leitmotif"
package_directory = "core"

def wordbook_sanitize(s):
    """
    Assumes that we are given a string with no spaces. Then, remove an
    punctuation, etc. that may be in the beginning or end of the string.
    """
    sanitized = s
    non_word_match = wordbook_filter.search(sanitized)

    while non_word_match is not None:
        match_span = non_word_match.span()

        if match_span[0] == 0:
            sanitized = sanitized[match_span[1]:len(sanitized)]
        else:
            sanitized = sanitized[0:match_span[0]]

        non_word_match = wordbook_filter.search(sanitized)

    return sanitized

def get_corpus_path(corpus_filepath):
    runpath = os.getcwd()
    runparse = runpath.split(os.sep)

    rundir = len(runparse) - 1
    tld = rundir - 1

    if runparse[tld] == package_root and runparse[rundir] == package_directory:
        return ".." + os.sep + corpus_filepath
    elif runparse[tld] == package_root:
        return corpus_file
    else:
        raise UnsurePathException(corpus_filepath)

class FunctionsTest(unittest.TestCase):
    
    # TODO More unit tests!
    def test_wordbook_sanitize(self):
        sanitations = {"...xkcd":"xkcd", "xkcd...":"xkcd", "...xkcd...":"xkcd",
          "xkcd":"xkcd", "...1xkcd":"xkcd", "1xkcd...":"xkcd",
          "...1xkcd...":"xkcd", "end.":"end"}

        for test in sanitations.keys():
            self.assertEqual(wordbook_sanitize(test), sanitations[test])

if __name__ == "__main__":
    unittest.main()
