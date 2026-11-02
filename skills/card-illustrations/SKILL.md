---
name: card-illustrations
description: Use when asked for an illustration, a thumbnail or a card picture for a card in a grid of content, such as a library of resources (guide, template, deck, article), when a set of cards needs one consistent treatment, or when product screenshots are shared as a reference for card illustrations. Two modes, "noir et blanc" (ink accent) or "accent couleur" (ten-hue palette), chosen by the argument or the wording of the request.
---

# Illustrations de cartes

## L'idée

Une carte montre la chose elle-même, simplifiée à ce dont le lecteur a besoin, cadrée avec intention, et chaque annotation a une raison. Un fragment d'interface ou de document, à plat, grand, sur un fond gris clair ; autour, quelques notes techniques en monospace reliées par un filet. On doit comprendre la ressource sans lire le texte de la carte.

## Le vocabulaire

Chaque scène se compose de trois à cinq de ces pièces, jamais toutes.

Références visuelles, à regarder avant de dessiner une scène :
- `references/vocabulaire.png` (et `.svg`) : les douze pièces, chacune isolée sur son panneau, avec sa règle en une ligne.
- `references/exemple-noir-et-blanc.png` et `references/exemple-accent-couleur.png` (et `.svg`) : la même scène complète dans les deux modes. Seule la couleur de l'élément accentué change.
- `references/accent-palette.png` et `.json` : les dix teintes de la palette, avec leur version douce.

| Pièce | Ce que c'est |
|---|---|
| **Fond** | Panneau gris clair (`#F3F3F2` à `#F5F5F4`), coins 16 à 24 px, format 13:10. Ni ombre, ni bord marqué. |
| **Scène** (stage) | Rectangle en pointillé `gray-300`, avec une grille très pâle à l'intérieur : la zone de travail. Optionnelle, pour dire « ceci est un espace de conception ». |
| **Fenêtre** | Fenêtre blanche, barre de titre à trois points gris, filet `gray-200`, ombre douce. Elle **déborde** de la scène ou du panneau (coupée à droite ou en bas) : le cadrage est volontaire. Barre d'adresse si l'URL compte. |
| **Squelette** | Le texte secondaire en barres grises arrondies (`gray-200`), les lignes de liste séparées par un filet, les avatars en disques gris. Seul l'élément qui porte le sens a de vrais mots (« Share », « Publish »). |
| **Pile** | Plusieurs cartes empilées avec un léger décalage vertical, seul le haut de chacune visible (un nom de fichier, un titre) ; celle du dessus est entière avec titre et paragraphe. Pour montrer un ensemble de documents. |
| **Popover** | Petite carte blanche qui chevauche le bord de la fenêtre (un montant, une rangée de cases), ombre plus marquée que la fenêtre : elle est au-dessus. |
| **Annotation** | Texte monospace `gray-500`, 11 à 13 px, posé **hors** de l'objet : un attribut (`data-target="share"`), un état (`{ open: false }` dans une petite carte), un chemin de fichier, une décision. Elle nomme ce que l'image montre, en langage d'atelier. |
| **Filet de rappel** | Ligne fine `gray-400` qui part de l'annotation et finit sur l'élément par un point plein de 4 px. Droite, ou une seule courbe douce. Une flèche pointillée pour un retour. |
| **Frise d'étapes** | Ligne horizontale avec des cercles creux et un label monospace sous chacun ; l'étape en cours est pleine. Pour situer la ressource dans un processus. |
| **Planche contact** | Grille de petites vignettes numérotées (`01` à `06`), une seule sélectionnée, reliée par un filet à sa version agrandie. Pour une série dont on regarde un élément. |
| **Cote** | Une mesure dessinée (trait, deux butées, « 4px »), comme sur une maquette annotée. Pour un détail de précision. |
| **Pastilles numérotées** | Disques pleins 1, 2, 3 posés sur les éléments, dans l'ordre de lecture. Avec un curseur si une action est en cours. |

## Deux modes

La skill se lance dans l'un de deux modes, qui ne changent qu'une chose : la couleur de l'unique élément accentué. Fond, surfaces, squelette, annotations, composition et gestes restent identiques.

| Mode | Comment l'appeler | L'élément accentué |
|---|---|---|
| **Noir et blanc** | `/card-illustrations noir et blanc`, « en noir et blanc », « monochrome », « sans couleur » | encre `gray-900` pleine (texte blanc dessus) |
| **Accent couleur** | `/card-illustrations accent`, « avec couleur d'accent », « en couleur » | une teinte de la palette, tirée d'un identifiant stable |

Choix du mode : l'argument ou les mots de la demande d'abord. Sans indication, reprendre le mode des scènes déjà en ligne pour que la bibliothèque reste homogène ; s'il n'y en a pas, noir et blanc. Ne jamais mélanger les deux modes dans une même grille : changer de mode, c'est repasser toutes les cartes visibles ensemble. Dans le code, le mode est une seule constante (`ACCENT_MODE: 'ink' | 'color'`) lue par toutes les scènes, pour basculer la bibliothèque en une ligne.

## L'accent : du gris, et une touche de couleur (mode accent couleur)

La scène reste grise (fond, surfaces blanches, squelette, annotations). **Un seul élément** porte une couleur d'accent : l'étape en cours, la vignette choisie, la cote, la case cochée, le bouton principal, l'élément retenu. Tout le reste est gris ou encre. L'accent réservé aux illustrations laisse l'interface du site (boutons, liens, navigation) monochrome.

