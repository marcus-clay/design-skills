#!/usr/bin/env python3
"""Assemble un croquis marker-sketch complet à partir d'un dessin brut.

Le dessin brut ne contient que le contenu (formes, textes, <use href="#g-..."/>).
Ce script ajoute le noyau de style (filtres, classes, flèches), le papier, les points,
injecte les symboles de la bibliothèque référencés, et peut convertir le texte en tracés.

Usage:
    python3 compose.py brut.svg -o croquis.svg
    python3 compose.py brut.svg -o croquis.svg --paper kraft --outline
    python3 compose.py --catalog                       # liste les symboles disponibles
    python3 compose.py brut.svg -o c.svg --transparent # sans papier ni points (pour slides)

Options:
    --paper cream|white|kraft|yellow|blue   teinte du papier (défaut: cream)
    --no-dots                               supprime les points
    --transparent                           fond transparent (ni papier ni points)
    --outline                               convertit les <text> en tracés (rendu identique partout)
    --embed-font                            incorpore la police en base64 (si pas --outline)
    --interactive scenes.json               produit une page HTML interactive (états, déplacements, liens)
                                            à partir du dessin brut + de la config JSON (voir references/interactif.md)
"""
import argparse
import base64
import copy
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")

PAPERS = {
    "cream": ("#f3f2ee", "#b8b8b2"),
    "white": ("#fbfbfa", "#c4c4bf"),
    "kraft": ("#e7dcc6", "#a79c86"),
    "yellow": ("#e4e98a", "#5f8a2c"),
    "blue": ("#dfe9ee", "#9fb0ba"),
}

TEXT_SIZES = {"t": 36, "tl": 52, "ts": 27, "tb": 32, "tg": 32, "tw": 36}
TEXT_FILL = {"t": "#161616", "tl": "#161616", "ts": "#161616", "tb": "#2547a8", "tg": "#7d8088", "tw": "#f3f2ee"}


# --------------------------------------------------------------------------- glyphes
def load_glyphs():
    path = ASSETS / "glyphes.svg"
    if not path.exists():
        return {}
    tree = ET.parse(path)
    out = {}
    for el in tree.getroot().iter(f"{{{SVG_NS}}}g"):
        gid = el.get("id")
        if gid and gid.startswith("g-"):
            out[gid] = el
    return out


def serialize(el):
    s = ET.tostring(el, encoding="unicode")
    return s.replace(f' xmlns="{SVG_NS}"', "").replace(f"{{{SVG_NS}}}", "")


def needed_glyphs(text, glyphs):
    found, queue = [], re.findall(r'href="#(g-[a-z0-9-]+)"', text)
    while queue:
        gid = queue.pop(0)
        if gid in found:
            continue
        if gid not in glyphs:
            sys.exit(f"Symbole inconnu: {gid}. Lancer compose.py --catalog pour la liste.")
        found.append(gid)
        queue += re.findall(r'href="#(g-[a-z0-9-]+)"', serialize(glyphs[gid]))
    return found


def print_catalog(glyphs):
    for gid, el in glyphs.items():
        print(f'{gid:22s} {el.get("data-w", "?"):>4}x{el.get("data-h", "?"):<4} {el.get("data-desc", "")}')


# --------------------------------------------------------------------------- texte -> tracés
_font_cache = {}


def get_font():
    if "f" not in _font_cache:
        try:
            from fontTools.ttLib import TTFont
        except ImportError:
            return None
        _font_cache["f"] = TTFont(str(ASSETS / "fonts" / "patrick-hand-400.woff"))
    return _font_cache["f"]


def text_to_path(chars, x, y, size, anchor, font):
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen

    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    hmtx = font["hmtx"]
    upm = font["head"].unitsPerEm
    k = size / upm
    width = sum(hmtx[cmap.get(ord(c), ".notdef")][0] for c in chars) * k
    x0 = x - (width / 2 if anchor == "middle" else width if anchor == "end" else 0)
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}")
    cur = x0
    for c in chars:
        name = cmap.get(ord(c))
        if name is None:
            name = ".notdef"
        if c != " ":
            gs[name].draw(TransformPen(pen, (k, 0, 0, -k, cur, y)))
        cur += hmtx[name][0] * k
    return pen.getCommands()


