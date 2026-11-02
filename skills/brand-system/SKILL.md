---
name: brand-system
description: >
  Système de marque sobre et éditorial, fourni comme marque par défaut : palette
  bleue sur fond clair, typographie Inter, dégradé doux, boutons en pilule, cartes
  à ombre légère, icônes Phosphor. Appliquer à tout livrable (présentation,
  document, page, artefact web) quand aucune autre charte n'est donnée, ou s'en
  servir comme modèle à remplacer par la charte d'un projet. À combiner avec
  `slides` (mises en page) et `pptx` (génération du fichier). Déclencher dès
  qu'on demande une mise en forme soignée, une identité visuelle, des tokens de
  design, ou un livrable client à l'aspect professionnel.
---

# Système de marque

Un référentiel visuel et éditorial complet, prêt à l'emploi : couleurs, typographie, dégradé, composants, règles de logo, ton de voix externe et structure des livrables. Il vaut pour tout output destiné à un client, un prospect ou une audience externe.

Ces valeurs sont des valeurs par défaut. Quand un projet a sa propre charte, la lire d'abord et remplacer les tokens (palette, polices, logo) : les règles de composition, le ton et la structure des livrables restent valables.

Esprit général : économie de moyens, espace blanc généreux, typographie à haute lisibilité, esthétique suisse et bauhaus.

Fichiers de référence :
- `references/tokens.css` et `references/tokens.json` : les tokens ci-dessous, prêts à importer.
- `references/charte.png` (et `.svg`) : la palette, la typographie et les composants sur une planche.

---

## 1. Palette

| Rôle | Hex | Notes |
|---|---|---|
| Couleur du logo | #295FEC | Logo uniquement |
| Primaire (CTA, liens, accents) | #3D65E8 | Interface, textes d'accent, boutons |
| Fond global clair | #EBEFF7 | Fond de slides de contenu, bandeaux |
| Fond off-white (base du dégradé) | #F8F9FB | Base des slides et pages avec dégradé |
| Surface, carte | #FFFFFF | Cartes, blocs, encadrés |
| Bloc surface légère | #F0F2F7 | Cartes dans les grilles |
| Texte principal | #111827 | Corps, titres sombres |
| Texte discret | #6B7280 | Labels, légendes, métadonnées |
| Vert de statut | #22C55E | Indicateurs positifs |

Un seul niveau de couleur d'accent par support : la couleur primaire.

## 2. Dégradé de fond

Un dégradé radial doux, appliqué sur les surfaces claires et les slides. Il reste subtil : invisible au premier regard.

```css
background: radial-gradient(
  ellipse at 85% 10%,
  rgba(180, 215, 245, 0.55) 0%,
  rgba(200, 230, 252, 0.25) 35%,
  transparent 65%
), #F8F9FB;

/* Variante sur deux coins opposés */
background:
  radial-gradient(ellipse at 90% 5%, rgba(165, 210, 245, 0.45) 0%, transparent 50%),
  radial-gradient(ellipse at 5% 95%, rgba(165, 210, 245, 0.25) 0%, transparent 45%),
  #F8F9FB;
```

En PPTX : fond de slide #F8F9FB, remplissage dégradé radial dans le coin haut droit, couleur de départ #B4D7F5 à 55 % d'opacité, vers transparent.

## 3. Composants

**Boutons**
- Action primaire : forme de pilule (rayon 999 px), fond primaire, texte blanc, icône flèche à droite.
- Action secondaire : pilule, fond blanc, bordure légère, texte sombre, icône flèche à droite.

**Cartes**
- Fond blanc ou surface légère, rayon 16 px, ombre douce, aucune bordure marquée.
- Métadonnée : l'année en texte discret, puis un séparateur point (par exemple « 2024 · Nom du projet »).
- Titre en semi-gras, corps en regular, lien en bas en texte discret.

## 4. Typographie

| Usage | Police | Graisse |
|---|---|---|
| Titres majeurs | Inter | Black 900 ou ExtraBold 800 |
| Sous-titres, labels | Inter | SemiBold 600 |
| Corps de texte | Inter | Regular 400 |
| Métadonnées, légendes | Inter | Regular 400, texte discret |

Police de repli prioritaire : Public Sans. Replis système : Geist, SF Pro, Helvetica Neue. Aucune police à empattement ni décorative.

