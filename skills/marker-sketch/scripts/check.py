#!/usr/bin/env python3
"""Contrôle rapide d'un dessin brut (ou d'un SVG composé) avant livraison.

Usage:
    python3 check.py draft.svg            # règles générales
    python3 check.py draft.svg --live     # budget serré pour réunion (<= 7 objets, texte lisible)

Retourne 0 s'il n'y a pas d'erreur bloquante, 1 sinon. Les avertissements ne bloquent pas.
Contrôle: SVG bien formé, symboles connus, classes connues, une seule couleur d'accent,
textes courts, tirets longs interdits, apostrophes droites, textes hors cadre, budget d'objets.
"""
import argparse
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
NS = "{http://www.w3.org/2000/svg}"
KNOWN = set("""paper ink fine mid inkg inkb flow dotk dash arr arrb arrg arr2 sh pp hl fx f1 f2 f3 f4 fh fb fo fr fs
cb co cr cs ch c1 c3 c4 t tl ts tb tg tw l r drag""".split())
ACCENT = {"cb": "bleu", "co": "orange", "cr": "rouge", "cs": "sable", "ch": "surligneur",
          "fb": "bleu", "fo": "orange", "fr": "rouge", "fs": "sable", "fh": "surligneur", "inkb": "bleu", "tb": "bleu"}
PALETTE = {"#161616", "#2547a8", "#80838a", "#8e9198", "#b3b6bc", "#c6c9ce", "#d6d8dc", "#a4a7ad", "#6f737d",
           "#1c1c1e", "#f3f2ee", "none", "#7d8088"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--live", action="store_true")
    a = ap.parse_args()
    raw = pathlib.Path(a.src).read_text(encoding="utf-8")
    errs, warns = [], []
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        print(f"ERREUR: SVG mal formé ({e}). Souvent un & non échappé (&amp;) ou une balise non fermée.")
        sys.exit(1)

    glyph_ids = set(re.findall(r'<g id="(g-[a-z0-9-]+)"', (ROOT / "assets" / "glyphes.svg").read_text(encoding="utf-8")))
    vb = (root.get("viewBox") or "0 0 1600 900").split()
    W, H = float(vb[2]), float(vb[3])

    uses = re.findall(r'href="#(g-[a-z0-9-]+)"', raw)
    for g in sorted(set(uses)):
        if g not in glyph_ids:
            errs.append(f"symbole inconnu {g} (voir compose.py --catalog)")

    classes = set()
    for el in root.iter():
        classes.update((el.get("class") or "").split())
    unknown = sorted(c for c in classes if c not in KNOWN)
    if unknown:
        warns.append("classes hors noyau: " + ", ".join(unknown))

    # le bleu d'annotation (inkb, tb) ne compte pas comme accent de remplissage
    fills = {ACCENT[c] for c in classes if c in ACCENT and c not in ("inkb", "tb")}
    if len(fills) > 1:
        warns.append("plusieurs couleurs d'accent de remplissage (" + ", ".join(sorted(fills)) + "): en garder une")

    for el in root.iter():
        for attr in ("fill", "stroke"):
            v = (el.get(attr) or "").lower()
            if v.startswith("#") and v not in PALETTE:
                warns.append(f"couleur {v} hors palette ({attr})")
                break

    texts = [t for t in root.iter(NS + "text")]
    long = []
    for t in texts:
        s = "".join(t.itertext()).strip()
        if len(s) > (22 if a.live else 34):
            long.append(s)
        if "\u2014" in s or "\u2013" in s:
            errs.append(f"tiret long interdit dans « {s} »")
        if "'" in s:
            warns.append(f"apostrophe droite dans « {s} » (utiliser ’)")
        try:
            x, y = float(t.get("x", 0)), float(t.get("y", 0))
            if x == 0 and y == 0:
                continue  # position donnée par la config interactive
            if x < 20 or x > W - 20 or y < 20 or y > H - 10:
                warns.append(f"texte près du bord ou hors cadre: « {s} »")
        except ValueError:
            pass
    if long:
        warns.append(f"{len(long)} texte(s) trop long(s) (1 à 4 mots, sinon une phrase de légende): « {long[0]} »")
    if a.live:
        small = [t for t in texts if "ts" in (t.get("class") or "").split()]
        if small:
            warns.append("mode live: éviter la classe .ts (texte petit), illisible en projection")

    budget = 7 if a.live else 14
    if len(uses) + len(texts) // 3 > budget:
        warns.append(f"beaucoup d'objets ({len(uses)} symboles, {len(texts)} textes): budget conseillé {budget}")
    if len(texts) > (9 if a.live else 18):
        warns.append(f"{len(texts)} textes: simplifier")

    for w in warns:
        print("avertissement:", w)
    for e in errs:
        print("ERREUR:", e)
    if not warns and not errs:
        print("ok")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
