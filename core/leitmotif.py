import collections

from word_tally import WordTally

"""
The module containing the main algorithm for letimotif. Take several WordTally
objects and, by some metric, compare their similarity with each other. Each
WordTally is also labeled as to what text it tallies.
"""

class Leitmotif(object):
    
    def __init__(self):
        self._word_tallies = []
    
    def add_word_tally(self, word_tally):
        """
        A requirement for the word_tally instances that are added to Leitmotif
        instances is that they should override get_most_frequent method. This
        is currently checked by checking the type of get_most_frequent's
        return---it should be an iterable.
        """
        if isinstance(word_tally, WordTally):
            raise TypeError("Not sure if given a WordTally object")

        if isinstance(word_tally.get_most_frequent(), collections.Iterable):
            raise TypeError("WordTally objects given should properly implement get_most_frequent method.")

        self._word_tallies.add(word_tally)

    def leitmotif(self):
        """
        Returns a set of words which is the possible recurring theme
        ("leitmotif") of the texts tallied, as added in this instance.
        """
        raise NotImplementedError("leitmotif must be implemented.")

class CountComparator(object):
    
    def compare(self, tally1, tally2):
        """
        Should return a value of how close tally1 is to tally2. Should return a
        nonnegative number. The smaller the number is, the closer both tallies
        are to each other.
        """
        raise NotImplementedError("compare must be implemented.")

class CartesianComparator(CountComparator):
    """
    Compares WordTally objects by a Cartesian metric. For each of the most
    frequent words in tally1, get how frequent it is in tally2. They will be
    the dimensions of the comparison. The same is done for tally2-tally1 and
    the results are combined.
    """
    
    def compare(self, tally1, tally2):
        """
        Takes the distance between tally1 and tally2 but no square root is
        performed for speed.
        """
        t1_t2 = self.__cartesian_distance(tally1, tally2)
        t2_t1 = self.__cartesian_distance(tally2, tally1)
        return t1_t2 + t2_t1

    def __cartesian_distance(self, t1, t2):
        t1_most_freq = t1.get_most_frequent()
        t1_freq = t1.get_max_frequency()
        running_sum = 0

        for word in t1_most_freq:
            t2_freq = t2.get_word_count(word)
            running_sum += (t1_freq - t2_freq) ** 2

        return running_sum
