def normalize_price(price_str):
    if not price_str:
        return 0.0

    cleaned = (
        price_str
        .replace("Â", "")
        .replace("£", "")
        .replace("$", "")
        .strip()
    )

    try:
        return float(cleaned)
    except:
        return 0.0

def normalize_title(title):
    return title.lower().strip()
