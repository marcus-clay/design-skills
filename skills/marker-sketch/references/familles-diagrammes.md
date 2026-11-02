# Les quinze familles de diagrammes

Choisir une famille avant de dessiner. Chaque fiche donne : quand l'utiliser, comment composer, symboles utiles, piège. Les coordonnées sont pour un canevas 1600 × 900. L'exemple de code utilise `sketch.py`.

| # | Famille | Question à laquelle elle répond |
|---|---|---|
| 1 | Flux linéaire | Dans quel ordre, avec quelles étapes ? |
| 2 | Boucle, cycle | Qu'est-ce qui se répète, où est le retour ? |
| 3 | Arbre, organigramme, décision | Qui dépend de qui, quelle branche choisir ? |
| 4 | Ensembles (Venn) | Où est l'intersection qui compte ? |
| 5 | Couches, pile | Sur quoi repose quoi ? |
| 6 | Hub et rayons | Qu'est-ce qui est au centre, qui s'y relie ? |
| 7 | Roue segmentée | Quelles parts d'un tout, quelles dimensions ? |
| 8 | Courbe et axes | Comment ça évolue, où est le seuil ? |
| 9 | Matrice 2 × 2 | Comment classer, quoi prioriser ? |
| 10 | Réseau, graphe | Comment les éléments s'influencent-ils ? |
| 11 | Scène d'objets | À quoi ressemble la situation, qui est là ? |
| 12 | Maquette d'interface | Quel écran, quel parcours ? |
| 13 | Avant, après | Qu'est-ce qui change ? |
| 14 | Frise, branches | Quand, avec quelles bifurcations ? |
| 15 | Entonnoir, pyramide | Où perd-on ou gagne-t-on en passant d'un niveau à l'autre ? |

## 1. Flux linéaire
- **Composition** : 3 à 5 étapes sur une ligne horizontale à y = 420, centres espacés de 400 à 540 px. Étape clé en `f4` ou `fh`, autres en `f1` ou blanc. Une icône (symbole) au-dessus de chaque étape (y = 190) si le sens le demande, jamais les deux sur chaque étape.
- **Liens** : flèches noires ouvertes entre les étapes, libellé de trois mots au plus au-dessus. Un retour ou une boucle en `flow` gris pointillé sous la ligne (voir `examples/parcours-discovery`).
- **Piège** : plus de cinq étapes en ligne devient illisible, passer en deux rangées en S ou regrouper par phase avec un périmètre `dotk`.

## 2. Boucle, cycle
- **Composition** : 3 à 5 nœuds sur un cercle de rayon 260 centré en (800, 450), flèches courbes entre eux, un mot au centre. Nœud de départ marqué (noir plein).
- **Piège** : les flèches doivent tourner dans un seul sens. Un cycle à plus de cinq nœuds se lit mal : fusionner.

## 3. Arbre, organigramme, décision
- **Composition** : racine en haut centrée (noire pleine pour une décision), niveaux espacés de 240 px, nœuds de même niveau alignés à peu près (pas au pixel). Feuilles = symboles avec libellé dessous (`g-check`, `g-cross`, `g-bolt`, `g-clock`). Libellés « oui » et « non » sur les liens, côté extérieur (voir `examples/arbre-decision`).
- **Piège** : trois branches par nœud au maximum, sinon passer en matrice ou en liste.

## 4. Ensembles (Venn)
- **Composition** : deux ou trois cercles de 400 px de diamètre, sans ombre ni papier (`solid=False`), chevauchement d'environ 100 px. Libellés dans la partie exclusive de chaque cercle (`tl`). Un seul accent (`fh`) sur l'intersection qui compte, annotation bleue avec flèche (voir `examples/venn-produit`).
- **Piège** : ne pas remplir tous les cercles de gris : les superpositions deviennent illisibles.

## 5. Couches, pile
- **Composition** : 3 à 5 rectangles larges (640 × 110) empilés à 190 px d'écart, du plus visible (haut) au plus profond (bas), gamme de gris `f1` à `f3` pour exprimer la profondeur, flèches grises courtes entre couches. Acteurs et services externes sur les côtés avec symboles (`g-person`, `g-cloud`, `g-db`). Périmètre pointillé autour de ce qui est « à nous » (voir `examples/architecture-assistant`).
- **Piège** : ne pas mélanger l'axe vertical « abstraction » et un autre axe.

