import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from unittest.mock import patch, mock_open, MagicMock
from fetchers import frequency_exist,build_frequency_dict
import pytest
from unittest.mock import patch

@pytest.fixture
def mock_frequency_cache():
    return {"apple": 123.4, "banana": 56.7, "cat": 98.2}

@pytest.fixture
def mock_excel_data():
    return {
        "Word": ["Apple", "Banana", "Cherry"],
        "SUBTLCD": [10.5, 5.0, 7.2]
    }


def test_frequency_exist_true(mock_frequency_cache):
    with patch("fetchers._frequency_cache", mock_frequency_cache):
        assert frequency_exist("apple") is True


def test_frequency_exist_false(mock_frequency_cache):
    with patch("fetchers._frequency_cache", mock_frequency_cache):
        assert frequency_exist("dog") is False

def test_frequency_exist_empty_string(mock_frequency_cache):
    with patch("fetchers._frequency_cache", mock_frequency_cache):
        assert frequency_exist("") is False


def test_frequency_exist_numeric_string(mock_frequency_cache):
    with patch("fetchers._frequency_cache", mock_frequency_cache):
        assert frequency_exist("123") is False