## 5. Icônes

Phosphor Icons ou Lucide, graisse Regular ou Light selon le contexte. Aucun emoji dans les livrables.

## 6. Logo

Le logo du projet est fourni avec le projet : aucun fichier de logo n'accompagne cette skill. Règles d'usage valables pour tout logo :

- **Slides, couverture sur fond de couleur :** logotype en haut à gauche, version blanche si elle existe, hauteur du symbole 36 à 40 px.
- **Slides de contenu, fond clair :** symbole seul ou logotype complet en pied de page, hauteur 20 à 24 px, texte discret, aligné en bas à gauche.
- **Documents Word :** logotype en en-tête de la première page, aligné à gauche, hauteur 28 à 32 px, sans étirement.
- **Artefacts web :** symbole SVG en ligne, 32 px, avec un lien vers le site.
- **Marge de protection :** au moins 1 fois la hauteur du symbole de chaque côté, sans texte ni élément graphique dans cette zone.
- **À éviter :** déformer ou étirer le logo, le recolorer hors de sa couleur ou du blanc, utiliser une version floue ou sous-résolue, le poser sur un fond de contraste insuffisant.

## 7. Ton de voix externe

- De pair à pair, jamais condescendant, jamais commercial.
- Précis et ancré : cas réels, métriques, mécanismes observables.
- Accessible sans vulgariser. L'expertise se lit dans la précision, pas dans les superlatifs.
- Appliquer `sober-writing` en parallèle pour la posture rédactionnelle, et `francais-parfait` pour un texte en français.

À bannir dans tous les documents externes : « passionné par », « orienté résultats », « créateur de valeur », les biographies auto-congratulatoires à la troisième personne, les listes de compétences sans contexte ni preuve, le ton d'agence qui promet beaucoup et explique peu.

## 8. Structure des livrables

**Proposition commerciale, one-pager**
1. Le contexte et l'enjeu du client, sans introduction sur soi.
2. L'angle d'intervention et son mécanisme.
3. Les livrables et les jalons.
4. Le tarif et les modalités.
5. Les références pertinentes (cas similaires).

**Étude de cas**
1. La situation de départ : métriques, contraintes, organisation.
2. Les décisions prises, et pourquoi.
3. Les résultats mesurables.
4. Ce qui aurait pu être fait autrement.

**Biographie professionnelle (80 à 100 mots)**
- Ouvrir sur le rôle et l'angle qui différencie.
- Deux ou trois preuves concrètes : clients, résultats, contextes.
- Fermer sur la disponibilité ou la spécialisation actuelle.

**E-mail de prospection** : objet spécifique au destinataire ; corps de 80 à 120 mots, avec une observation sur sa situation, une proposition directe et un appel à l'action clair.

**Document Word** : logotype en en-tête, pied de page avec les coordonnées du projet, corps en Inter ou Public Sans, titres en semi-gras, un seul accent de couleur, aucune fioriture décorative.

## 9. Combiner avec `slides` et `pptx`

Trois skills, trois rôles :

| Skill | Rôle |
|---|---|
| `brand-system` (celle-ci) | L'identité : palette, typographie, dégradé, composants, logo, ton |
| `slides` | La mise en page : quinze mises en page, structure narrative, titres |
| `pptx` (skill d'Anthropic, à installer séparément) | La génération technique du fichier `.pptx` |

Marche à suivre pour produire une présentation :
1. Lire `brand-system` pour fixer les tokens (ou les remplacer par ceux du projet).
2. Lire `slides` pour choisir la structure du deck et les mises en page, en reprenant ces tokens.
3. Lire `pptx` pour générer le fichier, en appliquant les valeurs des deux premières.
4. Contrôler le résultat slide par slide (export en images) avec la vérification de `slides`.

## 10. Vérification avant tout livrable

1. Le positionnement s'appuie sur des preuves, pas sur des qualificatifs.
2. Le ton est de pair à pair, pas commercial.
3. Le logo respecte ses règles d'usage et ses marges.
4. Couleur du logo et couleur d'accent de l'interface distinctes : #295FEC pour l'un, #3D65E8 pour l'autre.
5. Typographie Inter ou Public Sans uniquement.
6. Aucun emoji, aucun tiret cadratin, aucun mot à la mode creux.
7. `sober-writing` appliquée, et `francais-parfait` pour un texte en français.
