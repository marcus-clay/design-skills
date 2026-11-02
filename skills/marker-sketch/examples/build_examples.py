#!/usr/bin/env python3
"""Régénère les cinq exemples statiques (SVG + PNG) avec le constructeur sketch.py.
    python3 examples/build_examples.py
Chaque schéma tient en 10 à 25 lignes: c'est le niveau de détail visé pour une réponse rapide."""
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
BRUT = HERE / "brut"
BRUT.mkdir(exist_ok=True)
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "scripts"))
from sketch import Sketch  # noqa: E402


def venn():
    s = Sketch(seed="venn")
    for i, (x, y) in {"a": (650, 330), "b": (950, 330), "c": (800, 590)}.items():
        s.box(i, x, y, "", w=400, h=400, shape="oval", solid=False)
    s.box("m", 800, 430, "", w=110, h=90, shape="oval", fill="fh")
    s.text(585, 290, "Désirabilité", "tl")
    s.text(1015, 290, "Faisabilité", "tl")
    s.text(800, 690, "Viabilité", "tl")
    s.note(1290, 560, "le bon produit", target="m")
    s.save(BRUT / "venn-produit.svg")


def tree():
    s = Sketch(seed="tree")
    s.box("r", 800, 130, "Utilisateur bloqué ?", fill="f4", shape="pill", w=480)
    s.box("n1", 480, 370, "Article existant ?", shape="pill", w=380)
    s.box("n2", 1120, 370, "Urgent ?", shape="pill", w=300)
    s.glyph("l1", "g-check", 320, 640, "Envoyer le lien", scale=1.1)
    s.glyph("l2", "g-cross", 640, 640, "Rédiger l’article", scale=1.1)
    s.glyph("l3", "g-bolt", 1000, 640, "Escalader", scale=0.9)
    s.glyph("l4", "g-clock", 1260, 640, "File d’attente", scale=1.0)
    s.link("r", "n1", label="non résolu", bend=0.2)
    s.link("r", "n2", bend=0.2)
    s.link("n1", "l1", label="oui", bend=0.2)
    s.link("n1", "l2", label="non", bend=0.2)
    s.link("n2", "l3", label="oui", bend=0.2)
    s.link("n2", "l4", label="non", bend=0.2)
    s.save(BRUT / "arbre-decision.svg")


def stack():
    s = Sketch(seed="stack")
    ys = [160, 350, 540, 730]
    names = ["Interface : chat et widgets", "Orchestrateur d’agents", "Outils et connecteurs", "Données métier"]
    fills = ["f1", "f2", None, "f3"]
    for i, (y, n, f) in enumerate(zip(ys, names, fills)):
        s.box(f"L{i}", 720, y, n, w=640, h=110, fill=f, size=38)
        if f == "f3":
            pass
    for i in range(3):
        s.link(f"L{i}", f"L{i + 1}", kind="gray")
    s.glyph("u", "g-person", 170, 160, "Utilisateur")
    s.glyph("m", "g-cloud", 1330, 350, "Modèle")
    s.glyph("d", "g-db", 1330, 700, "Entrepôt")
    s.link("u", "L0", bend=0)
    s.link("L1", "m", kind="ink", bend=0)
    s.link("L3", "d", kind="ink", bend=0)
    s.perimeter(["L0", "L1", "L2", "L3"], "notre produit", pad=40)
    s.save(BRUT / "architecture-assistant.svg")


def scene():
    s = Sketch(seed="scene")
    s.glyph("w", "g-window", 800, 360, "", scale=1.6)
    s.glyph("p1", "g-person", 330, 560, "Équipe produit", scale=1.1)
    s.glyph("p2", "g-person", 1270, 560, "Design", scale=1.1)
    s.glyph("f", "g-person-dark", 800, 730, "Facilitation", scale=0.85, label_gap=40)
    s.glyph("b", "g-bubble", 360, 270, "", scale=1.0)
    s.glyph("i", "g-bulb", 1240, 250, "", scale=1.0)
    s.glyph("s1", "g-sticky", 520, 770, "", scale=0.7)
    s.glyph("s2", "g-sticky", 1090, 770, "", scale=0.7, cls="ch")
    s.note(1160, 90, "on décide ici", target="w")
    s.save(BRUT / "scene-atelier.svg")


def wireframe():
    s = Sketch(seed="wire")
    # écran 1: accueil
    s.wf("e1", "frame", 130, 150, 360, 640, "1. Accueil")
    s.wf("n1", "nav", 150, 170, 320, 50)
    s.wf("t1", "title", 170, 255, 280, 40, "Bonjour Camille")
    s.wf("i1", "image", 170, 320, 280, 170)
    s.wf("x1", "text", 170, 520, 280, 90)
    s.wf("b1", "button", 170, 660, 280, 70, "Commencer")
    # écran 2: résultats
    s.wf("e2", "frame", 620, 150, 360, 640, "2. Résultats")
    s.wf("n2", "nav", 640, 170, 320, 50)
    s.wf("q2", "input", 660, 250, 280, 56, "Rechercher")
    for k in range(3):
        s.wf(f"c{k}", "card", 660, 340 + k * 150, 280, 125)
    # écran 3: détail
    s.wf("e3", "frame", 1110, 150, 360, 640, "3. Détail")
    s.wf("n3", "nav", 1130, 170, 320, 50)
    s.wf("i3", "image", 1150, 250, 280, 200)
    s.wf("x3", "text", 1150, 480, 280, 120)
    s.wf("b3", "button", 1150, 660, 280, 70, "Réserver", fill="f1")
    s.link("e1", "e2", bend=0)
    s.link("e2", "e3", bend=0)
    s.note(1280, 840, "un seul appel à l’action", target="b3")
    s.save(BRUT / "wireframe-parcours.svg")


def journey():
    s = Sketch(seed="journey")
    s.glyph("i1", "g-magnifier", 260, 190, "", scale=0.9)
    s.glyph("i2", "g-target", 800, 190, "", scale=0.9)
    s.glyph("i3", "g-flag", 1340, 180, "", scale=0.8)
    s.box("a", 260, 420, "Explorer", fill="f1", w=300, h=120)
    s.box("b", 800, 420, "Définir", fill="fh", w=300, h=120)
    s.box("c", 1340, 420, "Livrer", fill="f4", w=300, h=120)
    s.link("a", "b")
    s.link("b", "c")
    s.perimeter(["a", "b"], "Discovery", pad=70)
    s.raw('<path class="flow" d="M1250 520C1250 770 260 770 260 520"/>', under=True)
    s.text(800, 800, "boucle d’apprentissage", "tg")
    s.note(1470, 640, "on mesure ici", target="c")
    s.save(BRUT / "parcours-discovery.svg")


if __name__ == "__main__":
    for fn in (venn, tree, stack, scene, journey, wireframe):
        fn()
    for svg in sorted(BRUT.glob("*.svg")):
        if svg.name.startswith(("migration", "tendance")):
            continue  # pages interactives: voir compose.py --interactive
        final = HERE / svg.name
        subprocess.run([sys.executable, str(ROOT / "scripts" / "compose.py"), str(svg), "-o", str(final), "--outline"], check=True)
        subprocess.run([sys.executable, str(ROOT / "scripts" / "render.py"), str(final), "-o", str(final.with_suffix(".png"))], check=True)
    for name in ("migration-organisation", "tendance-adoption"):
        subprocess.run([sys.executable, str(ROOT / "scripts" / "compose.py"), str(BRUT / f"{name}.svg"),
                        "--interactive", str(BRUT / f"{name}.json"), "-o", str(HERE / f"{name}.html")], check=True)
