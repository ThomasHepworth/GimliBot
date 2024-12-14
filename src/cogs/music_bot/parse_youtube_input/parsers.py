from datetime import datetime


def parse_duration(duration: int) -> str:
    """
    Parse a duration given in seconds into a human-readable format
    of hours, minutes, and seconds.
    """
    if duration < 0:
        raise ValueError("Duration must be a non-negative integer.")

    # Accepted units to convert input seconds into.
    units = [("hour", 3600), ("minute", 60), ("second", 1)]
    output = []

    for unit_name, unit_value in units:
        value, duration = divmod(duration, unit_value)
        if value or output:
            unit_label = unit_name if value == 1 else f"{unit_name}s"
            output.append(f"{value} {unit_label}")

    return ", ".join(output) if output else "0 seconds"


def parse_date(date_str: str) -> str:
    """
    Parse a date string in the format of YYYYMMDD into a human-readable format.
    """
    try:
        date = datetime.strptime(date_str, "%Y%m%d")
    except ValueError:
        return "Unknown"

    return date.strftime("%B %d, %Y")


def readable_view_count(view_count: int) -> str:
    """
    Convert an integer view count into a human-readable format with suffixes.

    Examples:
        0 -> "0 views"
        23 -> "23 views"
        2_300 -> "2.3k views"
        23_000 -> "23k views"
        1_000_000 -> "1M views"
        1_000_000_000 -> "1B views"
    """
    if view_count < 0:
        raise ValueError("View count must be a non-negative integer.")

    count_mappings = [
        (1_000_000_000, "B"),  # Billions
        (1_000_000, "M"),  # Millions
        (1_000, "k"),  # Thousands
        (1, ""),  # Less than 1,000
    ]

    for count, suffix in count_mappings:
        if view_count >= count:
            value = view_count / count
            formatted_value = f"{value:.1f}".rstrip("0").rstrip(".")
            plural_suffix = "views" if view_count != 1 else "view"
            return f"{formatted_value}{suffix} {plural_suffix}"

    return "0 views"