La palette compte dix teintes à **la même luminosité et la même saturation** en OKLCH (L 0,655, C 0,11), seule la teinte change. C'est le réglage le plus vif qui garde les dix couleurs dans le gamut sRGB et à 3:1 au moins sur blanc (seuil des éléments graphiques). Chaque teinte a une version douce (L 0,95, C 0,03) pour une pastille teintée ou un fond léger. Nuancier dans `references/accent-palette.png`, valeurs dans `references/accent-palette.json`.

| Nom | Accent | Doux |
|---|---|---|
| rouge | `#CB756E` | `#FFE7E4` |
| corail | `#C87A56` | `#FFE9DE` |
| orange | `#BF8242` | `#FDEBDA` |
| ambre | `#AF8B37` | `#F8EDD8` |
| vert | `#63A266` | `#E3F4E2` |
| émeraude | `#42A680` | `#DDF5E9` |
| turquoise | `#0DA5A5` | `#D8F5F5` |
| ciel | `#389DC7` | `#DBF3FF` |
| bleu | `#6B90D4` | `#E4EFFF` |
| violet | `#9284CE` | `#EEEBFF` |

Règles d'emploi :
- **Une teinte par scène**, choisie au hasard mais de façon stable : une fonction `accentFor(id)` tire la teinte de l'identifiant de la ressource (un hachage simple), pour obtenir la même couleur au serveur et au navigateur, sans erreur d'hydratation. Ne pas tirer avec `Math.random()`.
- Sur un accent plein, le texte est blanc et en gras (11 px minimum) ; sur un fond doux, le texte prend l'accent plein.
- Jamais deux teintes dans la même scène, jamais de dégradé entre teintes. Une barre de disponibilité verte et orange reste une exception où la couleur est le sujet.
- Ton de référence : une planche d'éléments d'interface où l'onglet actif est teinté, le bouton principal plein, la case cochée colorée et le curseur d'une teinte vive sur un fond quadrillé gris, en plus doux.

Ajouter une teinte : la calculer à L 0,655 et C 0,11, vérifier qu'elle est dans le gamut sRGB et à 3:1 sur blanc, puis la placer entre ses voisines de teinte.

## Composition

- L'objet à gauche ou au centre, les annotations à droite ou dessous, jamais par-dessus le contenu.
- Le cadrage coupe : une fenêtre qui déborde du panneau se lit plus grande et plus réelle qu'une fenêtre entière réduite.
- Marges du panneau généreuses (8 à 10 %) ; trois à cinq pièces ; si on hésite à en ajouter une, on ne l'ajoute pas.
- Lisible à la taille de la carte (environ 350 px de large) : texte 11 px minimum, monospace compris.
- Polices : une police sans empattement pour l'interface simulée, monospace système (`ui-monospace`, `font-mono`) pour les annotations seulement.

## Ce que la scène doit montrer

Le fragment dit ce que la ressource **est** et à quoi elle sert, sans montrer sa mécanique interne. Un atelier d'intelligence collective se montre par son tableau (post-it de plusieurs mains, le post-it retenu avec ses votes), plutôt que par son découpage horaire ; une checklist par ses cases cochées ; un rituel par ses deux réunions sur la semaine. Si le fragment demande une explication pour être compris, c'est le mauvais fragment. Les annotations précisent, elles ne rattrapent pas une image floue.

## Au survol

Un seul geste par scène, qui dit ce que fait le document : une case se coche, la pastille suivante se remplit, le popover se soulève, la vignette suivante se sélectionne. Transform et opacité, 300 ms, une courbe d'accélération douce, appareils à pointeur seulement, quelques pixels au plus.

## Mise en œuvre (React et Tailwind)

- Un composant par panneau (le fond) et un composant par scène, choisi par l'identifiant de la ressource.
- Quelques briques partagées par toutes les scènes : une surface (carte blanche, ombre douce), une pastille, une barre de squelette, les constantes de geste au survol (durée, déplacement).
- La même fonction de rendu alimente la grille, les cartes « pour continuer » et les carrousels.
- La page de détail d'une ressource peut s'ouvrir sur la chose elle-même (diagramme d'un modèle, slides d'un deck) plutôt que sur sa vignette.

## Ajouter une ressource

1. Une phrase : quel fragment représente la ressource, quel est l'unique élément qui prend la couleur, quelle annotation (au plus deux) le nomme.
2. Choisir trois à cinq pièces du vocabulaire. Écrire la scène en HTML et Tailwind, positionnée en pourcentages du panneau, les mots dans un dictionnaire par langue (espaces insécables en français).
3. L'ajouter au sélecteur de scènes, avec son geste au survol.
4. Capturer la grille à 1280 px en 2x et à 390 px, au repos et au survol. Vérifier : lisible à la taille de la carte, une seule couleur sur un seul élément, annotations hors de l'objet, rien de coupé sans intention.

## Ce qui a été écarté

- Feuilles isométriques « papier » : elles se lisent comme du matériel.
- Vignettes d'un diagramme réduit : texte illisible, trop d'éléments.
- Découpage horaire pour un atelier : il montre la mécanique, pas la chose.
- Dégradés, plusieurs couleurs dans une scène, couleurs saturées hors de la palette.