def classes_of(el):
    return (el.get("class") or "").split()


def outline_texts(root):
    font = get_font()
    if font is None:
        print("fontTools absent: texte conservé en <text> avec la police incorporée (pip install fonttools pour des tracés)", file=sys.stderr)
        return False
    for parent in list(root.iter()):
        for i, child in enumerate(list(parent)):
            if child.tag != f"{{{SVG_NS}}}text":
                continue
            cls = classes_of(child)
            base = next((c for c in cls if c in TEXT_SIZES), "t")
            size = float(child.get("font-size") or TEXT_SIZES[base])
            fill = child.get("fill") or TEXT_FILL[base]
            anchor = "start" if "l" in cls else "end" if "r" in cls else child.get("text-anchor", "middle")
            x = float(child.get("x", 0))
            y = float(child.get("y", 0))
            lines = []
            tspans = [t for t in child if t.tag == f"{{{SVG_NS}}}tspan"]
            if tspans:
                if (child.text or "").strip():
                    lines.append((x, y, child.text.strip()))
                cx, cy = x, y
                for t in tspans:
                    if t.get("x") is not None:
                        cx = float(t.get("x"))
                    if t.get("y") is not None:
                        cy = float(t.get("y"))
                    cy += float(t.get("dy", 0))
                    lines.append((cx, cy, (t.text or "").strip()))
            else:
                lines.append((x, y, (child.text or "").strip()))
            g = ET.Element(f"{{{SVG_NS}}}g")
            for attr in ("transform", "opacity"):
                if child.get(attr):
                    g.set(attr, child.get(attr))
            for lx, ly, s in lines:
                if not s:
                    continue
                d = text_to_path(s, lx, ly, size, anchor, font)
                p = ET.SubElement(g, f"{{{SVG_NS}}}path")
                p.set("d", d)
                p.set("fill", fill)
                p.set("stroke", fill)
                p.set("stroke-width", "0.7")
                p.set("stroke-linejoin", "round")
            parent[i] = g
    return True


# --------------------------------------------------------------------------- assemblage
def inner_content(text):
    m = re.search(r"<svg\b[^>]*>(.*)</svg>\s*$", text, re.S)
    return m.group(1) if m else text


