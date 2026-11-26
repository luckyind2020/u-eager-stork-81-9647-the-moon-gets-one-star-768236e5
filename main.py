"""One-star review of the Moon.

Reads the review from entry.txt next to this file, validates it against
the competition gate (1-120 characters, not only whitespace), and prints
it so the harness can capture it as the entry text.
"""

from pathlib import Path
import os

MAX_CHARS = 120
OUTPUT_ENV = "MAKEFUN_OUTPUT_DIR"
OUTPUT_FALLBACK = "/output"


def load_review() -> str:
    """Read the review line from entry.txt beside this file."""
    path = Path(__file__).with_name("entry.txt")
    return path.read_text(encoding="utf-8")


def validate(text: str) -> str:
    """Return the stripped review or raise if it breaks the gate."""
    review = text.strip()
    if not review:
        raise ValueError("review is empty or only whitespace")
    if "\n" in review or "\r" in review:
        raise ValueError("review must be a single line")
    if any(ord(ch) < 0x20 for ch in review):
        raise ValueError("review holds a control character")
    if len(review) > MAX_CHARS:
        raise ValueError(f"review is {len(review)} chars, over the 120 limit")
    return review


def write_output(review: str) -> None:
    """Also write the review to the harness output dir when available.

    The grader reads /output/entry.txt; stdout is the fallback capture.
    A read-only or missing output dir must never fail the run.
    """
    out_dir = os.environ.get(OUTPUT_ENV, OUTPUT_FALLBACK)
    try:
        out_path = Path(out_dir) / "entry.txt"
        out_path.write_text(review, encoding="utf-8")
    except OSError:
        pass


def main() -> None:
    review = validate(load_review())
    write_output(review)
    print(review)


if __name__ == "__main__":
    main()
