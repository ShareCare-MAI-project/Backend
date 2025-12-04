from datetime import datetime


def datetime_to_str_date(date: datetime) -> str:
    date = date.date()
    return f"{date.day}.{date.month}.{date.year}"
