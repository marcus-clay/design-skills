# Grammaire visuelle

Tout ce qui définit le rendu « feutre sur papier à points ». Les valeurs ci-dessous sont déjà codées dans `assets/template.svg` : ce fichier explique le pourquoi et les cas limites. Ne pas retoucher les valeurs, composer avec.

## 1. Le trait

| Élément | Valeur | Classe |
|---|---|---|
| Contour principal | noir `#161616`, 4,2 px, bouts et jonctions arrondis | `ink` |
| Contour intermédiaire | 3,2 px | `mid` |
| Détail fin (lignes de texte simulées, croix d'image) | 2,4 px | `fine` |
| Contour de contexte | gris `#80838a`, 3,6 px | `inkg` |
| Annotation | bleu stylo `#2547a8`, 3,4 px | `inkb` |
| Flux | gris `#8e9198`, 10 px, pointillé `.1 22 .1 30 .1 16 .1 34` | `flow` |
| Périmètre | noir, 5,5 px, points espacés de 17 px | `dotk` |
| Tirets | noir, 3,2 px, `16 12` | `dash` |
| Surligneur | gris `#b3b6bc`, 10 px, filtre feutre | `hl` |

Le tremblé n'est pas dessiné à la main : un filtre `#wob` (deux échelles de bruit, ondulation large de 7,5 px et grain fin de 2,6 px) est appliqué au groupe racine `#drawing`. Tout ce qui est dans ce groupe tremble de la même façon, d'où la cohérence. Conséquence : ne pas placer d'élément qui doit rester parfaitement droit (une règle, un cadre de slide) dans `#drawing`.

Dans le tracé lui-même, quatre habitudes à garder : les angles dépassent (le contour ne se referme pas à l'angle exact), les côtés d'un rectangle ne sont pas parallèles au pixel près, les cercles ne se referment pas parfaitement, les lignes ont un très léger arc. `sketch.py` et `build_glyphs.py` les produisent automatiquement.

## 2. Les objets à quatre couches

Dans cet ordre, avec le même `id` de géométrie :

1. **Ombre** : copie grise `#c6c9ce`, décalée de (-7, 10), classe `sh`.
2. **Papier** : copie opaque de la couleur du papier, classe `pp`. Elle empêche l'ombre de se voir à travers un objet et masque ce qui est derrière.
3. **Aplat** : copie décalée de (-2,5, +2,5) par rapport au contour, classe `f1` à `f4` ou accent. Le décalage entre aplat et contour est la signature du feutre qui déborde.
4. **Contour** : `<g class="ink"><path id="…" d="…"/></g>`. Le tracé porte l'`id`, le groupe porte le style, ce qui permet aux copies `use` de surcharger le remplissage.

Les stries horizontales du feutre viennent du filtre `#mk` (bruit étiré à l'horizontale transformé en masque d'opacité). `f4` (noir plein) n'a pas de filtre : le noir plein reste plein.

Sans ombre ni papier (`solid=False` dans `sketch.py`) : formes qui doivent se superposer et rester transparentes (Venn, zones, halos).

## 3. Les gris et l'encre

| Niveau | Couleur | Usage |
|---|---|---|
| `f1` | `#d6d8dc` | zone neutre, fond d'objet, contexte |
| `f2` | `#a4a7ad` | objet secondaire, couche intermédiaire |
| `f3` | `#6f737d` | objet important mais non central (texte blanc dessus) |
| `f4` | `#1c1c1e` | le seul élément qui doit attirer l'œil en premier (texte blanc `tw`) |

Hiérarchie d'encre : **noir** = le cœur, **gris** = le contexte, **bleu stylo** = ce que l'auteur ajoute en commentaire (flèche d'annotation, numéro, mot en marge). L'œil doit lire le noir en premier, le gris ensuite, le bleu en dernier.

## 4. Accents de couleur

Un seul accent de remplissage par dessin, sous 10 % de la surface, pour marquer un point précis (l'intersection d'un Venn, l'étape clé, l'élément à décider).

| Classe de remplissage | Couleur | Quand |
|---|---|---|
| `fh` | surligneur `#dde37c` | défaut : « regardez ici » |
| `fb` | bleu ciel `#2f93d8` | information, eau, données |
| `fo` | orange `#ef7c1f` | énergie, attention, mouvement |
| `fr` | rouge `#d9473c` | alerte, blocage, erreur |
| `fs` | sable `#c79b62` | matière, carton, terre |

Pour teinter un symbole de la bibliothèque : classe `cb co cr cs ch` (même palette), `c1 c3 c4` (gris). Le bleu stylo des annotations ne compte pas comme accent.

## 5. Le texte

Police Patrick Hand (OFL), pile de repli manuscrite. Un à trois mots par étiquette. Pas de phrase dans un objet ; une légende d'une phrase au plus, en `tb` (bleu) ou `tg` (gris), posée en marge. Tailles : `tl` 52 titre, `t` 36 courant, `ts` 27 mini (jamais en Live), `tb` 32 annotation bleue, `tg` 32 gris, `tw` 36 blanc sur noir. Alignement : `l` (à gauche) et `r` (à droite) ; centré par défaut. Multilignes : `<tspan x y>` avec 1,1 fois la taille de police entre les lignes. Les apostrophes sont courbes (’), jamais droites.

Largeur estimée d'un texte en `t` : environ 17 px par caractère. Une boîte qui contient un mot de 10 lettres fait au moins 240 px de large.

## 6. Le papier

| Papier | Fond | Points | Usage |
|---|---|---|---|
| `cream` (défaut) | `#f3f2ee` | `#b8b8b2` | tout usage |
| `white` | `#fbfbfa` | `#c4c4bf` | impression, document clair |
| `kraft` | `#e7dcc6` | `#a79c86` | atelier, ton chaleureux |
| `yellow` | `#e4e98a` | `#5f8a2c` | carnet, accent fort, un schéma isolé |
| `blue` | `#dfe9ee` | `#9fb0ba` | ton technique, données |

Points : cercles de 1,7 px, pas de 44 px. `--transparent` retire papier et points pour glisser le dessin dans une slide ou une page. Le papier a toujours sa couleur propre : la couche `pp` des objets s'y adapte.

## 7. Deux supports

- **Papier** (défaut) : tout ce qui précède.
- **Tablette** (variante, à demander explicitement) : mêmes objets, mais surlignage par larges bandes grises translucides à la place des aplats décalés, fond blanc ou très clair. Obtenir l'effet en remplaçant `f1`/`f2` par `hl` élargi (stroke 24 à 40) et en retirant `--paper`. Ne pas mélanger les deux supports dans un même dessin.

## 8. Échelle et densité

Canevas par défaut 1600 × 900 (16:9). Autres formats : `--size 1200x1200` (carré), `--size 1080x1350` (portrait de post), `--size 1600x1000`. Marges de sécurité : 60 px. Un objet principal fait de 200 à 380 px de large, un symbole de 100 à 230 px, un texte de 36 px. Si on est tenté de passer à 22 px pour tout faire tenir, c'est qu'il y a trop d'objets : retirer ou découper en deux croquis.

## 9. Ce qui casse le style (liste de contrôle)

- Un trait de largeur uniforme et parfaitement droit hors du filtre.
- Une ombre floue, un dégradé, une transparence qui laisse voir l'ombre à travers l'objet.
- Plus d'un accent de remplissage, ou un accent utilisé en décor.
- Du texte en police système sans le noyau de style (rendu serif ou sans-serif propre).
- Des flèches pleines ou des coudes à angle droit à la règle.
- Des objets alignés au pixel et de même taille partout (un schéma trop « propre » perd le côté croquis : varier légèrement les tailles, ne pas aligner mécaniquement les centres).
- Un dessin rempli à plus de 60 %.
