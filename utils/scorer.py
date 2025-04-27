# utils/scorer.py

def score_entry(entry):
    score = 0

    if "Persistence Key" in entry.flags:
        score += 5
    if "Suspicious Folder" in entry.flags:
        score += 2
    if "Executable File" in entry.flags:
        score += 2
    if "Incomplete Path" in entry.flags:
        score -= 2

    entry.score = max(0, min(10, score))  # Clamp score between 0 and 10
    return entry
