import abc
import csv
import collections.abc
import dataclasses
from matcher.name_matcher import NameMatchScorer

@dataclasses.dataclass
class Comparison:
    """Class representing two names and their similarity"""
    name1: str
    name2: str
    score: float = 0.0

class DocIterator(abc.ABC, collections.abc.Iterator):
    def __str__(self):
        return self.__class__.__name__

class TsvIterator(DocIterator):
    """Iterator to iterate over tsv-formatted documents"""
    def __init__(self, path):
        self.path = path
        self.fp = open(self.path)
        self.reader = csv.reader(self.fp, delimiter='\t')
        next(self.reader) # skip first row

    def __iter__(self):
        return self
    def __next__(self):
        try:
            row = next(self.reader)
            return Comparison(row[0], row[1], NameMatchScorer(row[0], row[1]))
        except StopIteration:
            self.fp.close()
            raise