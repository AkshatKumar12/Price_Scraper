from difflib import SequenceMatcher

def is_similar(a, b, threshold=0.85):
    return SequenceMatcher(None, a, b).ratio() > threshold

def deduplicate(products):
    unique = []
    for product in products:
        if not any(is_similar(product["normalized_name"], u["normalized_name"]) for u in unique):
            unique.append(product)
    return unique
