"""
Defines a dictionary structure.

(Actually, just a word list for look-up. Can be stored in any manner though:
plain lists, binary trees, hashes (?)...pick your own poison. Would also decide
how to load words into memory.)
"""

class WordDictionary(object):
    
    def __init__(self):
        """
        At all times, exclude_list must be a subset of word_list. exclude_list
        and word_list must be iterables.
        """
        self._exclude_list = None
        self._word_list = None

    @property
    def exclude_list(self):
        return self._exclude_list

    @property
    def word_list(self):
        return self._word_list

    def lookup(self, word):
        """
        Returns true if the given word is in the word list.
        """
        pass

    def exclusive_lookup(self, word):
        """
        Same as lookup but takes into consideration the exclude list: will
        return false if the word is in exclude_list.
        """
        pass

class SortedFileListDictionary(WordDictionary):
    """
    Reads its initial dictionary from a text file with one word per line.
    Assumes that the text file has sorted the words by frequency of word use in
    descending order (most frequent first).
    """
    
    def __init__(self, filename, exclusions):
        """
        Create an instance of SortedFileListDictionary. filename is a string
        describing the path of the sorted file list. exclusions is an iterable
        containing the words to exclude from the dictionary.
        """
        super(SortedFileListDictionary, self).__init__()
        self._exclude_list = set(exclusions)
        temp_list = []
        
        with open(filename) as words:
            for w in words:
                temp_list.append(w)

        self._word_list = set(temp_list)

    def lookup(self, word):
        return word in self.word_list

    def exclusive_lookup(self, word):
        return word in self.word_list and word not in self.exclude_list
