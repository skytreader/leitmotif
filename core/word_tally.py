import random
import re
import unittest

from english import PRONOUNS, ARTICLES
from utils import get_corpus_path, wordbook_sanitize
from word_dictionary import SortedFileListDictionary

nonsense_english = PRONOUNS.union(ARTICLES)

class WordTally(object):
    """
    Provides the facility to keep a running tally of words. Note that tally of
    words should be case-insensitive. It is the responsibility of the
    implementations of this class to keep the counting case-insensitive.
    """
    
    def __init__(self, word_dictionary):
        """
        Where word_dictionary is an instance of word_dictionary.WordDictionary. 
        """
        self.__dictionary = word_dictionary
        self.__space_sep = re.compile("\\s+")

    @property
    def dictionary(self):
        return self.__dictionary

    @property
    def space_sep(self):
        return self.__space_sep

    def get_word_count(self, word):
        """
        Returns how many instances of the word have we encountered so far.
        Return 0 if the word has never been encountered before.
        """
        pass

    def count(self, text, is_filename = True):
        """
        Counts the occurrences of words in the given text. Note that if the
        is_file flag is set to true, the parameter text is taken as a filename.
        """
        pass
    
    def get_most_frequent(self):
        """
        Can be unimplemented.
        """
        pass

    def get_least_frequent(self):
        """
        Can be unimplemented.
        """
        pass

class HashTally(WordTally):
    """
    Uses hashmaps to tally words
    """
    
    def __init__(self, word_dictionary):
        super(HashTally, self).__init__(word_dictionary)
        self.__tally = {}

    def get_word_count(self, word):
        word_count = self.__tally.get(word)

        if word_count:
            return word_count
        else:
            return 0
    
    def count(self, text, is_filename = True):
        """
        Word count is maintained as an internal state of this object. Repeated
        invocations of count would increment the internal state.
        """
        if is_filename:
            return self.__count_as_file(text)
        else:
            return self.__count_raw_text(text)

    def __count_flat(self, words):
        """
        Count the words in iterable words and update self.__tally .
        """
        for w in words:
            w = wordbook_sanitize(w)
            if self.__tally.has_key(w):
                self.__tally[w] += 1
            else:
                self.__tally[w] = 1
    
    def __count_as_file(self, filename):    
        with open(filename) as corpus:
            for line in corpus:
                line = line.strip()
                words = self.space_sep.split(line)

                self.__count_flat(words)

    def __count_raw_text(self, text):
        line = text.strip()
        # TODO We should also account for possible newlines inside the text.
        words = self.space_sep.split(line)

        self.__count_flat(words)

class HashTallyTest(unittest.TestCase):
    
    def setUp(self):
        dictionary_path = get_corpus_path("corpus/sorted_word_list.txt")
        sorted_dictionary = SortedFileListDictionary(dictionary_path,
          nonsense_english)

        self.file_tally_keeper = HashTally(sorted_dictionary)
        self.raw_tally_keeper = HashTally(sorted_dictionary)
        self.test_path = get_corpus_path("corpus/small_sample.txt")
        self.great_expectations = ""
        self.word_set = set()

        with open(self.test_path) as test_file:
            for line in test_file:
                self.great_expectations = "".join([self.great_expectations, line])

                lineparse = line.split(" ")
                for word in lineparse:
                    self.word_set.add(word)

        self.word_set = tuple(self.word_set)

    def test_count(self):
        """
        Test the counting methods.
        """
        self.file_tally_keeper.count(self.test_path, True)
        self.raw_tally_keeper.count(self.great_expectations, False)
        
        for i in xrange(50):
            random_word = random.choice(self.word_set)
            self.assertEqual(self.file_tally_keeper.get_word_count(random_word),
              self.raw_tally_keeper.get_word_count(random_word))

if __name__ == "__main__":
    unittest.main()
