---
name: marker-sketch
description: Dessine n'importe quelle idée, description, flux, architecture, organisation, wireframe ou scène sous forme de croquis au feutre sur papier à points (SVG noir, blanc, gris, ombres portées, un accent rare), de façon rapide et toujours avec la même construction. Quatre modes, Croquis (réponse directe), Live (réunion, atelier, échange oral), Atelier (schéma dense, mise en page automatique), Interactif (évolution maintenant, ensuite, plus tard, éléments déplaçables, formes qui changent). À utiliser dès qu'on demande un schéma, diagramme, flow, croquis, sketch, illustration, wireframe, maquette rapide, carte mentale, vue d'ensemble dessinée, "montre-moi", "dessine", "visualise", "schématise", ou une illustration animée ou interactive d'une évolution. Utiliser même si l'utilisateur ne parle pas de style : ce style est le défaut.
---

# marker-sketch

Transformer une idée en croquis au feutre : trait noir épais légèrement tremblé, aplat gris décalé avec des stries de feutre, ombre portée grise, texte manuscrit court, papier à points. Le rendu est le même à chaque fois parce que le style vit dans un noyau fixe (`assets/template.svg`, `assets/glyphes.svg`) et que la réflexion suit toujours le même protocole. Rien ne se redessine de mémoire : on assemble.

## Chemins et dépendances

Dans les commandes, `${CLAUDE_SKILL_DIR}` est le dossier de cette skill (Claude Code le remplace tout seul). Dans claude.ai, si la variable apparaît telle quelle, utiliser le chemin relatif depuis le dossier de la skill copié dans l'environnement d'exécution (`scripts/compose.py`). Les fichiers de travail (`draft.svg`, `croquis.svg`) s'écrivent dans le dossier de travail, jamais dans la skill.

Dépendances : Python 3 suffit pour `compose.py` (le texte reste en `<text>` avec la police incorporée). `fonttools` convertit le texte en tracés (`--outline`, rendu identique partout), `playwright` avec Chromium produit les PNG de contrôle (`render.py`). Installation : `pip install fonttools playwright && playwright install chromium`. Si une dépendance manque et ne s'installe pas, livrer le SVG et dire que le contrôle visuel n'a pas été fait.

## 1. Choisir le mode en dix secondes

| Situation | Mode | Sortie | Temps visé |
|---|---|---|---|
| Question ou demande de schéma, réponse illustrée | **Croquis** (défaut) | un SVG | une seule génération |
| Réunion, atelier, échange oral, « montre ce qu'on vient de dire » | **Live** | un SVG 16:9 très lisible, retouché à chaque échange | quelques secondes par retouche |
| Schéma dense (plus de 10 objets), liens nombreux, rendu à contrôler | **Atelier** | SVG construit par script, PNG de contrôle | une minute |
| « Maintenant, ensuite, plus tard », « actuellement, demain », évolution, tendance, éléments à déplacer | **Interactif** | une page HTML autonome | une configuration JSON |

En cas de doute, partir en Croquis. Ne jamais utiliser three.js par défaut : il ne sert qu'en Atelier, pour fabriquer un symbole en perspective qui manque (voir `references/glyphes.md`, section 3D).

## 2. Protocole mental, toujours le même (avant de tracer)

Répondre mentalement à ces six questions, dans l'ordre. C'est ce qui garantit la cohérence, pas le talent.

