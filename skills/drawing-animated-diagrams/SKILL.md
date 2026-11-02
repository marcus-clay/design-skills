---
name: drawing-animated-diagrams
description: Use when a page needs an explanatory diagram (process, timeline, flow, structure, before/after) as an SVG React component that draws itself as it scrolls into view, in a minimalist ink-and-grey style, for a Next.js or React site. Also when asked for a "diagramme animé", "schéma qui se dessine".
---

# Diagrammes dessinés, animés à l'entrée dans l'écran

## Principe

Une idée par diagramme, écrite d'abord en une phrase. Le dessin se trace une fois quand il entre dans l'écran, dans l'ordre où on le lit, puis ne bouge plus. L'encre porte le message, le gris porte le reste, les étiquettes sont sur le dessin, il n'y a pas de légende. Avec « Réduire les animations », le dessin est simplement là.

**REQUIRED BACKGROUND :** `diagram-storytelling` (réduction à une idée, verbes sur les flèches, nœuds = états). `emil-design-eng` pour les courbes et durées.

## Quand ne pas l'utiliser

- Un graphique de données (courbe, barres chiffrées) : outil de dataviz.
- Une animation qui joue en boucle pour montrer un fonctionnement en temps réel : prototype animé, pas diagramme.
- Un diagramme vu des dizaines de fois par jour dans un outil : pas d'animation du tout.

## Marche à suivre

1. **La phrase.** Écrire l'idée en une phrase, avec le sujet qui portera l'encre (« trois concepts explorés, un prototype retenu »). Si la phrase a deux idées, faire deux diagrammes.
2. **Le vocabulaire.** Copier `reference/diagramMotion.ts` et `reference/DiagramParts.tsx` dans le projet s'ils n'y sont pas. Ne jamais redéfinir `Panel`, `Arrowhead`, les tons ou les helpers localement.
3. **Les mots.** Un fichier de données bilingue (`en`/`fr`) : `title` et `desc` pour l'accessibilité, puis chaque étiquette. Une étiquette fait au plus quelques mots. Français : accents sur les majuscules, espace insécable avant « : », aucun tiret cadratin.
4. **La géométrie.** `viewBox="0 0 960 H"` (H entre 300 et 400), coordonnées en constantes nommées, 60 px de marge à gauche et à droite pour les étiquettes en bout de ligne (une étiquette `textAnchor="end"` à x = 54 est coupée). Minimum du `Panel` : 720 (il défile sur téléphone).
5. **L'ordre de lecture = l'ordre des délais.** Chaque élément reçoit un délai en ms qui suit la lecture : 0 pour ce qu'on lit d'abord, +200 à 300 ms par étape, 40 à 110 ms entre les éléments d'une même série. Le message en encre arrive en dernier (1 500 à 2 300 ms). Durée totale du tracé : 2 à 3 s.
6. **La vérification.** Rendre la page sur localhost, faire défiler le diagramme au centre, attendre 3 s, capturer le panneau (`reference/shoot-diagrams.cjs`, à lancer avec `NODE_PATH=<projet>/node_modules`). Regarder chaque capture : étiquettes coupées au bord, étiquette sous un bloc blanc, deux étiquettes côte à côte qui se touchent. Corriger, recapturer. Vérifier aussi à 390 px.

## Référence rapide

| Élément | Helper | Valeurs |
|---|---|---|
| Ligne, flèche | `draw(shown, delay, duration)` sur un `path` avec `pathLength={1}` | 400 à 900 ms |
| Ligne pointillée | ne peut pas se tracer : `rise` (fondu) | |
| Bloc, étiquette | `rise(shown, delay)` : monte de 8 px | 500 ms |
| Barre de temps | `grow(shown, delay, duration)` : pousse depuis la gauche | 500 à 800 ms |
| Cadre, lentille | `open(shown, delay)` : s'ouvre de 0,96 à 1 | 600 ms |
| Pointe de flèche | `<Arrowhead x y angle style={rise(...)}>` juste après le `draw` | |
| Tons | `INK #111827` message, `LINE #D1D5DB` bords, `PALE #E5E7EB` fonds, `#6B7280` étiquettes secondaires, `#9CA3AF` ce qui est écarté | |
| Texte | titre de nœud 14 px 600, étiquette 11 à 13 px, jamais plus petit que 10 | |
| Courbe | `cubic-bezier(0.22, 1, 0.36, 1)` (déjà dans les helpers) | |

Toute transformation CSS va sur un `<g>` enveloppant, jamais sur une forme qui a un `transform` SVG (elle le remplacerait).

## Formes par type d'idée

- **Séquence qui se resserre** : nœuds en ligne, éventail de branches, une seule continue en encre, les autres en `LINE` avec « écarté ».
- **Rythme dans le temps** : axe des semaines en haut, une ligne par acteur, barres `grow`, une flèche en encre pour la relation qui compte.
- **Ouverture puis convergence** : une lentille (`open` puis `draw` du contour) au-dessus d'une barre proportionnelle aux durées.
- **États et transitions** : nœuds = états (pointillé pour l'exploration, gris pour l'intermédiaire, encre pleine pour ce qui est gravé), flèches étiquetées par le verbe, au-dessus de la rangée pour ne pas toucher les nœuds.
- **Un objet découpé en parties** : l'objet à gauche, coupes en pointillé, flèche, les parties en cartes à droite, la première en encre.

Un exemple complet de chaque forme : `reference/exemple-TemplateDiagrams.tsx` et ses mots dans `reference/exemple-templateDiagramsData.ts`.

## Vignette d’un diagramme (carte, liste)

Le même composant rend une vue fixe et cadrée pour une carte : `thumb` désactive le panneau et la révélation, et le `viewBox` devient un cadre de 520 × 400 (13:10, comme l’image des cartes) centré sur le message. Un cadre par diagramme, dans `FRAMES`, vérifié en capture à 350 px de large : le texte reste lisible à partir de 11 px dans le dessin. Voir `Drawing` et `TemplateDiagramThumb` dans `reference/exemple-TemplateDiagrams.tsx`.

## Erreurs fréquentes

| Erreur | Correction |
|---|---|
| Ajouter une boucle (pastille qui circule, états qui clignotent) « pour que ça vive » | Le tracé est le mouvement. Une boucle seulement si le temps est le sujet du diagramme, une seule, après le tracé, via `useLoop` |
| Couleurs d'accent, vert/rouge pour valide/refusé | Encre et gris seulement ; un verdict se dit par la forme (plein, pointillé, écarté) ou par un mot |
| Légende à côté du dessin | Les mots sont sur le dessin, près de ce qu'ils nomment |
| Flèche étiquetée par le nom de l'écran d'arrivée | Le verbe de la transition (« validé », « non retenu ») |
| Étiquette centrée entre deux nœuds de 60 px d'écart | Elle déborde sur les nœuds : la placer au-dessus de la rangée |
| Délais choisis pour l'effet | Délais qui suivent la lecture, message en dernier |
| Déclarer fini sans capture | Capturer après défilement et 3 s d'attente, lire la capture |
