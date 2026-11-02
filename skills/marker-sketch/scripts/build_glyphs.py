#!/usr/bin/env python3
"""Génère assets/glyphes.svg : la bibliothèque de symboles dessinés « au feutre ».

Chaque symbole est un <g id="g-nom" data-w data-h data-desc> contenant les couches
ombre / papier / aplat / contour. Les irrégularités (dépassements aux angles, côtés non
parallèles, cercles ouverts) viennent d'un générateur pseudo-aléatoire déterministe par
symbole: relancer le script donne exactement le même résultat.

Usage: python3 scripts/build_glyphs.py
"""
import html
import math
import pathlib
import random
import zlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "glyphes.svg"


# ------------------------------------------------------------------ primitives de tracé
def num(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


class Pen:
    """Générateur de tracés irréguliers, déterministe pour un nom donné."""

    def __init__(self, name):
        self.r = random.Random(zlib.crc32(name.encode()))

    def j(self, a=1.8):
        return self.r.uniform(-a, a)

    def box(self, x, y, w, h, j=2.0, o=5.0):
        """Rectangle ouvert: quatre côtés légèrement non parallèles, dépassements aux angles."""
        r = self.r
        p = [
            (x - o * r.random(), y + self.j(j)),
            (x + w + o * r.random() * 0.7, y + self.j(j)),
            (x + w + self.j(j), y + h + o * r.random() * 0.7),
            (x - o * r.random() * 0.8, y + h + self.j(j)),
            (x + self.j(j), y - o * r.random()),
        ]
        return "M" + " L".join(f"{num(a)} {num(b)}" for a, b in p)

    def rbox(self, x, y, w, h, rad=14, j=1.6):
        r = self.r
        q = rad
        return (
            f"M{num(x + q)} {num(y + self.j(j))} L{num(x + w - q)} {num(y + self.j(j))} "
            f"Q{num(x + w + self.j(j))} {num(y)} {num(x + w)} {num(y + q)} L{num(x + w + self.j(j))} {num(y + h - q)} "
            f"Q{num(x + w)} {num(y + h)} {num(x + w - q)} {num(y + h + self.j(j))} L{num(x + q)} {num(y + h + self.j(j))} "
            f"Q{num(x)} {num(y + h)} {num(x + self.j(j))} {num(y + h - q)} L{num(x + self.j(j))} {num(y + q)} "
            f"Q{num(x)} {num(y)} {num(x + q + 3 + 4 * r.random())} {num(y - 1.5)}"
        )

    def smooth(self, pts, closed=False):
        """Courbe de Catmull-Rom passant par les points, convertie en Bézier cubique."""
        n = len(pts)
        d = f"M{num(pts[0][0])} {num(pts[0][1])}"
        rng = range(n) if closed else range(n - 1)
        for i in rng:
            p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
            p1 = pts[i]
            p2 = pts[(i + 1) % n]
            p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
            c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
            c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
            d += f" C{num(c1[0])} {num(c1[1])} {num(c2[0])} {num(c2[1])} {num(p2[0])} {num(p2[1])}"
        return d + (" Z" if closed else "")

    def ellipse(self, cx, cy, rx, ry, j=0.045, extra=0.05, n=12):
        """Cercle à la main: ne se referme pas exactement, rayon irrégulier."""
        r = self.r
        a0 = r.uniform(0, math.tau)
        total = math.tau * (1 + extra)
        pts = []
        for i in range(n + 1):
            a = a0 + total * i / n
            k = 1 + self.j(j)
            if i == n:
                k += 0.05  # la fin dépasse légèrement
            pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
        return self.smooth(pts)

    def blob(self, cx, cy, rx, ry, j=0.07, n=9):
        a0 = self.r.uniform(0, math.tau)
        pts = []
        for i in range(n):
            a = a0 + math.tau * i / n
            k = 1 + self.j(j)
            pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
        return self.smooth(pts, closed=True)

    def poly(self, pts, close=True, j=1.6, over=0):
        p = [(x + self.j(j), y + self.j(j)) for x, y in pts]
        d = "M" + " L".join(f"{num(a)} {num(b)}" for a, b in p)
        if close:
            d += " Z"
        return d

    def line(self, x1, y1, x2, y2, bow=2.5):
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy) or 1
        b = self.j(bow)
        cx, cy = mx - dy / ln * b, my + dx / ln * b
        return f"M{num(x1)} {num(y1)} Q{num(cx)} {num(cy)} {num(x2)} {num(y2)}"

    def lines(self, x, y, w, n, gap, lens=None, bow=2.2):
        """Lignes de texte simulées (traits horizontaux de longueurs variables)."""
        d = []
        for i in range(n):
            ln = (lens[i] if lens else self.r.uniform(0.55, 1.0)) * w
            yy = y + i * gap + self.j(1.2)
            d.append(self.line(x, yy, x + ln, yy + self.j(1.5), bow))
        return " ".join(d)


