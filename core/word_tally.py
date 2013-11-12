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
        raise NotImplementedError("get_word_count must be implemented.")

    def count(self, text, is_filename = True):
        """
        Counts the occurrences of words in the given text. Note that if the
        is_file flag is set to true, the parameter text is taken as a filename.
        """
        raise NotImplementedError("count must be implemented.")
    
    def get_most_frequent(self):
        """
        Returns a tuple of words containing the most frequent word counts
        encountered so far.

        Can be unimplemented.
        """
        pass

    def get_least_frequent(self):
        """
        Returns a tuple of words containing the least frequent word counts
        encountered so far.

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
        self.__frequent_list = []
        self.__most_frequent_count = 0

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
            w = wordbook_sanitize(w.lower())

            if self.dictionary.lookup(w):
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
        self.sorted_dictionary = SortedFileListDictionary(dictionary_path,
          nonsense_english)

        self.file_tally_keeper = HashTally(self.sorted_dictionary)
        self.raw_tally_keeper = HashTally(self.sorted_dictionary)
        self.test_path = get_corpus_path("corpus/small_sample.txt")
        self.sample = ""
        self.word_set = set()

        with open(self.test_path) as test_file:
            for line in test_file:
                self.sample = "".join([self.sample, line])

                lineparse = line.split(" ")
                for word in lineparse:
                    self.word_set.add(wordbook_sanitize(word.lower()))

        self.file_tally_dos = HashTally(self.sorted_dictionary)
        self.raw_tally_dos = HashTally(self.sorted_dictionary)
        self.test_path_dos = get_corpus_path("corpus/small_sample_dos.txt")
        self.sample_dos = ""
        
        with open(self.test_path) as test_file:
            for line in test_file:
                self.sample_dos = "".join([self.sample_dos, line])

        self.word_set = tuple(self.word_set)

    def test_count(self):
        """
        Test the counting methods.
        """
        self.file_tally_keeper.count(self.test_path)
        self.raw_tally_keeper.count(self.sample, False)

        self.file_tally_dos.count(self.test_path_dos)
        self.raw_tally_dos.count(self.test_path_dos)
        
        # Loop still necessary?
        for i in xrange(50):
            random_word = random.choice(self.word_set)

            unix_file_tally = self.file_tally_keeper.get_word_count(random_word)
            unix_raw_tally = self.raw_tally_keeper.get_word_count(random_word)
            dos_file_tally = self.file_tally_dos.get_word_count(random_word)
            dos_raw_tally = self.raw_tally_dos.get_word_count(random_word)

            if self.sorted_dictionary.lookup(random_word):
                self.assertTrue(unix_file_tally > 0)
                self.assertTrue(unix_raw_tally > 0)
                self.assertTrue(dos_file_tally > 0)
                self.assertTrue(dos_raw_tally > 0)
            else:
                self.assertEqual(unix_file_tally, 0)
                self.assertEqual(unix_raw_tally, 0)
                self.assertEqual(dos_file_tally, 0)
                self.assertEqual(dos_raw_tally, 0)
            self.assertEqual(unix_file_tally, unix_raw_tally)
            self.assertEqual(unix_file_tally, dos_file_tally)
            self.assertEqual(unix_file_tally, dos_raw_tally)

            self.assertEqual(dos_file_tally, dos_raw_tally)
            self.assertEqual(dos_file_tally, unix_raw_tally)

            self.assertEqual(dos_raw_tally, unix_raw_tally)
        
        # a list of all words that occurs four times in the quick brown fox corpus.
        four_list = ("quick", "brown", "fox", "jumps", "over", "lazy", "dog")
        
        for word in four_list:
            self.assertEqual(self.file_tally_keeper.get_word_count(word), 4)
            self.assertEqual(self.raw_tally_keeper.get_word_count(word), 4)
            self.assertEqual(self.file_tally_dos.get_word_count(word), 4)
            self.assertEqual(self.raw_tally_dos.get_word_count(word), 4)

if __name__ == "__main__":
    unittest.main()
