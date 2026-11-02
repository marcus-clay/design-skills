#!/usr/bin/env python3
"""Rend un SVG (ou un HTML) en PNG avec Chromium, pour contrôler visuellement le résultat.

Usage:
    python3 render.py croquis.svg                # écrit croquis.png à côté
    python3 render.py croquis.svg -o sortie.png  # chemin explicite
    python3 render.py croquis.svg --scale 2      # PNG 2x (3200 px de large)
    python3 render.py page.html --wait 800       # HTML interactif, attend 800 ms avant capture
    python3 render.py page.html --state 2        # HTML interactif, positionné sur l'état 2

Pourquoi Chromium: les filtres SVG (feTurbulence, feDisplacementMap) qui donnent le trait
feutre ne sont pas rendus correctement par la plupart des convertisseurs (cairosvg, ImageMagick).
"""
import argparse
import pathlib
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("-o", "--out")
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--wait", type=int, default=250, help="millisecondes avant capture")
    ap.add_argument("--state", type=float, default=None, help="état à afficher (HTML interactif)")
    a = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("playwright manquant: pip install playwright && playwright install chromium")

    src = pathlib.Path(a.src).resolve()
    out = pathlib.Path(a.out) if a.out else src.with_suffix(".png")
    is_html = src.suffix.lower() in (".html", ".htm")

    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": a.width, "height": a.height}, device_scale_factor=a.scale)
        if is_html:
            pg.goto(src.as_uri())
            if a.state is not None:
                pg.evaluate(f"window.sketch && window.sketch.jump({a.state})")
            pg.wait_for_timeout(a.wait)
            pg.screenshot(path=str(out))
        else:
            svg = src.read_text(encoding="utf-8")
            pg.set_content(
                "<!doctype html><meta charset='utf-8'><style>html,body{margin:0;background:#fff}"
                "svg{display:block;width:100vw;height:auto}</style>" + svg
            )
            pg.wait_for_timeout(a.wait)
            el = pg.query_selector("svg")
            el.screenshot(path=str(out))
        b.close()
    print(out)


if __name__ == "__main__":
    main()