# ------------------------------------------------------------------ assemblage d'un symbole
class Glyph:
    def __init__(self, gid, w, h, desc):
        self.gid, self.w, self.h, self.desc = gid, w, h, desc
        self.pen = Pen(gid)
        self.parts = []
        self.n = 0

    def obj(self, d, fill="fx", shadow=(-7, 10), paper=True, off=(-2.5, 2.5), cls="ink", extra_fill=None):
        """Objet à trois couches. fill: 'fx' (aplat gris/accent), 'f4' (noir), 'f1' (gris clair), None."""
        self.n += 1
        i = f"o{self.gid[1:]}-{self.n}"
        s = ""
        if shadow:
            s += f'<use href="#{i}" x="{shadow[0]}" y="{shadow[1]}" class="sh"/>'
        if paper:
            s += f'<use href="#{i}" class="pp"/>'
        if fill:
            s += f'<use href="#{i}" x="{off[0]}" y="{off[1]}" class="{fill}"/>'
        s += f'<g class="{cls}"><path id="{i}" d="{d}"/></g>'
        self.parts.append(s)

    def stroke(self, d, cls="fine"):
        self.parts.append(f'<path class="{cls}" d="{d}"/>')

    def hl(self, d):
        self.parts.append(f'<path class="hl" d="{d}"/>')

    def raw(self, s):
        self.parts.append(s)

    def svg(self):
        return (
            f'<g id="{self.gid}" data-w="{self.w}" data-h="{self.h}" data-desc="{html.escape(self.desc, quote=True)}">\n'
            + "\n".join(self.parts)
            + "\n</g>"
        )


GLYPHS = []


def glyph(gid, w, h, desc):
    def deco(fn):
        g = Glyph(gid, w, h, desc)
        fn(g, g.pen)
        GLYPHS.append(g)
        return fn

    return deco


# ------------------------------------------------------------------ personnes
@glyph("g-person", 120, 140, "personne (buste: tête ronde, épaules en dôme)")
def _(g, p):
    g.obj(p.ellipse(60, 30, 27, 27), fill="fx", shadow=(-5, 7), off=(-2, 2))
    g.obj(p.smooth([(14, 136), (16, 100), (34, 74), (60, 68), (86, 74), (104, 100), (106, 136)], closed=False) + " Z", fill="fx", shadow=(-6, 9))


@glyph("g-person-sm", 64, 76, "petite personne pour foules, réseaux, listes")
def _(g, p):
    g.obj(p.ellipse(32, 15, 13, 13), fill=None, shadow=None)
    g.obj(p.smooth([(6, 72), (8, 52), (18, 40), (32, 37), (46, 40), (56, 52), (58, 72)]) + " Z", fill=None, shadow=None)


@glyph("g-person-dark", 120, 140, "personne en silhouette noire (accent de rôle)")
def _(g, p):
    g.obj(p.ellipse(60, 30, 27, 27), fill="f4", shadow=(-5, 7), off=(-1, 1))
    g.obj(p.smooth([(14, 136), (16, 100), (34, 74), (60, 68), (86, 74), (104, 100), (106, 136)]) + " Z", fill="f4", shadow=(-6, 9), off=(-1, 1))


