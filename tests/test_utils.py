"""
Unit tests for utility functions.
"""

import pytest
from grompt.utils import load_variables


class TestLoadVariables:
    """Test cases for load_variables function."""

    def test_load_variables_from_file(self, tmp_path):
        """Test loading variables from a YAML file."""
        # Create test file
        test_file = tmp_path / "test_inputs.yaml"
        test_file.write_text(
            """
name: World
language: Python
count: 42
"""
        )

        result = load_variables(test_file)

        assert result["name"] == "World"
        assert result["language"] == "Python"
        assert result["count"] == 42

    def test_load_variables_from_string_path(self, tmp_path):
        """Test loading variables using string path."""
        test_file = tmp_path / "vars.yaml"
        test_file.write_text("key: value\n")

        result = load_variables(str(test_file))

        assert result["key"] == "value"

    def test_load_variables_empty_file(self, tmp_path):
        """Test loading from empty file returns empty dict."""
        test_file = tmp_path / "empty.yaml"
        test_file.write_text("")

        result = load_variables(test_file)

        assert result == {}

    def test_load_variables_none_content(self, tmp_path):
        """Test loading file with None content returns empty dict."""
        test_file = tmp_path / "none.yaml"
        test_file.write_text("null")

        result = load_variables(test_file)

        assert result == {}

    def test_load_variables_file_not_found(self):
        """Test loading non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_variables("nonexistent.yaml")

    def test_load_variables_complex_data(self, tmp_path):
        """Test loading complex nested data."""
        test_file = tmp_path / "complex.yaml"
        test_file.write_text(
            """
items:
  - name: item1
    value: 10
  - name: item2
    value: 20
metadata:
  author: Test
  version: 1.0
"""
        )

        result = load_variables(test_file)

        assert len(result["items"]) == 2
        assert result["items"][0]["name"] == "item1"
        assert result["metadata"]["author"] == "Test"
