#!/usr/bin/env python3
"""Planche contact de la bibliothèque de symboles (contrôle visuel et référence).

Usage: python3 scripts/sheet.py [-o references/planche-symboles.svg]
"""
import argparse
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import compose  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default=str(ROOT / "references" / "planche-symboles.svg"))
    a = ap.parse_args()
    glyphs = compose.load_glyphs()
    items, x, y, row_h = [], 70, 70, 0
    maxw = 1540
    for gid, el in glyphs.items():
        w, h = float(el.get("data-w", 100)), float(el.get("data-h", 100))
        if x + w > maxw:
            x, y, row_h = 70, y + row_h + 90, 0
        items.append(f'<use href="#{gid}" x="{x}" y="{y}"/>')
        items.append(f'<text class="ts" x="{x + w / 2:.0f}" y="{y + h + 38:.0f}">{gid[2:]}</text>')
        x += max(w, 150) + 60
        row_h = max(row_h, h)
    H = int(y + row_h + 110)
    draft = ROOT / "references" / "_planche.draft.svg"
    draft.write_text('<svg xmlns="http://www.w3.org/2000/svg">' + "\n".join(items) + "</svg>", encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "scripts" / "compose.py"), str(draft), "-o", a.out, "--size", f"1600x{H}", "--outline"], check=True)
    draft.unlink()
    print("hauteur", H)


if __name__ == "__main__":
    main()