@glyph("g-group", 190, 90, "groupe de trois personnes")
def _(g, p):
    for k, (x, y) in enumerate([(0, 10), (62, 0), (124, 10)]):
        g.raw(f'<use href="#g-person-sm" x="{x}" y="{y}"/>')


# ------------------------------------------------------------------ cartes, documents
@glyph("g-card", 230, 150, "carte avec lignes de texte simulées")
def _(g, p):
    g.obj(p.box(0, 0, 230, 150), fill=None)
    g.hl(p.line(26, 50, 150, 50, 1.5))
    g.stroke(p.lines(26, 42, 170, 3, 30, [0.9, 1.0, 0.6]), cls="mid")


@glyph("g-card-img", 210, 190, "carte avec image (rectangle barré) et deux lignes")
def _(g, p):
    g.obj(p.box(0, 0, 210, 190), fill=None)
    g.obj(p.box(18, 18, 174, 94, o=3), fill="fx", shadow=None, paper=False, off=(-2, 2))
    g.stroke(p.line(20, 20, 190, 110, 1.5) + " " + p.line(190, 20, 20, 110, 1.5), cls="mid")
    g.stroke(p.lines(20, 138, 150, 2, 26, [0.95, 0.6]), cls="mid")


@glyph("g-doc", 140, 180, "page de document avec coin plié et lignes")
def _(g, p):
    g.obj(p.poly([(0, 0), (100, 0), (140, 40), (140, 180), (0, 180)], j=1.4), fill=None)
    g.stroke(p.poly([(100, 0), (100, 40), (140, 40)], close=False, j=1.2), cls="mid")
    g.stroke(p.lines(22, 76, 96, 4, 26, [0.95, 0.85, 1.0, 0.5]))


@glyph("g-sticky", 120, 120, "note adhésive carrée (post-it)")
def _(g, p):
    g.obj(p.poly([(0, 0), (120, 0), (120, 88), (92, 120), (0, 120)], j=1.4), fill="fx", off=(-3, 3))
    g.stroke(p.poly([(92, 120), (92, 90), (120, 88)], close=False, j=1.2), cls="mid")
    g.stroke(p.lines(18, 36, 80, 2, 24, [0.9, 0.6]), cls="mid")


@glyph("g-list", 180, 140, "liste à puces")
def _(g, p):
    for i in range(4):
        y = 16 + i * 38
        g.obj(p.ellipse(14, y, 9, 9), fill="f4", shadow=None, paper=False, off=(-1, 1))
        g.stroke(p.line(40, y, 40 + p.r.uniform(80, 138), y + p.j(2), 1.5), cls="mid")


# ------------------------------------------------------------------ interfaces
@glyph("g-window", 330, 220, "fenêtre d'application: barre de titre, barre latérale, deux cartes")
def _(g, p):
    g.obj(p.box(0, 0, 330, 220), fill=None)
    g.obj(p.box(0, 0, 330, 38, o=2), fill="fx", shadow=None, paper=False, off=(-1.5, 1.5))
    g.stroke(p.line(66, 38, 66, 218, 1.5), cls="mid")
    g.obj(p.box(86, 58, 100, 64, o=3), fill=None, shadow=(-4, 6), cls="mid")
    g.obj(p.box(204, 58, 100, 64, o=3), fill=None, shadow=(-4, 6), cls="mid")
    g.stroke(p.lines(88, 150, 200, 3, 22, [1.0, 0.8, 0.55]))
    g.stroke(p.lines(14, 62, 38, 3, 26, [1.0, 0.8, 0.9]))


