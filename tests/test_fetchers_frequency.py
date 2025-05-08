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


def test_frequency_exist_case_insensitive(mock_frequency_cache):
    with patch("fetchers._frequency_cache", mock_frequency_cache):
        assert frequency_exist("Apple") is True


def test_frequency_exist_empty_string(mock_frequency_cache):
    with patch("fetchers._frequency_cache", mock_frequency_cache):
        assert frequency_exist("") is False


def test_frequency_exist_numeric_string(mock_frequency_cache):
    with patch("fetchers._frequency_cache", mock_frequency_cache):
        assert frequency_exist("123") is False

def test_build_frequency_dict(mock_excel_data):
    expected_dict = {
        "apple": 10.5,
        "banana": 5.0,
        "cherry": 7.2
    }

    with patch("wolern.src.fetchers.pd.read_excel") as mock_read_excel, \
         patch("builtins.open", mock_open()) as mock_file, \
         patch("json.dump") as mock_json_dump:

        # Simulate reading the Excel file
        mock_df = MagicMock()
        mock_df.__getitem__.side_effect = lambda x: mock_excel_data[x]
        mock_df["Word"].str.lower.return_value = [w.lower() for w in mock_excel_data["Word"]]
        mock_read_excel.return_value = mock_df

        build_frequency_dict()

        # Check that the output dictionary was dumped to JSON
        mock_json_dump.assert_called_once_with(
            expected_dict, mock_file(), ensure_ascii=False, indent=2
        )