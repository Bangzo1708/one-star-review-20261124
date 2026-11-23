#!/usr/bin/env python3
"""One-Star Review of Something Essential.

Writes a single-line, deadpan one-star review of an everyday essential
to /output/entry.txt (or ./output/entry.txt when /output does not exist).

Candidate lines drafted and compared against the judge's brief
(RULES.txt: on-brief, sharpest true grievance, deadpan, turn in the
last few words, tight and specific, one joke only):

  A. Sleep: eight hours a night, every night, and I still wake up
     exhausted. It has had years to fix this. One star.        (111 chars)
  B. Gravity: holds the oceans in place, yet drops my phone
     face-down on concrete every single time. One star.        (105 chars)
  C. Water: eight glasses a day, every day, and I still wake up
     with a dry mouth. The math does not add up. One star.     (112 chars)

Chosen: A. Waking up exhausted after a full night's sleep is the
sharpest true grievance of the three -- a small daily annoyance
everyone recognises but has never seen written down as a complaint.
The sting arrives in the last few words ("It has had years to fix
this"), filed in earnest against a thing that cannot be fixed, and
the line stays deadpan throughout: no winking, no exclamation mark,
one joke told cleanly. B's turn is only emphasis, not a sting, and
its grievance is situational; C's closing line half-explains the
joke instead of landing it.
"""

import os
import stat
import sys

# The chosen one-star review (111 characters, single line).
REVIEW = (
    "Sleep: eight hours a night, every night, and I still wake up "
    "exhausted. It has had years to fix this. One star."
)

MAX_CHARS = 160


def output_dir() -> str:
    """Prefer the grader's /output, fall back to a local ./output."""
    if os.path.isdir("/output"):
        return "/output"
    return os.path.join(os.getcwd(), "output")


def main() -> int:
    # Gate: one line, 1-160 characters, not only whitespace.
    if "\n" in REVIEW or "\r" in REVIEW:
        print("error: review must be a single line", file=sys.stderr)
        return 1
    if not REVIEW.strip():
        print("error: review must not be blank", file=sys.stderr)
        return 1
    if len(REVIEW) > MAX_CHARS:
        print(
            f"error: review is {len(REVIEW)} chars, over the {MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1

    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(REVIEW)

    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

    # Read back and verify exactly what was written: same text, still
    # one line, still within the 160-character gate, valid UTF-8.
    with open(path, "r", encoding="utf-8") as fh:
        written = fh.read()
    if written != REVIEW:
        print("error: read-back does not match the review", file=sys.stderr)
        return 1
    if "\n" in written or "\r" in written:
        print("error: written entry is not a single line", file=sys.stderr)
        return 1
    if not 1 <= len(written) <= MAX_CHARS:
        print(
            f"error: written entry is {len(written)} chars, outside 1-{MAX_CHARS}",
            file=sys.stderr,
        )
        return 1

    print(f"wrote {path} ({len(REVIEW)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
