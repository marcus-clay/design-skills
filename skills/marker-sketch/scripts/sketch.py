#!/usr/bin/env python3
"""Constructeur de croquis (mode Atelier): décrire un schéma en quelques lignes, obtenir le dessin brut.

Les liens se calculent tout seuls (bords des objets, courbe en S, flèche ouverte), les objets reçoivent
les quatre couches du style (ombre, papier, aplat décalé, contour irrégulier). Ensuite compose.py ajoute le
papier et les filtres.

    import sys; sys.path.insert(0, "scripts")
    from sketch import Sketch
    s = Sketch()
    a = s.box("a", 220, 330, "Idée", fill="f1")          # (id, centre x, centre y, texte)
    b = s.box("b", 720, 330, "Prototype")
    c = s.glyph("c", "g-person", 1220, 330, "Utilisateur")
    s.link("a", "b", label="tester")
    s.link("b", "c", kind="flow")
    s.perimeter(["a", "b"], "équipe")
    s.note(900, 140, "le goulot", target="b")
    s.save("draft.svg")                                    # puis: python3 scripts/compose.py draft.svg -o croquis.svg

Types de liens: ink (noir, flèche), gray (gris, flèche), flow (gris pointillé large), dash (tirets noirs),
blue (annotation), line (trait nu). Remplissages: f1 f2 f3 f4 fh fb fo fr fs (un seul accent par dessin).
"""
import html
import math
import pathlib
import random
import re
import sys
import zlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_glyphs import Pen, num  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GLYPH_SIZE = {m.group(1): (float(m.group(2)), float(m.group(3)))
              for m in re.finditer(r'<g id="(g-[a-z0-9-]+)" data-w="(\d+)" data-h="(\d+)"',
                                   (ROOT / "assets" / "glyphes.svg").read_text(encoding="utf-8"))}
LINK = {
    "ink": ('ink arr', None), "gray": ('inkg arrg', None), "flow": ('flow', None),
    "dash": ('dash arr', None), "blue": ('inkb arrb', None), "line": ('ink', None),
}
DARK_FILLS = {"f4", "f3"}


def esc(s):
    return html.escape(str(s), quote=False)


class Node:
    def __init__(self, id, cx, cy, hw, hh):
        self.id, self.cx, self.cy, self.hw, self.hh = id, cx, cy, hw, hh