1. **Message en une phrase.** Que doit comprendre le lecteur en trois secondes ? Cette phrase devient le titre, ou l'annotation bleue.
2. **Famille de diagramme.** Choisir dans `references/familles-diagrammes.md` (quinze familles : flux, boucle, arbre, ensembles, couches, hub, roue, courbe, matrice, réseau, scène, maquette, avant/après, frise, entonnoir).
3. **Métaphore éventuelle.** Si l'idée est abstraite (tension, croissance, dette, friction), chercher un objet physique qui porte la tension et qui se dessine en une dizaine de traits (`references/metaphores.md`). Sinon, rester sur la famille.
4. **Budget.** 5 à 9 objets, 40 % de blanc, textes de un à trois mots (une légende d'une phrase au maximum). En Live : 7 objets maximum.
5. **Hiérarchie d'encre.** Noir = le cœur du message (un seul objet plein noir, au plus). Gris = le contexte. Bleu stylo = annotations, flèches de commentaire, numéros. Un seul accent de remplissage par dessin (jaune surligneur, orange, rouge, bleu ciel ou sable), moins de 10 % de la surface, jamais pour décorer.
6. **Composition.** Lecture de gauche à droite et de haut en bas, un point focal, alignements sur une grille lâche, espace réservé aux annotations.

Puis écrire. Puis contrôler (section 8).

## 3. Règles de style non négociables

- Jamais de dégradé, jamais de contour fin et régulier, jamais d'ombre floue. Ombre = copie grise décalée de (-7, 10).
- Trois gris + noir + papier : `f1` clair, `f2` moyen, `f3` foncé, `f4` noir plein.
- Flèches ouvertes en V (classes `arr`, `arrb`, `arrg`), courbes en S plutôt que coudes à angle droit.
- Flux gris pointillé large (`flow`), périmètres noirs en petits points (`dotk`), tirets (`dash`).
- Texte : police Patrick Hand, classes `t` (36), `tl` (52, titres), `ts` (27, mini), `tb` (bleu), `tg` (gris), `tw` (blanc sur noir). Français soigné : accents sur les majuscules, œ, guillemets « », pas de tiret long, apostrophe courbe ’.
- Les mots sont ceux du lecteur. Pas de jargon inventé, pas de phrases.
- Pas d'emoji, pas de logo de marque, pas de personnage protégé.

Valeurs numériques exactes, couleurs et cas particuliers : `references/grammaire-visuelle.md`.

## 4. Mode Croquis : écrire directement

Le dessin brut ne contient que le contenu. Le noyau de style est ajouté par `compose.py`.

Pattern d'un objet (quatre couches, même `id` partagé) :

```svg
<use href="#a1" x="-7" y="10" class="sh"/>        <!-- ombre -->
<use href="#a1" class="pp"/>                       <!-- papier opaque -->
<use href="#a1" x="-2.5" y="2.5" class="f1"/>     <!-- aplat décalé -->
<g class="ink"><path id="a1" d="M300 300 L560 296 L556 420 L296 424 L302 296"/></g>
<text class="t" x="430" y="372">Idée</text>
```

Les angles dépassent légèrement (le tracé ne se referme pas exactement), les côtés ne sont jamais parallèles au pixel près. Pour les symboles (personne, fenêtre, base de données, nuage, loupe...), utiliser la bibliothèque :

```svg
<use href="#g-person" x="540" y="260" class="cb"/>   <!-- classes de teinte: cb co cr cs ch c1 c3 c4 -->
```

Catalogue : `python3 ${CLAUDE_SKILL_DIR}/scripts/compose.py --catalog` ou `references/glyphes.md`. Planche visuelle : `references/planche-symboles.png`.

Assemblage et contrôle :

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/compose.py draft.svg -o croquis.svg --outline      # papier, points, filtres, texte en tracés
python3 ${CLAUDE_SKILL_DIR}/scripts/check.py draft.svg                                  # budget, accents, symboles, accents de couleur
python3 ${CLAUDE_SKILL_DIR}/scripts/render.py croquis.svg                               # PNG de contrôle (Chromium)
```

Options de `compose.py` : `--paper cream|white|kraft|yellow|blue`, `--no-dots`, `--transparent` (pour glisser dans une slide), `--size 1200x1200`, `--embed-font` (garde le texte éditable), `--title`.

Sans exécution de code (conversation simple dans claude.ai) : copier le bloc `<defs>` de `assets/template.svg` tel quel, y coller les seuls symboles utilisés depuis `assets/glyphes.svg`, puis le contenu dans `<g id="drawing" filter="url(#wob)">`. Dire explicitement que le contrôle visuel n'a pas pu être fait.

## 5. Mode Live : réunion, atelier, oral

Lire `references/mode-live.md` avant la première retouche. L'essentiel :

- Écouter, ne pas rédiger. Extraire de l'échange 3 à 7 éléments : les noms deviennent des objets, les verbes des flèches, « mais » et « sinon » des branches, « avant/après » deux colonnes, « d'abord, puis » un flux.
- Format 16:9, texte minimum 36 px (`t`), titres 52 px (`tl`), jamais `ts`. Lisible à quatre mètres.
- **Positions stables.** À chaque retouche, ne déplacer que ce qui change. Réutiliser les mêmes identifiants et coordonnées. L'équipe ne doit pas perdre ses repères.
- Retouches orales : « ajoute », « relie », « barre », « mets en avant » (noir plein ou surligneur), « version propre » (réaligner, une seule fois à la fin).
- Projection : `python3 ${CLAUDE_SKILL_DIR}/scripts/live.py draft.svg` ouvre une page qui se met à jour seule à chaque réécriture du fichier (plein écran avec la touche f). Dans claude.ai : republier le même artifact ou rendre le SVG en PNG à chaque retouche.
- Maquettes et flows en direct : recettes dans `references/wireframes-flows.md`.

## 6. Mode Atelier : schémas denses construits par script

Pour plus de dix objets ou beaucoup de liens, écrire quelques lignes avec `scripts/sketch.py` : les liens se calculent aux bords des objets, courbes en S et flèches ouvertes comprises.

```python
import sys; sys.path.insert(0, "${CLAUDE_SKILL_DIR}/scripts")
from sketch import Sketch
s = Sketch()
s.box("a", 260, 420, "Explorer", fill="f1")        # (id, centre x, centre y, texte)
s.box("b", 800, 420, "Définir", fill="fh")
s.glyph("c", "g-flag", 1340, 400, "Livrer")
s.link("a", "b"); s.link("b", "c", label="valider")
s.perimeter(["a", "b"], "Discovery")
s.note(1330, 640, "on mesure ici", target="c")
s.save("draft.svg")
```

Objets : `box` (formes `box`, `pill`, `oval`, option `solid=False` pour les ensembles qui se chevauchent), `glyph`, `text`, `label`, `wf` (éléments de maquette), `badge` (numéro bleu). Liens : `link(kind="ink|gray|flow|dash|blue|line")`, `arrow`, `perimeter`, `note`, `highlight`, `raw` (SVG libre). Exemples complets dans `examples/build_examples.py`.

Pour une mise en page automatique d'un graphe volumineux, calculer les positions avec ELK ou dagre (npm), puis passer les coordonnées à `sketch.py`.

## 7. Mode Interactif : évolution dans le temps

Quand la demande parle d'évolution, d'états successifs, de « maintenant, ensuite, plus tard », d'un changement de tendance, d'une organisation qui se transforme, de pièces à déplacer : produire une page HTML autonome. Lire `references/interactif.md` (six patrons, schéma de la configuration, pièges).

Principe : un dessin brut (les éléments ont un `id`) + une configuration JSON (états, images clés par élément : `x y s r o d draw txt`, couches, notes) :

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/compose.py draft.svg --interactive scenes.json -o page.html
python3 ${CLAUDE_SKILL_DIR}/scripts/render.py page.html --state 1        # contrôler chaque état
```

La page offre : boutons d'états, curseur de temps, lecture, couches à afficher ou masquer, glisser-déposer des éléments marqués `drag`, double-clic pour renommer un texte, liens qui suivent les éléments, export de l'état en SVG, copie de la disposition (JSON), clavier (flèches, espace, f). Aucune dépendance, fonctionne hors ligne. Exemples : `examples/migration-organisation.html`, `examples/tendance-adoption.html`.

## 8. Contrôle avant de répondre

1. `check.py` sans erreur (symboles connus, tirets longs absents, un seul accent de couleur).
2. Rendu PNG regardé : texte lisible, rien ne se chevauche, ombres visibles, point focal évident, blanc suffisant.
3. Le message tient en une phrase en regardant le dessin sans lire le texte.
4. Si un contrôle visuel est impossible, le dire.

## 9. Livrer selon l'environnement

- **Claude Code** : écrire `croquis.svg` (et le PNG) dans le dossier de travail, donner le chemin. En Live, lancer `live.py`.
- **claude.ai avec exécution de code** : générer, contrôler, envoyer le SVG et le PNG. Pour une page interactive ou un dessin à garder et partager, publier en artifact (charger d'abord la skill `artifact-design`, titre de deux à quatre mots) ; le HTML produit par `compose.py --interactive` est déjà autonome.
- **Sans exécution** : SVG complet écrit à la main selon la section 4, annoncé comme non contrôlé.

Réponses en français : appliquer `francais-parfait` aux libellés du dessin comme au texte autour.

## 10. Index des références

| Fichier | Quand le lire |
|---|---|
| `references/grammaire-visuelle.md` | valeurs exactes du style, classes, papiers, cas limites |
| `references/familles-diagrammes.md` | choisir et composer une des quinze familles |
| `references/metaphores.md` | idée abstraite à rendre visible |
| `references/glyphes.md` | catalogue des 47 symboles, ajouter un symbole, 3D optionnelle |
| `references/mode-live.md` | réunion, atelier, oral |
| `references/wireframes-flows.md` | maquettes, parcours, états d'écran |
| `references/interactif.md` | pages animées, états, éléments déplaçables |
| `references/planche-symboles.png` | aperçu de tous les symboles |
| `examples/` | six croquis (SVG et PNG), deux pages interactives, `brut/` (dessins sources et configurations), `build_examples.py` |
