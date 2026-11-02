# Mode Live : réunion, atelier, échange oral

Objectif : pendant que les gens parlent, montrer en quelques secondes une vision synthétisée et sketchée, puis la corriger au rythme de la discussion. Le croquis n'est pas un livrable, c'est un support de conversation. La vitesse et la stabilité comptent plus que la finesse.

## 1. Règles

1. **Sept objets au maximum.** Au-delà, regrouper (un périmètre `dotk` autour de trois objets devient un seul objet) ou faire un deuxième croquis.
2. **Texte lisible à quatre mètres** : `t` (36 px) au minimum, `tl` (52 px) pour les titres, jamais `ts`. Un à trois mots par étiquette.
3. **Positions stables.** Une retouche ne déplace que ce qui change. Réutiliser les mêmes identifiants et les mêmes coordonnées d'un tour à l'autre. Dire en une ligne ce qui a changé.
4. **Format 16:9** (1600 × 900), papier `cream` ou `white` (meilleur contraste en projection), pas de papier jaune.
5. **Une seule couleur d'accent**, réservée à ce dont on est en train de parler (surligneur `fh`). Quand le sujet change, déplacer l'accent.
6. **Pas d'embellissement.** Si l'équipe discute du fond, un rectangle suffit. Le symbole vient quand il porte du sens.
7. **Ne pas corriger ce qui n'a pas été dit.** Ne pas inventer de boîtes pour « compléter » le schéma.

## 2. De la parole au dessin

| Ce qu'on entend | Ce qu'on dessine |
|---|---|
| un nom (équipe, outil, écran, personne) | un objet (`box`, symbole) |
| un verbe, « envoie », « valide », « dépend de » | une flèche, libellé de trois mots au plus |
| « d'abord…, puis… » | flux horizontal |
| « mais », « sinon », « ça dépend » | branche (arbre) |
| « avant…, après… », « aujourd'hui…, demain… » | deux zones, ou mode Interactif |
| « plus ou moins », « d'un côté…, de l'autre… » | axe ou matrice 2 × 2 |
| « tout le monde passe par… » | hub |
| « ça bloque », « le problème c'est… » | annotation bleue avec flèche, ou accent `fr` sur un objet |
| « on ne sait pas encore » | contour en tirets (`dash`) et point d'interrogation (`g-bubble-q`) |
| « c'est décidé » | pastille `g-check` |
| « il faut que quelqu'un… » | drapeau `g-flag` avec un prénom en `tb` |
| des quantités (« trois fois plus ») | des tailles différentes, sans chiffres inventés |

## 3. Boucle d'une réunion

1. **Premier jet (moins de 30 secondes de réflexion)** : message en une phrase, famille de diagramme, 3 à 5 objets. Écrire `draft.svg`, composer, afficher.
2. **Retouches** : à chaque phrase de l'équipe, ajouter ou modifier un objet. Ne pas réécrire tout le fichier, éditer ses lignes.
3. **Cristalliser** : quand le sujet change, enregistrer l'état (copie `draft-1.svg`) puis repartir de la même base.
4. **Version propre** (une seule fois, à la fin ou sur demande) : réaligner, regrouper, ajouter titre et légende, exporter SVG et PNG.

Conventions de réunion à garder dans un coin du croquis, toujours au même endroit (bande de droite, x entre 1250 et 1560) :

| Pastille | Sens |
|---|---|
| `g-check` | décision prise |
| `g-bubble-q` | question ouverte |
| `g-bubble-bang` | risque |
| `g-flag` + prénom en `tb` | action et responsable |
| `g-sticky` | idée à garder |

## 4. Grille d'ancrage

Pour que les retouches restent stables, poser les objets sur une grille lâche (pas besoin d'être exact) :

- colonnes : x = 220, 520, 820, 1120 (la bande x > 1250 est réservée aux pastilles)
- rangées : y = 190, 430, 670
- titre : (800, 90), en `tl`

Un objet ajouté prend la case libre la plus proche de ceux auquel il se relie. Un objet supprimé laisse sa case vide jusqu'à la version propre.

## 5. Outils selon l'environnement

- **Claude Code** : éditer `draft.svg` et laisser `python3 scripts/live.py draft.svg` tourner. La page `http://localhost:8765` se met à jour dans la seconde (fondu léger), plein écran avec f. Aucune installation, bibliothèque standard uniquement. Pour partager l'écran, ouvrir cette page dans un onglet.
- **claude.ai** : générer le SVG composé, le rendre en PNG et l'afficher dans la conversation ; pour un affichage persistant, publier un artifact HTML qui contient le SVG et republier à chaque retouche (même artifact, mise à jour sur place).
- **Sans exécution de code** : écrire le SVG complet à chaque tour (il reste petit si on garde le budget de sept objets).

## 6. Recettes express

Chaque recette tient en 5 à 15 lignes avec `sketch.py` (exemples dans `examples/build_examples.py`).

- **Flux** : 3 à 5 `box` sur y = 430, `link` entre elles, étape discutée en `fh`.
- **Priorisation** : croix d'axes (deux `arrow`), quatre mots de quadrants en `tg`, éléments en `pill` placés à leur position.
- **Décision** : racine `f4`, deux enfants, feuilles en symboles (`g-check`, `g-cross`).
- **Cartographie d'acteurs** : hub central noir, personnes autour (`g-person`), liens `ink` pour les échanges forts, `gray` pour les faibles.
- **Écran à discuter** : `wf` (cadre, nav, image, texte, bouton), annotations bleues numérotées (`references/wireframes-flows.md`).
- **Avant et après** : deux zones, mêmes objets, flèche large ; si l'équipe veut manipuler, passer en Interactif.
- **Problème en une image** : une métaphore (`references/metaphores.md`) au centre, trois mots, une annotation bleue.

## 7. À éviter

- Réorganiser tout le schéma à chaque tour : l'équipe perd ses repères.
- Ajouter des détails que personne n'a mentionnés.
- Dépasser sept objets pour « faire complet ».
- Attendre la version parfaite : un croquis faux mais corrigeable en dix secondes vaut mieux qu'un croquis juste en deux minutes.
- Attribuer des phrases ou des prénoms à des personnes sans qu'elles l'aient dit.
