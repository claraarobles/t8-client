
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
