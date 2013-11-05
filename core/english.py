"""
Python listing of various English word categories (articles, pronouns, etc).
Everything is in lowercase.
"""
from utils import get_corpus_path

PRONOUNS = set(("i", "me", "my", "mine", "myself", "we", "us", "our", "ours",
    "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "his",
    "him", "himself", "they", "them", "their", "theirs", "themselves", "she",
    "her", "hers", "herself", "it", "its", "itself"))

ARTICLES = set(("a", "is", "the", "be", "and", "of", "in", "to", "that", "for"
    "with", "on", "do", "this"))

# Relative to the root of this project
TEST_CORPUS_FILENAME = get_corpus_path("corpus/great_expectations.txt")

TEST_CORPUS_TEXT = ""

# Fill up TEST_CORPUS_TEXT with the contents of TEST_CORPUS_FILENAME
with open(TEST_CORPUS_FILENAME) as great_expectations:
    for line in great_expectations:
        TEST_CORPUS_TEXT = "".join((TEST_CORPUS_TEXT, line))