@glyph("g-browser", 350, 240, "navigateur: pastilles, barre d'adresse, image et texte")
def _(g, p):
    g.obj(p.box(0, 0, 350, 240), fill=None)
    g.obj(p.box(0, 0, 350, 42, o=2), fill="fx", shadow=None, paper=False, off=(-1.5, 1.5))
    for k in range(3):
        g.obj(p.ellipse(22 + k * 22, 21, 5, 5), fill="f4", shadow=None, paper=False, off=(0, 0))
    g.obj(p.rbox(104, 11, 200, 20, 10), fill=None, shadow=None, paper=True, cls="fine")
    g.obj(p.box(24, 62, 130, 90, o=3), fill="fx", shadow=None, paper=False, off=(-2, 2))
    g.stroke(p.line(26, 64, 152, 150, 1.5) + " " + p.line(152, 64, 26, 150, 1.5), cls="mid")
    g.stroke(p.lines(178, 74, 150, 5, 24, [1.0, 0.85, 0.95, 0.7, 0.9]))
    g.stroke(p.lines(24, 184, 300, 2, 24, [1.0, 0.75]))


@glyph("g-phone", 120, 230, "téléphone (écran, encoche, bouton)")
def _(g, p):
    g.obj(p.rbox(0, 0, 120, 230, 18), fill=None)
    g.obj(p.box(12, 36, 96, 140, o=2), fill="fx", shadow=None, paper=False, off=(-2, 2))
    g.obj(p.rbox(40, 12, 40, 10, 5), fill="f4", shadow=None, paper=False, off=(0, 0))
    g.stroke(p.ellipse(60, 204, 10, 10), cls="mid")
    g.stroke(p.lines(22, 62, 70, 3, 28, [1.0, 0.75, 0.55]), cls="mid")


@glyph("g-laptop", 270, 180, "portable: cadre noir, écran clair, socle")
def _(g, p):
    g.obj(p.box(30, 0, 210, 132, o=4), fill="f4", off=(0, 0))
    g.obj(p.box(44, 14, 182, 104, o=2), fill="f1", shadow=None, paper=True, off=(-2, 2), cls="fine")
    g.obj(p.poly([(0, 144), (270, 144), (252, 164), (18, 164)], j=1.2), fill="f1", shadow=(-5, 8), off=(-1, 1))
    g.stroke(p.lines(62, 40, 140, 3, 26, [1.0, 0.8, 0.55]), cls="mid")


@glyph("g-screen", 230, 190, "écran de bureau sur pied")
def _(g, p):
    g.obj(p.box(0, 0, 230, 140, o=4), fill=None)
    g.obj(p.box(14, 14, 202, 100, o=2), fill="fx", shadow=None, paper=False, off=(-2, 2), cls="fine")
    g.obj(p.poly([(92, 142), (138, 142), (146, 172), (84, 172)], j=1.2), fill="f1", shadow=None, off=(-1, 1))
    g.stroke(p.line(56, 176, 176, 176, 2))


@glyph("g-book", 230, 150, "livre ouvert")
def _(g, p):
    g.obj(p.smooth([(115, 22), (80, 6), (36, 4), (4, 14), (6, 128), (40, 118), (84, 120), (115, 140)]) + " L115 22 Z", fill=None)
    g.obj(p.smooth([(115, 22), (150, 6), (194, 4), (226, 14), (224, 128), (190, 118), (146, 120), (115, 140)]) + " L115 22 Z", fill=None, shadow=None)
    g.stroke(p.lines(24, 40, 70, 4, 20, [1, 0.8, 1, 0.6]))
    g.stroke(p.lines(136, 40, 70, 4, 20, [1, 0.8, 1, 0.6]))


@glyph("g-bubble", 190, 140, "bulle de dialogue avec lignes")
def _(g, p):
    g.obj(p.poly([(14, 0), (176, 0), (190, 14), (190, 92), (176, 106), (84, 106), (34, 136), (44, 106), (14, 106), (0, 92), (0, 14)], j=1.6), fill=None)
    g.stroke(p.lines(24, 30, 138, 3, 24, [1.0, 0.85, 0.5]), cls="mid")


@glyph("g-bubble-q", 96, 96, "bulle grise avec point d'interrogation")
def _(g, p):
    g.obj(p.blob(48, 48, 40, 38), fill="fx", off=(-3, 3))
    g.stroke("M34 38 C34 18 62 18 62 38 C62 52 48 52 48 66", cls="ink")
    g.obj(p.ellipse(48, 78, 3, 3), fill="f4", shadow=None, paper=False, off=(0, 0))


