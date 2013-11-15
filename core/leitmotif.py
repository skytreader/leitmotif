import collections
import math
import unittest

from word_tally import WordTally

"""
The module containing the main algorithm for letimotif. Take several WordTally
objects and, by some metric, compare their similarity with each other. Each
WordTally is also labeled as to what text it tallies.
"""

class Leitmotif(object):
    """
    Leitmotif classes are defined by, at least, the following components:

      - how words are counted (word_tally)
      - the comparison method used to compare similarity of word counts
    """
    
    def __init__(self, comparator):
        # FIXME Should this be a set?
        self._word_tallies = []
        self.comparator = comparator
    
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

class IntersectionsLeitmotif(Leitmotif):
    """
    Costly computation for leitmotifs (O(n^2)). The idea is to compare every
    word tally with each other and get the closests ones. Then, get the
    intersection of their most frequent words.

    Closeness is defined as a threshold. All tallies that are at most as far as
    the threshold set are considered "close".

    Properties:
    similarity - A number defining how similar two tallies should be (smaller
    value means more similar tallies).

    closeness - A number defining how many other tallies must any given tally be
    similar to before it is considered close to the set. It should always be
    between 0 and 1. 0 will make the whole set of tallies close (regardless of
    similarity) while 1 would require a tally to be similar to everythin in the
    set.
    
    close_count_limit - Simply ceil(tallies_in_the_set * closeness). The _exact_
    number of tallies to which a given tally must be similar to in order to be
    considered close.
    """
    
    # TODO Take into account how close is it to how many members of the set.
    # That is, view the tallies as a graph and consider how connected a tally
    # is to the rest of the set.
    def __init__(self, comparator, similarity, closeness = 0.5):
        """
        Creates an instance of IntersectionLeitmotif.

        comparator - An instance of CountComparator class to be used for
        comparing tallies.

        similarity - A number defining how similar two tallies should be (smaller
        value means more similar tallies).

        closeness - A number between 0 and 1, defining how many other tallies
        must any given tally be similar to before it is considered close to the
        set. 0 will make the whole set of tallies close while 1 would require
        a tally to be similar to everything in the set. Defaults to 0.5 (tally
        must be similar to at least half the set before it is considered close).
        """
        super(IntersectionsLeitmotif, self).__init__(comparator)
        self.similarity = similarity
        self.closeness = closeness
        self.__close_tallies = set()

        # Initially set to 0 since there should be no tallies in the set yet.
        self.__close_count_limit = 0

    @property
    def close_tallies(self):
        return self.__close_tallies

    @property
    def close_count_limit(self):
        return self.__close_count_limit

    def add_word_tally(self, tally):
        """
        Overridden to compute close_count_limit every time a tally is added.
        """
        # Compute closeness first before calling super method so that closeness
        # computation would not have to check for equality.
        self.__compute_closeness(tally)
        super(IntersectionLeitmotif, self).add_word_tally(tally)
        self.__close_count_limit = int(math.ceil(len(self._word_tallies) * self.closeness))

    def __is_close(self, tally1, tally2):
        distance = self.comparator.compare(tally1, tally2)
        return distance <= self.similarity

    def __compute_closeness(self, tally):
        """
        Compute the closeness of the given tally with the rest of what's already
        added in this class. If they are close enough, the tally is added to
        the close tally set. Nothing is returned.
        """
        similar_count = 0
        
        # FIXME See TODO above!!!
        for t in self._word_tally:
            if self.__is_close(t, tally):
                similar_count += 1

            if similar_count == self.close_count_limit:
                self.__close_tallies.add(tally)

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
