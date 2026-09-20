#!/usr/bin/env python3
"""Export one note per explicit Beamer frame; reject missing or mismatched notes."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "slides/talk.tex").read_text()
frames = re.findall(r"\\begin\{frame\}(.*?)\\end\{frame\}", source, re.S)
output = ["# Speaker notes", "",
          "One factory path: freeze, execute, judge, gate.",
          "The finding is a protected checker that still reads worker-controlled expected results.",
          "Three surrounding grants are independent synthetic checks, not one exploit chain.",
          "Workers are deterministic scripts. No model-driven exploitation claim.", ""]
for number, frame in enumerate(frames, 1):
    notes = re.findall(r"\\note\{([^{}]*)\}", frame, re.S)
    if len(notes) != 1:
        raise SystemExit(f"Slide {number}: require exactly one plain-text note.")
    output += [f"## Slide {number}", "", notes[0].strip(), ""]
(ROOT / "SPEAKER_NOTES.md").write_text("\n".join(output))
print(f"Exported {len(frames)} slide notes")
