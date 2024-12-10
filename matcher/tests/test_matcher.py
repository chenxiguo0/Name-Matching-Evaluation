import pytest
from matcher.name_matcher import ExactMatchScorer, JaccardScorer, LevenshteinScorer, TfidfScorer

def test_exact_match():
    scorer = ExactMatchScorer("John", "John")
    assert scorer.score("John", "John") == 1.0
    assert scorer.score("John", "jane") == 0.0

def test_jaccard_similarity():
    scorer = JaccardScorer("night", "light")
    score = scorer.score("night", "light")
    assert 0 <= score <= 1
    assert score > 0.5  

def test_levenshtein_distance():
    scorer = LevenshteinScorer("kitten", "sitting")
    score = scorer.score("kitten", "sitting")
    assert 0 <= score <= 1
    assert score < 0.5  

def test_tfidf_scorer():
    scorer = TfidfScorer("Robert", "Bob")
    score = scorer.score("Robert", "Bob")
    assert 0 <= score <= 1