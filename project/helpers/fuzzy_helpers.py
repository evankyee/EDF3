from fuzzywuzzy import fuzz

def fuzzy_match(keyword, keyword_bank):
    # Find the most similar word in the keyword bank to the given keyword
    return max(keyword_bank, key=lambda word: fuzz.ratio(keyword.lower(), word.lower()))