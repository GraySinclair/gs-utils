from datetime import date

# TODO: Add optional iso toggle  

def month_to_gte_lt(month: str) -> tuple[str, str]:
    """
    '2023-01' -> ('2023-01-01', '2023-02-01')
    """
    year, m = map(int, month.split("-"))
    start = date(year, m, 1)

    if m == 12:
        end = date(year + 1, 1, 1)
    else:
        end = date(year, m + 1, 1)

    # plain YYYY-MM-DD strings
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")
    
