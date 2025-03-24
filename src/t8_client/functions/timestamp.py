
from datetime import datetime, timezone


def utc_to_timestamp(utc_date: str) -> int:
    """
    Converts a date in UTC format (YYYY-MM-DDTHH:MM:SS) to a timestamp.

    Args:
        utc_date (str): Date in UTC format (YYYY-MM-DDTHH:MM:SS).

    Returns:
        int: Timestamp corresponding to the UTC date.
    """
    try:
        # Parse the UTC date from the string into a datetime object
        dt = datetime.strptime(utc_date, "%Y-%m-%dT%H:%M:%S")

        # Convert the datetime object to UTC and get the timestamp as an integer
        return int(dt.replace(tzinfo=timezone.utc).timestamp())

    except ValueError as e:
        # Handle date format errors and raise an exception with a clear message
        raise ValueError(
            f"Invalid date format: {utc_date}. It must be 'YYYY-MM-DDTHH:MM:SS'."
        ) from e
