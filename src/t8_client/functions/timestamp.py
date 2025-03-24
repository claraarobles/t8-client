
from datetime import datetime, timezone


def utc_to_timestamp(utc_date: str) -> int:
    """
    Convierte una fecha en formato UTC (YYYY-MM-DDTHH:MM:SS) a un timestamp.

    Args:
        utc_date (str): Fecha en formato UTC (YYYY-MM-DDTHH:MM:SS).

    Returns:
        int: Timestamp correspondiente a la fecha UTC.
    """
    try:
        # Parsear la fecha UTC
        dt = datetime.strptime(utc_date, "%Y-%m-%dT%H:%M:%S")
        return int(dt.replace(tzinfo=timezone.utc).timestamp())


    except ValueError as e:
        raise ValueError(
            f"Formato de fecha inválido: {utc_date}. Debe ser 'YYYY-MM-DDTHH:MM:SS'."
        ) from e