## 6. Hub et rayons
- **Composition** : un objet central (noir plein ou grand symbole), 4 à 7 satellites à distance régulière mais pas parfaite, liens de longueurs différentes, libellé sous chaque satellite. Satellite à relier en priorité plus proche ou plus gros.
- **Piège** : au-delà de sept satellites, regrouper (second niveau en `inkg`).

## 7. Roue segmentée
- **Composition** : un grand cercle découpé en 4 à 8 parts par des traits depuis le centre, un mot par part, une part mise en avant (`fh` ou noir). Titre au centre (`tl`).
- **Piège** : les parts ne représentent des proportions que si elles sont dessinées proportionnelles. Sinon préciser « sans échelle ».

## 8. Courbe et axes
- **Composition** : axes noirs à flèches ouvertes (origine (200, 740)), une courbe épaisse (6 px), un seuil en tirets gris avec légende grise, un point marqué (`g-target` à demi-échelle), une annotation bleue pour la rupture de pente (voir `examples/tendance-adoption`). Titres d'axes en `ts`.
- **Piège** : pas de graduations ni de chiffres inventés. Si les données sont réelles, les chiffres viennent de la source, jamais d'une estimation.

## 9. Matrice 2 × 2
- **Composition** : deux axes en croix, quatre quadrants nommés (un mot chacun), un axe annoté à chaque extrémité (« faible » à « fort »), éléments posés comme des pastilles (`box` en `pill`) à leur position réelle, le quadrant cible en `fh`.
- **Piège** : les deux axes doivent être indépendants. Nommer chaque axe par un critère mesurable.

## 10. Réseau, graphe
- **Composition** : 6 à 10 nœuds (`oval` ou petite personne `g-person-sm`) de tailles différentes selon l'importance, liens gris par défaut, liens importants en noir, un nœud pivot en noir plein. Pour plus de dix nœuds, calculer les positions avec ELK, dagre ou d3-force.
- **Piège** : les croisements de liens se résolvent en déplaçant des nœuds, pas en compliquant les liens.

## 11. Scène d'objets
- **Composition** : un objet central grand (écran, tableau, bureau), 2 à 4 personnes ou objets autour, un ou deux accessoires qui racontent le moment (bulle, ampoule, post-it, tasse), une annotation bleue. Les personnages sont des symboles anonymes (aucune ressemblance, aucun personnage protégé). Voir `examples/scene-atelier`.
- **Piège** : sans accessoire qui raconte quelque chose, c'est un décor : ajouter l'objet qui porte l'idée.

## 12. Maquette d'interface
- **Composition** : écrans à hauteur égale (640 px), 3 écrans maximum par croquis, éléments en blocs gris avec croix pour les images, traits pour le texte, un seul bouton principal noir par écran, flèches entre écrans, pastilles bleues numérotées pour les annotations. Détail dans `wireframes-flows.md` et `examples/wireframe-parcours`.
- **Piège** : ne pas écrire de vrai texte dans les blocs, sauf titres et boutons (la maquette discute de structure, pas de copie).

## 13. Avant, après
- **Composition** : deux zones côte à côte séparées par une flèche large (`g-arrow-block`) ou une ligne `dotk`, mêmes objets dans les deux zones pour que la différence saute aux yeux, la zone « après » avec l'accent. Titres `tl` « Avant » et « Après » ou « Maintenant » et « Demain ».
- **Variante vivante** : en mode Interactif, les objets se déplacent d'une zone à l'autre (`references/interactif.md`, patron 2).
- **Piège** : ne dessiner que ce qui change, le reste en gris.

## 14. Frise, branches
- **Composition** : ligne de temps horizontale (y = 450) avec 4 à 6 jalons, bifurcations en courbes en S vers le haut ou le bas, dates en `tg`, jalon actuel en noir plein, jalons futurs en pointillé `dash`.
- **Piège** : ne pas échelonner les jalons à intervalle égal si les durées sont inégales sans le dire.

## 15. Entonnoir, pyramide
- **Composition** : 3 à 5 niveaux de largeur décroissante (trapèzes ou bandes) empilés, un mot et éventuellement un chiffre sourcé par niveau, la fuite principale annotée en bleu. Pyramide : même logique, sommet noir.
- **Piège** : les largeurs doivent être proportionnelles aux chiffres si on en affiche.

## Combiner
Une famille principale, une famille secondaire au plus (par exemple un flux avec une matrice en vignette). Si on a envie d'en combiner trois, c'est deux croquis.
