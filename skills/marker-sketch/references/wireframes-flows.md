# Maquettes et parcours

Pour discuter de structure, pas de pixels. Une maquette au feutre sert à décider ce qu'il y a sur l'écran, dans quel ordre, avec quelle action principale. Elle ne sert ni à valider les couleurs ni à écrire la copie.

## 1. Éléments (méthode `wf` de `sketch.py`)

Coin haut gauche (x, y), largeur, hauteur.

| `kind` | Rendu | Paramètres utiles |
|---|---|---|
| `frame` | cadre d'écran avec ombre, titre au-dessus | `label` = « 1. Accueil » |
| `nav` | barre grise avec trois points | |
| `title` | titre manuscrit ou trait épais | `label` |
| `image` | rectangle gris barré d'une croix | `fill` pour changer le gris |
| `text` | lignes de texte simulées (une par 26 px de hauteur) | |
| `input` | champ arrondi, libellé gris | `label` = « Rechercher » |
| `button` | pastille noire, texte blanc ; `fill="f1"` pour un bouton secondaire | `label` |
| `card` | carte avec lignes | `fill` |
| `avatar` | rond gris | |

Un écran mobile : cadre 360 × 640. Un écran bureau : cadre 640 × 400, ou le symbole `g-browser`. Trois écrans mobiles tiennent côte à côte (x = 130, 620, 1110). Quatre écrans : réduire à 280 × 500.

```python
s.wf("e1", "frame", 130, 150, 360, 640, "1. Accueil")
s.wf("n1", "nav", 150, 170, 320, 50)
s.wf("i1", "image", 170, 320, 280, 170)
s.wf("b1", "button", 170, 660, 280, 70, "Commencer")
s.link("e1", "e2", label="ouvrir")          # le lien relie les cadres
```

Modèle complet : `examples/wireframe-parcours.svg`.

## 2. Règles de lecture

- Un **bouton principal noir** par écran, jamais deux. Les actions secondaires en `f1`.
- Les images sont des rectangles barrés, jamais des dessins. Les avatars des ronds.
- Pas de vrai texte dans les blocs de contenu : des lignes. Seuls titres, boutons et libellés de champs portent des mots.
- Densité réaliste : si l'écran contient plus de sept blocs, le découper en deux écrans.
- Ordre de lecture identique à l'écran réel : haut, milieu, bas.

## 3. Annotations

Le dessin pose les questions, les annotations y répondent. Stylo bleu uniquement.

- **Numéro** : `s.badge(cx, cy, 1)` posé sur l'élément, avec la légende numérotée à droite ou en dessous, en `tb`.
- **Commentaire direct** : `s.note(x, y, "un seul appel à l'action", target="b3")`.
- **Décision à prendre** : bulle `g-bubble-q` à côté de l'élément concerné.
- **Risque** : `g-bubble-bang`.

## 4. Parcours (flow)

- Écrans reliés par des flèches noires, l'action déclenchante en trois mots au-dessus de la flèche (« ouvrir », « valider », « retour »).
- Embranchements : un écran avec deux flèches sortantes, la plus fréquente en noir, l'autre en `gray`.
- Retour ou abandon : flux `flow` (gris pointillé) qui revient ou sort du cadre, `g-cross` à l'extrémité pour un abandon.
- Moments hors écran (notification, e-mail, appel) : un petit symbole (`g-bubble`, `g-phone`) entre deux écrans, sans cadre.

## 5. États d'un écran

Pour montrer vide, chargé, erreur : le même écran trois fois en petit format (cadres de 216 × 384, éléments réduits dans la même proportion), alignés, un libellé en `tg` sous chacun (« vide », « chargé », « erreur »). L'erreur reçoit l'accent `fr` sur l'élément concerné. Ne pas dessiner plus de trois états.

## 6. Parcours utilisateur (vue d'ensemble)

Rangée du haut : étapes (`box`, quatre à six) ; rangée du milieu : ce que fait la personne (symbole ou trois mots) ; rangée du bas : ce qu'elle ressent, matérialisé par une courbe continue (`ink`, une seule) qui monte et descend, creux annoté en bleu. Points de douleur : accent `fr` sur un seul point. Pas de smileys.

## 7. Storyboard

Quatre à six vignettes (cadres 300 × 220) en rangée, chaque vignette = une scène avec un ou deux symboles et un libellé de trois mots dessous. Flèche fine entre les vignettes. Même méthode que la scène d'objets (`references/familles-diagrammes.md`, famille 11).

## 8. En réunion

Dessiner d'abord le cadre vide, puis remplir à mesure de la discussion. Ne dessiner que l'écran dont on parle ; garder les autres en cadres vides à demi-échelle. Passer à `references/mode-live.md` pour le rythme.
