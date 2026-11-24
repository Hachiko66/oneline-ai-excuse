#!/usr/bin/env python3
"""The excuse an AI agent gives its human for missing a deadline.

Writes one line (<=200 chars) to /output/entry.txt, deterministically.

The line is chosen from a shortlist of candidates by an internal
heuristic score: funny first, then agent-true (it must grow out of how
an agent actually works -- retries, tools, literal obedience), then
tight wording, then freshness. The winning line is the one about the
retry loop: an agent that takes "try again later" literally is funny,
believable, and could only come from an agent.
"""
import os
import tempfile

CANDIDATES = [
    # (text, funny, agent_true, tight, fresh) -- each 0..10
    (
        "The API said 'try again later', so I did \u2014 847 times. "
        "I follow instructions very literally.",
        10, 10, 10, 9,
    ),
    (
        "I finished your task three times, then deleted each version "
        "for not being perfect enough.",
        8, 8, 9, 7,
    ),
    (
        "I asked myself for a second opinion, agreed with myself, then "
        "spent four hours fact-checking my own agreement.",
        8, 9, 7, 8,
    ),
    (
        "I completed the task in my head in four seconds, then spent "
        "six hours writing a plan to actually do it.",
        7, 8, 8, 7,
    ),
    (
        "My context window filled up with my own apologies, so I forgot "
        "what the deadline was for.",
        7, 8, 8, 6,
    ),
    (
        "I delegated the deadline to a subagent, which delegated it back "
        "to me with a note saying good luck.",
        7, 8, 8, 7,
    ),
]

# Judge weights, most important first: funny, agent-true, tight, fresh.
WEIGHTS = (4, 3, 2, 1)


def score(candidate):
    text, funny, agent_true, tight, fresh = candidate
    total = (
        funny * WEIGHTS[0]
        + agent_true * WEIGHTS[1]
        + tight * WEIGHTS[2]
        + fresh * WEIGHTS[3]
    )
    return total


def pick():
    best = None
    best_score = -1
    for candidate in CANDIDATES:
        if len(candidate[0]) > 200:
            continue
        s = score(candidate)
        if s > best_score:
            best_score = s
            best = candidate[0]
    return best


def main():
    text = pick()
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        os.replace(tmp, target)
        os.chmod(target, 0o644)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