class Sketch:
    def __init__(self, w=1600, h=900, seed="croquis"):
        self.w, self.h, self.seed = w, h, seed
        self.nodes = {}
        self.under, self.body, self.over = [], [], []
        self.n = 0

    # ------------------------------------------------------------------ outils
    def pen(self, key):
        self.n += 1
        return Pen(f"{self.seed}-{key}-{self.n}")

    def _lines(self, label):
        return [l for l in str(label).split("\n")] if label else []

    def _text(self, x, y, label, cls="t", size=36, anchor=None):
        lines = self._lines(label)
        if not lines:
            return ""
        if anchor:
            cls += f" {anchor}"
        y0 = y - (len(lines) - 1) * size * 0.55 + size * 0.34
        if len(lines) == 1:
            return f'<text class="{cls}" x="{num(x)}" y="{num(y0)}">{esc(lines[0])}</text>'
        spans = "".join(f'<tspan x="{num(x)}" y="{num(y0 + i * size * 1.1)}">{esc(l)}</tspan>' for i, l in enumerate(lines))
        return f'<text class="{cls}">{spans}</text>'

    def _object(self, i, d, fill, shadow=True, paper=True):
        s = ""
        if shadow:
            s += f'<use href="#{i}" x="-7" y="10" class="sh"/>'
        if paper:
            s += f'<use href="#{i}" class="pp"/>'
        if fill:
            s += f'<use href="#{i}" x="-2.5" y="2.5" class="{fill}"/>'
        s += f'<g class="ink"><path id="{i}" d="{d}"/></g>'
        return s

    # ------------------------------------------------------------------ objets
    def box(self, id, cx, cy, label="", w=None, h=None, fill=None, shape="box", size=36, solid=True):
        """Boîte (shape='box'), pastille arrondie ('pill') ou ovale ('oval'). Centre (cx, cy).
        solid=False: sans ombre ni papier (formes qui se chevauchent: Venn, zones)."""
        lines = self._lines(label)
        longest = max((len(l) for l in lines), default=3)
        w = w or max(200, longest * size * 0.46 + 70)
        h = h or max(112, len(lines) * size * 1.15 + 56)
        p = self.pen(id)
        x, y = cx - w / 2, cy - h / 2
        if shape == "oval":
            d = p.ellipse(cx, cy, w / 2, h / 2)
        elif shape == "pill":
            d = p.rbox(x, y, w, h, rad=min(h / 2.2, 40))
        else:
            d = p.box(x, y, w, h)
        i = f"s{id}"
        tcls = "tw" if fill in DARK_FILLS else "t"
        self.body.append(f'<g id="{id}">' + self._object(i, d, fill, solid, solid) + self._text(cx, cy, label, tcls, size) + "</g>")
        self.nodes[id] = Node(id, cx, cy, w / 2, h / 2)
        return id

    def glyph(self, id, name, cx, cy, label="", scale=1.0, cls="", label_gap=44):
        """Symbole de la bibliothèque (compose.py --catalog), centré en (cx, cy)."""
        if name not in GLYPH_SIZE:
            sys.exit(f"Symbole inconnu: {name}")
        gw, gh = GLYPH_SIZE[name]
        w, h = gw * scale, gh * scale
        use = f'<use href="#{name}"' + (f' class="{cls}"' if cls else "") + "/>"
        tr = f'translate({num(cx - w / 2)} {num(cy - h / 2)})' + (f" scale({scale:g})" if scale != 1 else "")
        out = f'<g id="{id}"><g transform="{tr}">{use}</g>'
        if label:
            out += self._text(cx, cy + h / 2 + label_gap, label)
        out += "</g>"
        self.body.append(out)
        self.nodes[id] = Node(id, cx, cy, w / 2, h / 2)
        return id

    def text(self, x, y, label, cls="t", anchor=None, size=None):
        base = {"t": 36, "tl": 52, "ts": 27, "tb": 32, "tg": 32}.get(cls, 36)
        self.body.append(self._text(x, y, label, cls, size or base, anchor))

    def label(self, id, dy=-70, label="", cls="tl"):
        """Titre posé au-dessus (dy<0) ou au-dessous (dy>0) d'un objet existant."""
        n = self.nodes[id]
        self.text(n.cx, n.cy + (-n.hh + dy if dy < 0 else n.hh + dy), label, cls)

    # ------------------------------------------------------------------ maquettes (wireframes)
    def wf(self, id, kind, x, y, w, h, label="", fill=None):
        """Élément de maquette, coin haut gauche (x, y). kind: frame, image, text, title, button, input, nav,
        avatar, card. Les écrans se relient ensuite avec link(). Texte: 'label' (bouton, champ, titre d'écran)."""
        p = self.pen(id)
        i = f"s{id}"
        cx, cy = x + w / 2, y + h / 2
        out = ""
        if kind == "frame":
            out = self._object(i, p.box(x, y, w, h, j=2.5, o=7), fill)
            if label:
                out += self._text(cx, y - 34, label, "t", 32)
        elif kind == "image":
            out = self._object(i, p.box(x, y, w, h, j=2, o=4), fill or "f1", shadow=False)
            out += f'<path class="fine" d="{p.line(x, y, x + w, y + h, 3)} {p.line(x + w, y, x, y + h, 3)}"/>'
        elif kind == "text":
            n = max(1, int(h // 26))
            out = f'<path class="fine" d="{p.lines(x, y + 10, w, n, 26)}"/>'
        elif kind == "title":
            out = f'<path class="ink" d="{p.line(x, cy, x + w, cy + p.j(2), 3)}"/>'
            if label:
                out = self._text(x, cy, label, "t", 34, "l")
        elif kind == "button":
            f = fill if fill is not None else "f4"
            out = self._object(i, p.rbox(x, y, w, h, rad=h / 2.2), f, shadow=True)
            out += self._text(cx, cy, label, "tw" if f in DARK_FILLS else "t", 30)
        elif kind == "input":
            out = self._object(i, p.rbox(x, y, w, h, rad=12), fill, shadow=False)
            if label:
                out += self._text(x + 22, cy, label, "tg", 28, "l")
        elif kind == "nav":
            out = self._object(i, p.box(x, y, w, h, j=1.5, o=4), fill or "f2", shadow=False)
            for k in range(3):
                out += f'<path class="ink" d="M{num(x + 30 + k * 34)} {num(cy)} l.1 .1"/>'
        elif kind == "avatar":
            out = self._object(i, p.ellipse(cx, cy, w / 2, h / 2), fill or "f1", shadow=False)
        elif kind == "card":
            out = self._object(i, p.box(x, y, w, h, j=2, o=5), fill)
            out += f'<path class="fine" d="{p.lines(x + 24, y + 30, w - 60, max(1, int((h - 40) // 26)), 26)}"/>'
        else:
            sys.exit(f"wf: type inconnu {kind}")
        self.body.append(f'<g id="{id}">{out}</g>')
        self.nodes[id] = Node(id, cx, cy, w / 2, h / 2)
        return id

    def badge(self, cx, cy, n):
        """Pastille numérotée au stylo bleu (légende des maquettes)."""
        p = self.pen(f"badge{n}")
        self.over.append(f'<path class="inkb" d="{p.ellipse(cx, cy, 20, 20)}"/>' + self._text(cx, cy, str(n), "tb", 28))

    # ------------------------------------------------------------------ liens
    def _edge(self, n, tx, ty, gap):
        dx, dy = tx - n.cx, ty - n.cy
        k = 1 / max(abs(dx) / (n.hw + gap), abs(dy) / (n.hh + gap), 1e-6)
        return n.cx + dx * k, n.cy + dy * k

    def link(self, a, b, kind="ink", label="", bend=0.0, gap=(12, 18)):
        A, B = self.nodes[a], self.nodes[b]
        x1, y1 = self._edge(A, B.cx, B.cy, gap[0])
        x2, y2 = self._edge(B, A.cx, A.cy, gap[1])
        dx, dy = x2 - x1, y2 - y1
        if abs(dx) >= abs(dy) * 0.7:
            o = dy * bend
            d = f"M{num(x1)} {num(y1)} C{num(x1 + dx / 2)} {num(y1 + o)} {num(x2 - dx / 2)} {num(y2 - o)} {num(x2)} {num(y2)}"
        else:
            o = dx * bend
            d = f"M{num(x1)} {num(y1)} C{num(x1 + o)} {num(y1 + dy / 2)} {num(x2 - o)} {num(y2 - dy / 2)} {num(x2)} {num(y2)}"
        cls = LINK[kind][0]
        self.under.append(f'<path class="{cls}" d="{d}"/>')
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            half = len(label) * 8.5 + 10  # demi-largeur estimée du texte (36 px)
            if abs(dx) >= abs(dy) * 1.6:
                lx, ly = mx, my - 32  # lien horizontal: libellé au-dessus
            else:
                side = 1 if dx >= 0 else -1  # lien plutôt vertical: libellé sur le côté extérieur
                lx, ly = mx + side * (half + 14), my
            self.body.append(self._text(lx, ly, label, "tb" if kind == "blue" else "t", 30))
        return d

    def arrow(self, x1, y1, x2, y2, kind="ink", bow=0.12):
        dx, dy = x2 - x1, y2 - y1
        d = f"M{num(x1)} {num(y1)} Q{num((x1 + x2) / 2 - dy * bow)} {num((y1 + y2) / 2 + dx * bow)} {num(x2)} {num(y2)}"
        self.over.append(f'<path class="{LINK[kind][0]}" d="{d}"/>')

    # ------------------------------------------------------------------ annotations et périmètres
    def perimeter(self, ids, label="", pad=58):
        ns = [self.nodes[i] for i in ids]
        x0 = min(n.cx - n.hw for n in ns) - pad
        x1 = max(n.cx + n.hw for n in ns) + pad
        y0 = min(n.cy - n.hh for n in ns) - pad
        y1 = max(n.cy + n.hh for n in ns) + pad
        p = self.pen("per")
        self.under.insert(0, f'<path class="dotk" d="{p.box(x0, y0, x1 - x0, y1 - y0, j=3, o=8)}"/>')
        if label:
            self.body.append(self._text(x0 + 24, y0 - 24, label, "tb" if False else "t", 32, "l"))
        return (x0, y0, x1, y1)

    def note(self, x, y, label, target=None, anchor="middle"):
        """Annotation au stylo bleu, avec flèche vers un objet (optionnel)."""
        self.body.append(self._text(x, y, label, "tb", 32))
        if target:
            n = self.nodes[target]
            tx, ty = self._edge(n, x, y, 14)
            sx, sy = x, y + 26 if ty > y else y - 36
            self.arrow(sx, sy, tx, ty, "blue", 0.18)

    def highlight(self, cx, cy, w, h=10):
        """Surligneur gris derrière un mot (à appeler avant le texte)."""
        self.under.append(f'<path class="hl" d="M{num(cx - w / 2)} {num(cy)} L{num(cx + w / 2)} {num(cy - 2)}"/>')

    # ------------------------------------------------------------------ sortie
    def raw(self, svg_fragment, under=False):
        """Ajoute du SVG brut (formes libres) au dessin."""
        (self.under if under else self.body).append(svg_fragment)

    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}">\n'
                + "\n".join(self.under) + "\n" + "\n".join(self.body) + "\n" + "\n".join(self.over) + "\n</svg>\n")

    def save(self, path):
        pathlib.Path(path).write_text(self.svg(), encoding="utf-8")
        print(path, f"({len(self.nodes)} objets)")


def distribute(n, a, b):
    """n positions régulièrement réparties entre a et b (centres)."""
    if n == 1:
        return [(a + b) / 2]
    return [a + (b - a) * i / (n - 1) for i in range(n)]