def build_interactive(a, full, bg, need):
    import json
    cfg_path = pathlib.Path(a.interactive)
    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"Config JSON invalide ({cfg_path}): {e}")
    try:
        ET.fromstring(full)
    except ET.ParseError as e:
        sys.exit(f"SVG mal formé: {e}. Corriger le dessin brut (balises non fermées, & non échappé).")
    # le svg devient fluide (taille gérée par la page) et reçoit l'id attendu par le moteur
    full = re.sub(r"<svg\b([^>]*)>", lambda m: "<svg id=\"sketch\" preserveAspectRatio=\"xMidYMid meet\"" + re.sub(r'\s(width|height)="[^"]*"', "", m.group(1)) + ">", full, count=1)
    full = re.sub(r"<\?xml[^>]*\?>\s*", "", full)
    # vérifie que les éléments animés existent
    ids = set(re.findall(r'\bid="([^"]+)"', full))
    for k in (cfg.get("elements") or {}):
        if k not in ids:
            print(f"Attention: l'élément « {k} » est dans la config mais absent du dessin.", file=sys.stderr)
    for m in re.finditer(r'data-link="([^"]+)"', full):
        for part in m.group(1).split(">"):
            if part.strip() not in ids:
                print(f"Attention: lien vers « {part.strip()} » introuvable.", file=sys.stderr)
    page = (ASSETS / "interactive.html").read_text(encoding="utf-8")
    b64 = base64.b64encode((ASSETS / "fonts" / "patrick-hand-400.woff").read_bytes()).decode()
    font = "@font-face{font-family:'Patrick Hand';src:url(data:font/woff;base64," + b64 + ") format('woff')}"
    runtime = (ASSETS / "runtime.js").read_text(encoding="utf-8")
    title = a.title or cfg.get("title") or "Croquis interactif"
    page = (page.replace("__TITLE__", title.replace("<", "&lt;"))
                .replace("__PAPER__", bg)
                .replace("/*__FONT__*/", font)
                .replace("__SVG__", full)
                .replace("__SCENES__", json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/"))
                .replace("/*__RUNTIME__*/", runtime))
    dest = pathlib.Path(a.out) if a.out else pathlib.Path(a.src).with_suffix(".html")
    dest.write_text(page, encoding="utf-8")
    print(dest, f"({len(page) // 1024} ko, {len(need)} symboles)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", nargs="?")
    ap.add_argument("-o", "--out")
    ap.add_argument("--paper", default="cream", choices=PAPERS.keys())
    ap.add_argument("--no-dots", action="store_true")
    ap.add_argument("--transparent", action="store_true")
    ap.add_argument("--outline", action="store_true")
    ap.add_argument("--embed-font", action="store_true")
    ap.add_argument("--size", default="1600x900", help="taille du canevas, ex. 1600x1200")
    ap.add_argument("--title")
    ap.add_argument("--catalog", action="store_true")
    ap.add_argument("--interactive", metavar="SCENES_JSON", help="config JSON du mode interactif -> sortie HTML")
    a = ap.parse_args()

    glyphs = load_glyphs()
    if a.catalog:
        print_catalog(glyphs)
        return
    if not a.src:
        ap.error("fichier source requis")

    raw = pathlib.Path(a.src).read_text(encoding="utf-8")
    template = (ASSETS / "template.svg").read_text(encoding="utf-8")

    if 'id="drawing"' in raw:
        full = raw  # déjà complet: seulement post-traitement
        body = None
    else:
        body = inner_content(raw)
        full = template.replace("<!-- DESSIN ICI -->", body)

    # injection des symboles
    need = needed_glyphs(full, glyphs)
    inject = "".join("\n" + serialize(glyphs[g]) for g in need)
    if inject and "id=\"g-" not in full.split("</defs>")[0]:
        full = full.replace("</defs>", inject + "\n</defs>", 1)

    # taille du canevas
    W, H = (int(v) for v in a.size.lower().split("x"))
    if (W, H) != (1600, 900):
        full = full.replace('viewBox="0 0 1600 900" width="1600" height="900"', f'viewBox="0 0 {W} {H}" width="{W}" height="{H}"')
        full = full.replace('width="1600" height="900"', f'width="{W}" height="{H}"')
        full = full.replace('width="1720" height="980"', f'width="{W + 120}" height="{H + 80}"')

    # papier
    bg, dots = PAPERS[a.paper]
    full = full.replace("#f3f2ee", bg).replace('fill="#b8b8b2"', f'fill="{dots}"')
    if a.transparent:
        full = re.sub(r'<rect class="paper"[^>]*/>\s*', "", full)
        full = re.sub(r'<rect width="1600" height="900" fill="url\(#dots\)"/>\s*', "", full)
    elif a.no_dots:
        full = re.sub(r'<rect width="1600" height="900" fill="url\(#dots\)"/>\s*', "", full)
    if a.title:
        full = re.sub(r"<title>.*?</title>", f"<title>{a.title}</title>", full, count=1)

    if a.interactive:
        return build_interactive(a, full, bg, need)

    # texte
    try:
        root = ET.fromstring(full)
    except ET.ParseError as e:
        sys.exit(f"SVG mal formé: {e}. Corriger le dessin brut (balises non fermées, & non échappé).")
    embed = a.embed_font
    if a.outline:
        if not outline_texts(root):
            embed = True  # fontTools absent: on incorpore la police pour garder le rendu manuscrit
    if embed:
        b64 = base64.b64encode((ASSETS / "fonts" / "patrick-hand-400.woff").read_bytes()).decode()
        style = root.find(f".//{{{SVG_NS}}}style")
        style.text = (
            "@font-face{font-family:'Patrick Hand';src:url(data:font/woff;base64," + b64 + ") format('woff')}\n"
            + style.text
        )
    out = ET.tostring(root, encoding="unicode")
    out = '<?xml version="1.0" encoding="UTF-8"?>\n' + out.replace(f"{{{SVG_NS}}}", "")
    dest = pathlib.Path(a.out) if a.out else pathlib.Path(a.src).with_name(pathlib.Path(a.src).stem + ".full.svg")
    dest.write_text(out, encoding="utf-8")
    print(dest, f"({len(out) // 1024} ko, {len(need)} symboles)")


if __name__ == "__main__":
    main()
