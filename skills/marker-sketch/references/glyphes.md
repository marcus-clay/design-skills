# Bibliothèque de symboles

47 symboles dessinés au feutre, prêts à poser. Aperçu visuel : `planche-symboles.png`. Liste à jour : `python3 scripts/compose.py --catalog`.

## 1. Utilisation

```svg
<use href="#g-person" x="540" y="260"/>                  <!-- coin haut gauche en (540, 260) -->
<use href="#g-person" x="540" y="260" class="cb"/>       <!-- teinte: cb co cr cs ch, gris c1 c3 c4 -->
<g transform="translate(540 260) scale(.6)"><use href="#g-person"/></g>   <!-- à l'échelle -->
```

Avec `sketch.py` : `s.glyph("p", "g-person", cx, cy, "Utilisateur", scale=1.0, cls="cb")` (centré en cx, cy, libellé dessous).

Règles : l'origine d'un symbole est son coin haut gauche, ses dimensions sont données ci-dessous. À l'échelle 0,5 le trait reste lisible, en dessous de 0,4 préférer un autre symbole. `compose.py` injecte tout seul les symboles utilisés dans le fichier final (les autres ne pèsent rien). Les symboles qui portent une teinte d'aplat (`fx`) acceptent les classes de teinte ; ceux en noir plein (`g-person-dark`) et ceux sans aplat non.

## 2. Catalogue

| Symbole | Taille | Description |
|---|---|---|
| `g-person` | 120 × 140 | personne (buste: tête ronde, épaules en dôme) |
| `g-person-sm` | 64 × 76 | petite personne pour foules, réseaux, listes |
| `g-person-dark` | 120 × 140 | personne en silhouette noire (accent de rôle) |
| `g-group` | 190 × 90 | groupe de trois personnes |
| `g-card` | 230 × 150 | carte avec lignes de texte simulées |
| `g-card-img` | 210 × 190 | carte avec image (rectangle barré) et deux lignes |
| `g-doc` | 140 × 180 | page de document avec coin plié et lignes |
| `g-sticky` | 120 × 120 | note adhésive carrée (post-it) |
| `g-list` | 180 × 140 | liste à puces |
| `g-window` | 330 × 220 | fenêtre d'application: barre de titre, barre latérale, deux cartes |
| `g-browser` | 350 × 240 | navigateur: pastilles, barre d'adresse, image et texte |
| `g-phone` | 120 × 230 | téléphone (écran, encoche, bouton) |
| `g-laptop` | 270 × 180 | portable: cadre noir, écran clair, socle |
| `g-screen` | 230 × 190 | écran de bureau sur pied |
| `g-book` | 230 × 150 | livre ouvert |
| `g-bubble` | 190 × 140 | bulle de dialogue avec lignes |
| `g-bubble-q` | 96 × 96 | bulle grise avec point d'interrogation |
| `g-bubble-bang` | 96 × 96 | bulle grise avec point d'exclamation |
| `g-check` | 70 × 70 | pastille avec coche (validé) |
| `g-cross` | 70 × 70 | pastille avec croix (refusé) |
| `g-code` | 90 × 54 | chevrons de code </> |
| `g-cloud` | 200 × 130 | nuage |
| `g-db` | 120 × 150 | base de données (cylindre à disques) |
| `g-clock` | 90 × 90 | horloge |
| `g-chart` | 240 × 190 | graphique: axes et courbe en dents de scie |
| `g-kanban` | 300 × 200 | tableau kanban à trois colonnes (à faire, en cours, fait) |
| `g-agent` | 160 × 130 | agent: boîte à deux yeux et petits pieds (mascotte) |
| `g-button` | 170 × 64 | bouton (pilule avec libellé simulé) |
| `g-toggle` | 110 × 56 | interrupteur activé |
| `g-input` | 270 × 64 | champ de saisie |
| `g-cursor` | 80 × 110 | curseur flèche de souris |
| `g-bulb` | 90 × 130 | ampoule (idée) |
| `g-star` | 90 × 90 | étoile |
| `g-heart` | 90 × 84 | cœur |
| `g-flag` | 80 × 140 | drapeau sur mât (objectif) |
| `g-lock` | 90 × 120 | cadenas |
| `g-target` | 120 × 120 | cible (trois cercles et point) |
| `g-bolt` | 70 × 120 | éclair |
| `g-magnifier` | 120 × 120 | loupe |
| `g-mug` | 120 × 120 | tasse |
| `g-pen` | 120 × 40 | stylo ou feutre en biais |
| `g-gear` | 110 × 110 | engrenage |
| `g-pin` | 80 × 120 | repère de carte |
| `g-ladder` | 70 × 320 | échelle (niveaux d'abstraction) |
| `g-hills` | 300 × 90 | ligne d'horizon: collines |
| `g-arrow-block` | 150 × 90 | grosse flèche pleine (transition, phase suivante) |
| `g-pile` | 200 × 120 | pile de trois cartes (collection, backlog) |

## 3. Ajouter un symbole

Le fichier `assets/glyphes.svg` est généré par `scripts/build_glyphs.py` : ne pas l'éditer à la main. Ajouter une fonction dans le script avec la classe `Glyph` :

```python
@glyph("g-trophee", 100, 130, "trophée (réussite)")
def _(g, p):
    g.obj(p.rbox(20, 10, 60, 70), fill="fx")                 # objet à trois couches (ombre, papier, aplat) + contour
    g.stroke(p.line(50, 80, 50, 110), cls="ink")              # simple trait
    g.obj(p.box(25, 110, 50, 14), fill="f4", shadow=None)     # base noire sans ombre
```

Placer la fonction avant `main()` dans `scripts/build_glyphs.py`. `g.raw(...)` accepte du SVG libre, par exemple `<use href="#g-person-sm" x="0" y="10"/>` pour composer un symbole à partir d'un autre.

Outils de tracé de `Pen` : `box`, `rbox`, `ellipse`, `blob`, `poly`, `line`, `lines`, `smooth`. Le tracé est déterministe par nom de symbole : relancer le script redonne le même dessin. Puis `python3 scripts/build_glyphs.py && python3 scripts/sheet.py` et vérifier la planche.

## 4. Symbole en perspective (optionnel, hors usage courant)

three.js n'est pas utilisé à l'exécution. Il ne sert qu'à fabriquer, une fois, un symbole en perspective qui manque (cube, escalier, étagère, bureau en 3/4) :

1. Construire la géométrie avec `BoxGeometry` ou `ExtrudeGeometry`, la poser en perspective faible (caméra à 35 degrés, `fov` 25).
2. Extraire les arêtes visibles avec `EdgesGeometry` (seuil 25 degrés), projeter chaque arête en 2D.
3. Redessiner chaque arête avec `Pen.line` (trait feutre, léger arc, dépassement aux angles) et remplir les faces avec `f1`, `f2`, `f3` selon l'orientation (haut clair, côté moyen, ombre foncée).
4. Ajouter le résultat à `build_glyphs.py` comme un symbole ordinaire.

Ne jamais envoyer three.js au lecteur : le livrable reste un SVG.
