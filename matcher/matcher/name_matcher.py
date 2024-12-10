from abc import ABC
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from Levenshtein import ratio
from sklearn.metrics.pairwise import cosine_similarity
from jellyfish import jaro_winkler_similarity as jaro_winkler

class NameMatchScorer:
    """Interface for scoring putative name matches"""
    def __init__(self, name1, name2, threshold=0.5):
        self.name1 = name1
        self.name2 = name2
        self.threshold = threshold

    def __str__(self):
        return f"{self.__class__.__name__}(name1='{self.name1}', name2='{self.name2}')"

    def __repr__(self):
        return self.__str__()

    def score(self, name1, name2):
        pass

class ExactMatchScorer(NameMatchScorer):
    """Exact match scoring implementation"""
    def score(self, name1, name2):
        return 1.0 if name1.lower() == name2.lower() else 0.0

class JaccardScorer(NameMatchScorer):
    """Jaccard similarity implementation"""
    def score(self, name1, name2):
        set1 = set(name1.lower())
        set2 = set(name2.lower())
        
        if not set1 and not set2:
            return 0.0
            
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union

class LevenshteinScorer(NameMatchScorer):
    """Levenshtein distance implementation"""
    def score(self, name1, name2):
        return ratio(name1.lower(), name2.lower())

class TfidfScorer(NameMatchScorer):
    """TF-IDF with cosine similarity implementation"""
    def __init__(self, name1, name2, threshold=0.5, ngram_range=(1, 4)):
        super().__init__(name1, name2, threshold)
        if not (1 <= ngram_range[0] <= ngram_range[1] <= 4):
            raise ValueError("ngram_range must be between 1 and 4")
        self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=ngram_range)

    def score(self, name1, name2):
        # Fit and transform on both names
        tfidf_matrix = self.vectorizer.fit_transform([name1.lower(), name2.lower()])
        return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
class JaroWinklerScorer(NameMatchScorer):
    """Jaro-Winkler similarity implementation"""
    def score(self, name1, name2):
        return jaro_winkler(name1.lower(), name2.lower())