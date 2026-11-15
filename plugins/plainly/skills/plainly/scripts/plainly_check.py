"""Plainly checker: flag long sentences, passive voice, long paragraphs and wordy phrases.

Reads plain text or Markdown from a file or stdin. Standard library only.

    uv run plainly_check.py FILE        # or: python plainly_check.py FILE
    cat FILE | uv run plainly_check.py -
    uv run plainly_check.py FILE --strict   # also flag contractions and complex verb forms
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

WORDS_FILE = Path(__file__).resolve().parent.parent / "references" / "words.md"
STEP_MAX = 20
TEXT_MAX = 25
PARAGRAPH_MAX = 6

WORD = re.compile(r"[A-Za-z0-9][\w'’-]*")
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"(\[*])")
NUMBERED = re.compile(r"^\s*\d+[.)]\s+")
BULLET = re.compile(r"^\s*[-*+]\s+")
QUOTED = re.compile(r"\"[^\"]*\"|“[^”]*”")
PARENS = re.compile(r"\([^()]*\)")
IRREGULAR = "built|done|driven|given|held|kept|known|left|lost|made|paid|put|read|run|seen|sent|set|shown|taken|thrown|told|written"
PASSIVE = re.compile(
    rf"\b(?:am|is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?(\w{{2,}}ed|{IRREGULAR})\b", re.I
)
NOT_VERBS = "something|nothing|anything|everything|during|string|morning|evening|thing|interesting"
COMPLEX_VERB = re.compile(
    rf"\b(?:has|have|had)\s+been\b"
    rf"|\b(?:has|have|had)\s+(?:\w+ly\s+)?(?:\w{{2,}}ed|{IRREGULAR})\b"
    rf"|\b(?:am|is|are|was|were|be)\s+(?!(?:{NOT_VERBS})\b)\w{{2,}}ing\b",
    re.I,
)
CONTRACTION = re.compile(r"\b\w+n[’']t\b|\b\w+[’'](?:re|ll|ve|d)\b|\b(?:it|that|there|what|here|who)[’']s\b", re.I)


@dataclass
class Block:
    """A paragraph or list item, with its first line number."""

    line: int
    text: str
    is_step: bool


@dataclass
class Finding:
    line: int
    kind: str
    message: str


def load_swaps(path: Path = WORDS_FILE) -> dict[str, str]:
    """Read `| avoid | use instead |` rows from the word list."""
    swaps = {}
    for row in path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) == 2 and cells[0] not in ("avoid", "") and not cells[0].startswith("-"):
            swaps[cells[0].lower()] = cells[1]
    return swaps


def to_blocks(text: str) -> list[Block]:
    """Split Markdown into paragraphs and list items. Skip frontmatter, code, headings and tables."""
    blocks, current, in_code = [], None, False
    lines = text.splitlines()
    skip_until = lines.index("---", 1) + 1 if lines[:1] == ["---"] and "---" in lines[1:] else 0
    for number, raw in enumerate(lines, start=1):
        if number <= skip_until:
            continue
        line = raw.strip()
        if line.startswith("```"):
            in_code, current = not in_code, None
            continue
        if in_code or not line or line.startswith(("#", "|")):
            current = None
            continue
        line = re.sub(r"`[^`]*`", "X", line.lstrip("> ").strip())
        is_item = bool(NUMBERED.match(line) or BULLET.match(line))
        if is_item or current is None:
            content = NUMBERED.sub("", BULLET.sub("", line))
            current = Block(number, content, bool(NUMBERED.match(line)))
            blocks.append(current)
        else:
            current.text += " " + line
    return blocks


def sentences(text: str) -> list[str]:
    return [s for s in SENTENCE_END.split(text) if WORD.search(s)]


def word_count(sentence: str) -> int:
    """Count words. Quoted text and text in parentheses count as one word each."""
    return len(WORD.findall(PARENS.sub(" X ", QUOTED.sub(" X ", sentence))))


def preview(sentence: str, words: int = 8) -> str:
    parts = sentence.split()
    return " ".join(parts[:words]) + (" ..." if len(parts) > words else "")


def check_sentence(sentence: str, limit: int, strict: bool) -> list[tuple[str, str]]:
    """Return (kind, message) pairs for one sentence."""
    found = []
    count = word_count(sentence)
    if count > limit:
        found.append(("long-sentence", f'{count} words (max {limit}): "{preview(sentence)}"'))
    for match in PASSIVE.finditer(sentence):
        found.append(("passive", f'"{match.group(0)}" - say who does it'))
    if ";" in sentence:
        found.append(("semicolon", f'write two sentences: "{preview(sentence)}"'))
    if strict:
        for match in COMPLEX_VERB.finditer(sentence):
            found.append(("verb-form", f'"{match.group(0)}" - use a simple verb form'))
        for match in CONTRACTION.finditer(sentence):
            found.append(("contraction", f'"{match.group(0)}" - write it in full'))
    return found


def check(text: str, swaps: dict[str, str], strict: bool = False) -> list[Finding]:
    """Return all findings for a text."""
    findings = []
    for block in to_blocks(text):
        limit = STEP_MAX if block.is_step else TEXT_MAX
        found = sentences(block.text)
        for sentence in found:
            for kind, message in check_sentence(sentence, limit, strict):
                findings.append(Finding(block.line, kind, message))
        if len(found) > PARAGRAPH_MAX:
            findings.append(Finding(block.line, "long-paragraph", f"{len(found)} sentences (max {PARAGRAPH_MAX})"))
        lowered = QUOTED.sub(" ", block.text.lower())
        for avoid, use in swaps.items():
            if re.search(rf"(?<!\w){re.escape(avoid)}(?:s|d|ed|es|ing)?(?!\w)", lowered):
                findings.append(Finding(block.line, "word", f'"{avoid}" -> {use}'))
    return findings


def summary(text: str, findings: list[Finding]) -> str:
    counts = [word_count(s) for b in to_blocks(text) for s in sentences(b.text)]
    average = sum(counts) / len(counts) if counts else 0
    return f"{len(findings)} findings | {len(counts)} sentences | average {average:.1f} words per sentence"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("file", help="text or Markdown file, or - for stdin")
    parser.add_argument("--strict", action="store_true", help="also flag contractions and complex verb forms")
    parser.add_argument("--fail", action="store_true", help="exit 1 when there are findings (for CI)")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    text = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
    text = text.lstrip("﻿")
    findings = check(text, load_swaps(), args.strict)
    for f in findings:
        print(f"L{f.line:<4} {f.kind:<15} {f.message}")
    print(summary(text, findings))
    return 1 if args.fail and findings else 0


if __name__ == "__main__":
    sys.exit(main())
