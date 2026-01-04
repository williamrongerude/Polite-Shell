# politeness.py

import re

POLITE_SCORES = {
    "pretty please with sugar on top": 5,
    "if it's not too much trouble": 4,
    "i was wondering if you could": 4,
    "i beg you to": 4,
    "as a humble request": 4,
    "i humbly request": 3,
    "would you be so kind": 3,
    "pretty please": 3,
    "humbly": 2,
    "kindly": 2,
    "please": 1,
    "could you": 1,
    "would you": 1,
    "can you": 1,
    "may you": 1,
    "might you": 1,
}
PHRASES = sorted(POLITE_SCORES, key=len, reverse=True)

REQUEST_PATTERNS = [
    re.compile(r"^(?:would|could|can)\s+you\b"),
    re.compile(r"^i\s+was\s+wondering\s+if\b"),
    re.compile(r"^would\s+it\s+be\s+possible\b"),
    re.compile(r"^at\s+your\s+convenience\b"),
]


def normalize(cmd: str) -> str:
    cmd = cmd.lower().replace("’", "'").strip()
    return re.sub(r"[\";:,\?\!]", "", cmd)


def detect_politeness(command: str) -> int:
    cmd = normalize(command)
    head = " ".join(cmd.split()[:10])
    score = 0

    for phrase in PHRASES:
        if phrase in head:
            score += POLITE_SCORES[phrase]
            head = head.replace(phrase, "")

    for patt in REQUEST_PATTERNS:
        if patt.search(head):
            score += 1

    return score


def classify_politeness(score: int) -> str:
    if score == 0:
        return "rude"
    if score <= 2:
        return "basic_politeness"
    if score <= 5:
        return "good_politeness"
    return "exceptional_politeness"