@glyph("g-bubble-bang", 96, 96, "bulle grise avec point d'exclamation")
def _(g, p):
    g.obj(p.blob(48, 48, 40, 38), fill="fx", off=(-3, 3))
    g.stroke("M48 22 L47 56", cls="ink")
    g.obj(p.ellipse(48, 72, 3.5, 3.5), fill="f4", shadow=None, paper=False, off=(0, 0))


@glyph("g-check", 70, 70, "pastille avec coche (validé)")
def _(g, p):
    g.obj(p.ellipse(35, 35, 29, 29), fill=None, shadow=(-4, 6))
    g.stroke("M20 36 L31 48 L52 22", cls="ink")


@glyph("g-cross", 70, 70, "pastille avec croix (refusé)")
def _(g, p):
    g.obj(p.ellipse(35, 35, 29, 29), fill=None, shadow=(-4, 6))
    g.stroke(p.line(22, 22, 48, 48, 1) + " " + p.line(48, 22, 22, 48, 1), cls="ink")


@glyph("g-code", 90, 54, "chevrons de code </>")
def _(g, p):
    g.stroke("M28 8 L7 27 L28 46 M62 8 L83 27 L62 46 M52 2 L38 52", cls="ink")


# ------------------------------------------------------------------ infrastructure
@glyph("g-cloud", 200, 130, "nuage")
def _(g, p):
    g.obj("M44 116 C8 116 2 74 36 66 C34 30 84 14 108 40 C126 10 184 24 174 66 C204 72 202 116 168 116 Z", fill=None)


@glyph("g-db", 120, 150, "base de données (cylindre à disques)")
def _(g, p):
    g.obj(p.ellipse(60, 24, 54, 17) + " " + p.line(6, 24, 6, 120, 1.5) + " " + p.line(114, 24, 114, 120, 1.5) + " M6 120 C6 148 114 148 114 120", fill="fx", off=(-2, 2), shadow=(-6, 10))
    g.stroke("M6 56 C6 82 114 82 114 56 M6 88 C6 114 114 114 114 88", cls="mid")


@glyph("g-clock", 90, 90, "horloge")
def _(g, p):
    g.obj(p.ellipse(45, 45, 39, 39), fill=None, shadow=(-4, 7))
    g.stroke("M45 45 L45 20 M45 45 L63 56", cls="ink")


@glyph("g-chart", 240, 190, "graphique: axes et courbe en dents de scie")
def _(g, p):
    g.stroke("M16 8 L16 168 L228 168", cls="ink")
    g.stroke("M30 146 L74 100 L112 124 L160 56 L206 70", cls="ink")
    g.stroke(p.ellipse(206, 70, 6, 6), cls="mid")


@glyph("g-kanban", 300, 200, "tableau kanban à trois colonnes (à faire, en cours, fait)")
def _(g, p):
    for c in range(3):
        x = c * 104
        g.stroke(p.line(x, 8, x + 80, 8, 2), cls="mid")
        for k in range(2 if c != 1 else 1):
            f = "fx" if (c == 1 and k == 0) else None
            g.obj(p.box(x + 8, 34 + k * 62, 56, 50, o=3), fill=f, shadow=(-4, 6), off=(-2, 2), cls="mid")


@glyph("g-agent", 160, 130, "agent: boîte à deux yeux et petits pieds (mascotte)")
def _(g, p):
    g.obj(p.box(0, 0, 160, 100, o=4), fill="fx", off=(-3, 3), shadow=(-6, 9))
    g.obj(p.box(32, 34, 20, 26, o=1.5, j=1), fill="f4", shadow=None, paper=False, off=(0, 0))
    g.obj(p.box(108, 34, 20, 26, o=1.5, j=1), fill="f4", shadow=None, paper=False, off=(0, 0))
    g.obj(p.box(34, 102, 14, 22, o=2, j=1), fill=None, shadow=None, paper=True, cls="mid")
    g.obj(p.box(112, 102, 14, 22, o=2, j=1), fill=None, shadow=None, paper=True, cls="mid")


