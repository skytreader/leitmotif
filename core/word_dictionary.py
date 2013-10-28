"""
Defines a dictionary structure.

(Actually, just a word list for look-up.)
"""

class WordDictionary(object):
    
    def __init__(self):
        """
        At all times, exclude_list must be a subset of word_list. exclude_list
        and word_list must be iterables.
        """
        self.__exclude_list = None
        self.__word_list = None

    @property
    def exclude_list(self):
        return self.__exclude_list

    @property
    def word_list(self):
        return self.__word_list

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
    
    def __init__(self, filename, exclusions):
        super(SortedFileListDictionary, self).__init__()
        self.__exclude_list = set(exclusions)
        temp_list = []
        
        with open(filename) as words:
            for w in words:
                temp_list.append(w)

        self.__word_list = set(temp_list)

    def lookup(self, word):
        return word in self.word_list

    def exclusive_lookup(self, word):
        return word in self.word_list and word not in self.exclude_list
