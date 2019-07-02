from datetime import datetime, timezone

def parse_rfc3339(ts: str) -> (datetime, bool):
    """
    Parses RFC3339 dates, with or without milliseconds.  Raises ValueError if
    the date is improperly formatted.
    """
    try:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        pass

    try:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
    except ValueError:
        raise