@glyph("g-button", 170, 64, "bouton (pilule avec libellé simulé)")
def _(g, p):
    g.obj(p.rbox(0, 0, 170, 64, 30), fill="fx", off=(-2, 2), shadow=(-5, 8))
    g.stroke(p.line(44, 32, 126, 32, 1.5), cls="mid")


@glyph("g-toggle", 110, 56, "interrupteur activé")
def _(g, p):
    g.obj(p.rbox(0, 0, 110, 56, 28), fill="fx", off=(-2, 2), shadow=(-4, 7))
    g.obj(p.ellipse(82, 28, 17, 17), fill="f4", shadow=None, paper=False, off=(0, 0))


@glyph("g-input", 270, 64, "champ de saisie")
def _(g, p):
    g.obj(p.box(0, 0, 270, 64, o=3), fill=None, shadow=(-4, 7))
    g.stroke(p.line(22, 18, 22, 46, 0.8), cls="mid")


# ------------------------------------------------------------------ objets du quotidien
@glyph("g-cursor", 80, 110, "curseur flèche de souris")
def _(g, p):
    g.obj(p.poly([(4, 4), (4, 92), (26, 70), (44, 108), (60, 100), (42, 64), (74, 62)], j=1.2), fill="f4", off=(-2, 2), shadow=(-6, 9))


@glyph("g-bulb", 90, 130, "ampoule (idée)")
def _(g, p):
    g.obj(p.smooth([(30, 96), (14, 74), (6, 50), (14, 22), (45, 6), (76, 22), (84, 50), (76, 74), (60, 96)]) + " Z", fill="fx", off=(-3, 3), shadow=(-5, 8))
    g.obj(p.box(28, 98, 34, 24, o=2), fill=None, shadow=None, cls="mid")
    g.stroke(p.line(36, 104, 56, 104, 1) + " M45 56 L45 82", cls="mid")


@glyph("g-star", 90, 90, "étoile")
def _(g, p):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        r = 42 if i % 2 == 0 else 18
        pts.append((45 + r * math.cos(a), 46 + r * math.sin(a)))
    g.obj(p.poly(pts, j=1.4), fill="fx", off=(-2, 2), shadow=(-4, 7))


@glyph("g-heart", 90, 84, "cœur")
def _(g, p):
    g.obj("M45 78 C16 54 4 40 8 24 C12 6 38 6 45 26 C52 6 78 6 82 24 C86 40 74 54 45 78 Z", fill="fx", off=(-2, 2), shadow=(-4, 7))


@glyph("g-flag", 80, 140, "drapeau sur mât (objectif)")
def _(g, p):
    g.stroke(p.line(14, 6, 14, 138, 2), cls="ink")
    g.obj(p.poly([(14, 8), (74, 24), (14, 54)], j=1.2), fill="fx", off=(-2, 2), shadow=(-4, 6))


@glyph("g-lock", 90, 120, "cadenas")
def _(g, p):
    g.stroke("M22 54 L22 36 C22 6 68 6 68 36 L68 54", cls="ink")
    g.obj(p.box(8, 52, 74, 60, o=3), fill="fx", off=(-3, 3), shadow=(-5, 8))
    g.obj(p.ellipse(45, 80, 6, 6), fill="f4", shadow=None, paper=False, off=(0, 0))


@glyph("g-target", 120, 120, "cible (trois cercles et point)")
def _(g, p):
    g.obj(p.ellipse(60, 60, 54, 54), fill=None, shadow=(-5, 8))
    g.stroke(p.ellipse(60, 60, 34, 34), cls="ink")
    g.obj(p.ellipse(60, 60, 14, 14), fill="f4", shadow=None, paper=False, off=(0, 0))


@glyph("g-bolt", 70, 120, "éclair")
def _(g, p):
    g.obj(p.poly([(44, 2), (6, 66), (32, 66), (22, 118), (64, 48), (38, 48)], j=1.2), fill="fx", off=(-2, 2), shadow=(-5, 8))


