# Mode Interactif : une illustration qui évolue

Pour montrer une transformation dans le temps : un processus produit qui évolue, une organisation (maintenant, ensuite, plus tard ; actuellement, demain), un changement de tendance, un enrichissement progressif. La page produite est un seul fichier HTML, sans dépendance, qui fonctionne hors ligne, avec le même style feutre que les croquis statiques.

## 1. Ce que la page permet

- boutons d'états, curseur de temps (on fait défiler l'évolution à la main), lecture automatique, retour au début
- éléments qui se déplacent, changent de taille, de rotation, d'opacité, de forme (courbes qui se déforment), se tracent (trait qui apparaît), changent de texte
- liens (flèches) qui suivent les éléments qui bougent
- couches à afficher ou masquer (par exemple « Rôles », « Risques »)
- éléments marqués `drag` : glissés à la souris ou au doigt, ce qui modifie l'état affiché
- double-clic sur un texte pour le renommer
- boutons « Exporter SVG » (l'état affiché, statique) et « Copier la disposition » (JSON des positions)
- clavier : flèches gauche et droite, espace (lecture), Début et Fin, f (plein écran)
- respect de `prefers-reduced-motion` (transitions instantanées) ; si l'appareil est lent, le tremblé du trait est désactivé automatiquement

## 2. Fabrication en trois fichiers

1. **`draft.svg`** : dessin brut, comme en mode Croquis, mais chaque élément qui bouge est un groupe (ou un chemin) avec un `id`. Les liens sont des chemins vides avec `data-link`.
2. **`scenes.json`** : la chorégraphie (états, images clés, couches, notes).
3. **Assemblage** : `python3 scripts/compose.py draft.svg --interactive scenes.json -o page.html`

Contrôle : `python3 scripts/render.py page.html --state 0` (puis 1, 2, 1.5 pour vérifier l'entre-deux). Le script prévient si la configuration cite un `id` absent du dessin.

## 3. Le dessin brut

- Dessiner chaque élément animé **centré sur l'origine (0, 0)**, et donner sa position dans `x` et `y` de la première image clé : la page place l'origine de l'élément à ce point, et l'échelle et la rotation se font autour de lui. Un élément déclaré sans image clé reste en (0, 0), donc ne pas déclarer ce qui est dessiné en place. Ne pas écrire d'attribut `transform` sur un élément animé, la page le remplace.
- Un symbole : `<g id="p1"><use href="#g-person" x="-60" y="-70"/></g>`.
- Un lien qui suit deux éléments : `<path id="k1" class="ink arr" data-link="a>b" data-bend=".2"/>` (pas d'attribut `d`, la page le calcule ; `data-bend` règle la courbure en S).
- Une couche : `data-layer="roles"` sur les éléments concernés, déclarée dans `layers`.
- Un chemin qui change de forme : la structure de commandes doit être identique dans chaque état (même suite de lettres `M`, `C`, `L`, `Z`, seuls les nombres changent). Sinon la forme bascule d'un coup à mi-parcours.
- Le style s'applique comme d'habitude (`ink`, `dotk`, `f1`...). Les tracés pointillés (`dotk`, `flow`, `dash`) ne peuvent pas utiliser `draw` : la propriété remplace le pointillé par un trait plein pendant l'animation.

## 4. La configuration `scenes.json`

```json
{
  "title": "Notre organisation produit",
  "states": ["Maintenant", "Ensuite", "Plus tard"],
  "notes": ["Trois files d'attente.", "Squads mixtes.", "Plateforme commune."],
  "layers": [{ "id": "roles", "label": "Rôles", "on": true }],
  "duration": 1300,
  "hold": 1800,
  "elements": {
    "p1": { "k": [ {"x":300,"y":330}, {"x":560,"y":240}, {"x":230,"y":360} ], "drag": true, "lag": 0.05 },
    "sqA": { "k": [ {"o":0,"d":"M-10 -10L10 -6L7 10L-6 7Z"}, {"o":1,"d":"M-270 -80L270 -76L267 80L-266 77Z"}, {} ] }
  }
}
```

| Clé | Rôle |
|---|---|
| `states` | noms des états (2 à 6), un bouton chacun |
| `notes` | une phrase par état, affichée en bleu en haut à droite |
| `layers` | couches affichables ; `on: false` pour la masquer au départ |
| `duration` | millisecondes d'une transition (défaut 1100) |
| `hold` | pause en lecture automatique (défaut 1700) |
| `elements.<id>.k` | tableau d'images clés, une par état |
| `elements.<id>.drag` | `true` : déplaçable à la souris |
| `elements.<id>.lag` | retard 0 à 0,9 : l'élément démarre après les autres (effet d'entraînement) |

Image clé, toutes clés facultatives, **la valeur précédente est reconduite** si on n'écrit rien :

| Clé | Effet |
|---|---|
| `x`, `y` | position de l'origine de l'élément sur la page (px) |
| `s` | échelle (1 = taille dessinée) |
| `r` | rotation en degrés autour de l'origine |
| `o` | opacité de 0 à 1 (un élément à 0 n'est plus cliquable) |
| `d` | nouvelle forme d'un `<path>` (déformation fluide) |
| `draw` | 0 à 1, longueur de trait visible (trait qui se dessine) |
| `txt` | nouveau texte (change à mi-transition) |

## 5. Six patrons

**1. Maintenant, ensuite, plus tard (feuille de route).** Trois colonnes (`dotk` ou titres `tl`), des cartes (`g-card`, `g-sticky`) qui glissent de colonne en colonne (`x` change d'un état à l'autre). La carte en cours en `fh`. Notes : « ce qu'on livre », « ce qu'on prépare », « ce qu'on explore ». Couches optionnelles « Équipe A » et « Équipe B ».

**2. Avant, après (structure d'organisation).** Des personnes (`g-person` à 0,6) qui se regroupent : silos en colonnes, puis squads mixtes, puis squads plus plateforme. Périmètres `dotk` qui se déforment (`d`) et apparaissent (`o`). Liens de passage de relais qui disparaissent. C'est l'exemple `examples/migration-organisation`.

**3. Enrichissement.** Un noyau qui s'étoffe : à chaque état, de nouveaux nœuds apparaissent (`o` 0 puis 1, `s` 0,6 puis 1) et leurs liens se tracent (`draw` 0 puis 1). Les couches permettent de revenir à la version minimale.

**4. Changement de tendance.** Axes fixes, une courbe qui se déforme (`d`), un point repère qui suit (`x`, `y`), une annotation bleue qui se trace à l'état où la pente casse (`draw`), un seuil en tirets. Texte du repère qui change (`txt`). C'est l'exemple `examples/tendance-adoption`.

**5. Évolution d'un processus.** Étapes en `box` sur une ligne. Entre deux états : une étape disparaît (`o` 0, les suivantes glissent de `x` vers la gauche), une autre se dédouble (deux copies superposées qui s'écartent), le goulot passe en `fr` puis revient en gris. Les liens (`data-link`) se reconnectent seuls.

**6. Montée en charge.** Un objet central qui grandit (`s`), se scinde en trois (trois copies superposées en état 0, écartées ensuite), les liens se multiplient. Texte du chiffre clé (`txt`) sans inventer de valeur.

## 6. Bonnes pratiques

- Deux à quatre états : au-delà, c'est une présentation.
- Dix à quinze éléments animés au maximum, sinon la lecture devient confuse et lente.
- Chaque état doit tenir debout seul (c'est ce qu'on exporte pour une slide). Tester avec `render.py --state N`.
- Les éléments qui ne changent pas ne sont pas déclarés : ils restent fixes.
- Une phrase par état dans `notes`, de trois à quinze mots.
- Les éléments `drag` sont ceux que l'équipe voudra déplacer en réunion. Après manipulation, « Copier la disposition » donne le JSON des positions à recoller dans la configuration (ou à me renvoyer pour fusion).
- Le tremblé du trait est calculé sur toute la page : un élément qui bouge « glisse » légèrement dans le bruit, ce qui ressemble à du dessin animé à la main. Si l'effet gêne, ajouter `data-q="low"` sur `<html>` pour le couper.

## 7. Livraison

- **Claude Code** : `page.html` dans le dossier, chemin donné ; l'ouvrir dans le navigateur.
- **claude.ai** : publier la page en artifact (autonome, environ 50 ko ; charger la skill `artifact-design` d'abord, titre de deux à quatre mots). Les téléchargements peuvent être bloqués dans le cadre de l'artifact : dans ce cas « Exporter SVG » affiche le texte à copier.
- **Pour une slide** : exporter chaque état en SVG (bouton) ou en PNG (`render.py --state N`), puis les poser côte à côte.

## 8. Pièges connus

- Oublier `id` sur un élément déclaré : le script le signale, l'élément ne bouge pas.
- Chemin dont la structure change entre états : la forme saute au lieu de se déformer.
- `draw` sur un tracé pointillé : le pointillé devient plein pendant l'animation.
- Élément dessiné en place au lieu d'être centré sur (0, 0) : il part dans un coin dès qu'on lui donne une position. Le redessiner autour de l'origine.
- Texte édité (double-clic) : la modification vit dans la page, elle disparaît au rechargement ; l'export SVG la conserve.
