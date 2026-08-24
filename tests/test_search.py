import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__),"..","src"))

from search import  matches_filename_pattern, SearchResult, SearchResultCollector

def test_matches_filename_pattern_case_insensitive():
    assert matches_filename_pattern("MyReport.txt", "report")==True

def test_matches_filename_pattern_no_match():
    assert matches_filename_pattern("photo.jpg", "report")==False