@glyph("g-magnifier", 120, 120, "loupe")
def _(g, p):
    g.obj(p.ellipse(48, 48, 38, 38), fill="f1", off=(-3, 3), shadow=(-5, 8))
    g.stroke(p.line(76, 76, 112, 112, 1.5), cls="ink")


@glyph("g-mug", 120, 120, "tasse")
def _(g, p):
    g.obj("M10 14 C8 70 12 104 40 108 C70 112 92 102 92 14 Z", fill="fx", off=(-3, 2), shadow=(-6, 8))
    g.stroke("M92 38 C124 30 124 82 92 80", cls="ink")
    g.stroke(p.ellipse(51, 14, 41, 8), cls="mid")


@glyph("g-pen", 120, 40, "stylo ou feutre en biais")
def _(g, p):
    g.obj(p.poly([(0, 20), (20, 4), (112, 2), (116, 28), (20, 36)], j=1.2), fill="fx", off=(-2, 2), shadow=(-4, 6))
    g.stroke(p.line(24, 6, 22, 34, 1), cls="mid")


@glyph("g-gear", 110, 110, "engrenage")
def _(g, p):
    pts = []
    n = 8
    for i in range(n * 2):
        a0 = i * math.pi / n - math.pi / (2 * n)
        r = 50 if i % 2 == 0 else 38
        a1 = a0 + math.pi / n
        pts.append((55 + r * math.cos(a0 + 0.07), 55 + r * math.sin(a0 + 0.07)))
        pts.append((55 + r * math.cos(a1 - 0.07), 55 + r * math.sin(a1 - 0.07)))
    g.obj(p.poly(pts, j=1.0), fill="fx", off=(-2, 2), shadow=(-5, 8))
    g.stroke(p.ellipse(55, 55, 14, 14), cls="ink")


@glyph("g-pin", 80, 120, "repère de carte")
def _(g, p):
    g.obj("M40 114 C10 74 4 56 4 40 C4 14 22 2 40 2 C58 2 76 14 76 40 C76 56 70 74 40 114 Z", fill="fx", off=(-3, 3), shadow=(-5, 8))
    g.stroke(p.ellipse(40, 40, 11, 11), cls="ink")


@glyph("g-ladder", 70, 320, "échelle (niveaux d'abstraction)")
def _(g, p):
    g.stroke(p.line(8, 4, 12, 318, 3) + " " + p.line(60, 4, 58, 318, 3), cls="ink")
    for k in range(9):
        y = 30 + k * 33
        g.stroke(p.line(10, y, 58, y + p.j(3), 1.5), cls="mid")


@glyph("g-hills", 300, 90, "ligne d'horizon: collines")
def _(g, p):
    g.stroke("M0 70 C40 20 80 14 118 50 C150 76 176 40 210 36 C250 32 276 52 300 66", cls="ink")


@glyph("g-arrow-block", 150, 90, "grosse flèche pleine (transition, phase suivante)")
def _(g, p):
    g.obj(p.poly([(0, 26), (88, 24), (88, 2), (150, 46), (88, 88), (90, 66), (2, 64)], j=1.6), fill="f3" if False else "fx", off=(-3, 3), shadow=(-5, 8))


@glyph("g-pile", 200, 120, "pile de trois cartes (collection, backlog)")
def _(g, p):
    for k, (x, y) in enumerate([(0, 0), (14, 24), (28, 48)]):
        g.obj(p.box(x, y, 150, 56, o=3), fill=None, shadow=(-4, 6) if k == 2 else None)
        g.stroke(p.lines(x + 14, y + 22, 90, 1, 0, [1.0]), cls="mid")


# ------------------------------------------------------------------ sortie
def main():
    body = "\n".join(g.svg() for g in GLYPHS)
    OUT.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg"><defs>\n' + body + "\n</defs></svg>\n",
        encoding="utf-8",
    )
    print(f"{len(GLYPHS)} symboles -> {OUT} ({OUT.stat().st_size // 1024} ko)")


if __name__ == "__main__":
    main()
