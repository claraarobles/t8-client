"""
This module contains automated tests for the `utc_to_timestamp` function from the
`timestamp.py` module.

The tests verify that the function correctly converts UTC-formatted dates to timestamps
and properly handles error cases, such as invalid formats or incorrect data types.

Included tests:
- `test_valid_date`: Verifies that a valid UTC date is correctly converted to a
    timestamp.
- `test_another_valid_date`: Verifies another valid UTC date.
- `test_invalid_format`: Ensures that a `ValueError` is raised for invalid date formats.
- `test_empty_string`: Verifies that an empty string raises a `ValueError`.
- `test_non_string_input`: Ensures that a `TypeError` is raised if the input is not a
    string.
"""
from src.t8_client.functions.timestamp import utc_to_timestamp

# Constants for expected values
EXPECTED_TIMESTAMP_2023_03_15 = 1678883445

def test_valid_date() -> None:
    """Test with a valid UTC date."""
    # Verify that the function correctly converts a valid UTC date string to a timestamp
    assert utc_to_timestamp("2023-03-15T12:30:45") == EXPECTED_TIMESTAMP_2023_03_15

# Constants for expected values
EXPECTED_TIMESTAMP_2000_01_01 = 946684800

def test_another_valid_date() -> None:
    """Test with another valid UTC date."""
    # Verify that the function correctly converts another valid UTC date string
    # to a timestamp
    assert utc_to_timestamp("2000-01-01T00:00:00") == EXPECTED_TIMESTAMP_2000_01_01

def test_invalid_format() -> None:
    """Test with an invalid date format."""
    # Ensure the function raises a ValueError when the input date format is incorrect
    try:
        utc_to_timestamp("2023/03/15 12:30:45")
        raise AssertionError("Expected a ValueError exception")
    except ValueError:
        pass  # This error was expected

def test_empty_string() -> None:
    """Test with an empty string."""
    # Ensure the function raises a ValueError when the input is an empty string
    try:
        utc_to_timestamp("")
        raise AssertionError("Expected a ValueError exception")
    except ValueError:
        pass  # This error was expected

def test_non_string_input() -> None:
    """Test with an incorrect data type (integer)."""
    # Ensure the function raises a TypeError when the input is not a string
    try:
        utc_to_timestamp(1678883445)
        raise AssertionError("Expected a TypeError exception")
    except TypeError:
        pass  # This error was expected
