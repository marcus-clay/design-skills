---
name: slides
description: >
  Système de création de présentations et de slides : tokens de design,
  catalogue de quinze mises en page, structure narrative et conventions de
  rédaction des titres. Appliquer à tout output de type deck, pitch,
  présentation client, keynote, support de formation ou rapport visuel.
  Déclencher dès que la demande implique des slides, un deck, une présentation
  PowerPoint, Google Slides, ou tout support visuel multi-pages. Prend la
  priorité sur une skill de génération de fichiers (pptx) pour les choix
  visuels et stylistiques : celle-ci gère la technique, slides gère les
  tokens, la structure narrative et les mises en page.
---

# Slides

Système de design pour les présentations. S'applique à tous les decks :
internes, clients ou publics.

Les valeurs de palette, de typographie et de logo ci-dessous sont des valeurs
par défaut. Si le projet a sa propre charte, la lire d'abord (palette, logo,
polices) et remplacer ces valeurs : les mises en page, les règles et la
structure narrative restent les mêmes.

Si une skill de génération de fichiers existe (par exemple `pptx`), la lire
également pour la technique de génération.

---

## 1. Tokens de design

### Palette principale

| Rôle | Hex | Usage slides |
|---|---|---|
| Bleu logo | #295FEC | Logo uniquement |
| Bleu primaire | #3D65E8 | Accents, surtitres, CTA, bordure top, dots timeline |
| Fond off-white (gradient) | #F8F9FB | Fond de base pour slides avec gradient |
| Fond clair contenu | #EBEFF7 | Slides de transition, fond alternatif |
| Surface / carte | #FFFFFF | Blocs de contenu, cartes |
| Bloc surface légère | #F0F2F7 | Cards dans grilles 3-6 blocs |
| Texte principal | #111827 | Titres, corps |
| Texte muted | #6B7280 | Labels, légendes, footer |

### Gradient de fond (soft blue)

Appliqué sur les slides de fond clair, couvertures légères et slides de titre :

- En PPTX : fond de slide #F8F9FB, remplissage dégradé radial, coin haut-droit,
  couleur #B4D7F5 opacité 55% vers transparent.
- Variante symétrique (décks longs) : gradient également en coin bas-gauche,
  #B4D7F5 opacité 25%.
- Le gradient est toujours doux et subtil. Jamais de saturation forte.
  Il doit rester invisible au premier regard.

### Typographie

| Usage | Police | Poids | Taille indicative |
|---|---|---|---|
| Titre de slide | Inter | Black 900 ou ExtraBold 800 | 36-56pt |
| Titre hero (big title) | Inter | Black 900 | 72-96pt |
| Sous-titre / chapeau | Inter | SemiBold 600 | 20-24pt |
| Surtitle / label section | Inter | SemiBold 600 | 10-12pt, uppercase, #3D65E8 |
| Corps de texte | Inter | Regular 400 | 14-16pt |
| Label / métadonnée | Inter | Regular 400 | 10-12pt, muted |

Fallback : Public Sans (https://fonts.google.com/specimen/Public+Sans).
Fallbacks système : Geist, SF Pro, Helvetica Neue. Jamais de serif.

### Icônes

Phosphor Icons (https://phosphoricons.com/) ou Lucide (https://lucide.dev/).
Regular ou Light. Zéro emoji.

---

## 2. Logo dans les slides

**Assets** : le symbole et le logotype (symbole + nom) de la marque du projet,
en SVG ou PNG. Aucun logo n'est fourni avec cette skill.

### Placement standard

- **Couverture (fond couleur primaire)** : logotype en haut à gauche,
  hauteur 36-40px, version blanche si elle existe ; sinon symbole seul.
- **Slides de contenu (fond clair)** : footer bas gauche, symbole rond 20px
  + nom en Inter Regular 10pt muted #6B7280.
- **Slides de transition** : même footer ou absence de logo (minimaliste).

### Structure du footer standard

```
[Symbole 20px]  Nom        adresse e-mail | site | LinkedIn   [N°]
```

Footer aligné sur la ligne de base, typographie 10pt muted. Séparateur |
entre les éléments de contact. Numéro de slide aligné à droite.

---

## 3. Catalogue de layouts

### Règle universelle

Une idée par slide. Espace blanc généreux. Un élément dominant.
Ratio texte/visuel : maximum 60% texte. Titres affirmatifs et spécifiques.

---

### LAYOUT 01 — Couverture

Structure :
- Fond : bleu #3D65E8 ou fond gradient off-white selon le ton du deck
- Logo wordmark haut gauche
- Surtitle (client ou contexte) : uppercase, Inter SemiBold 12pt, blanc ou bleu
- Titre principal : Inter Black 900, 48-56pt, blanc ou #111827, max 2 lignes
- Sous-titre ou accroche : Regular 18pt, muted ou blanc 70%
- Footer : coordonnées (e-mail, site, LinkedIn), 10pt, bas gauche

Variante fond gradient (decks concept) : fond #F8F9FB + gradient radial haut-droit,
titre en #111827, accent en #3D65E8.

---

### LAYOUT 02 — Grand titre (section, transition, idée forte)

Structure :
- Fond : #EBEFF7 ou gradient off-white
- Ligne de bordure top : 3px plein #3D65E8, pleine largeur
- Titre seul : Inter Black 900, 56-72pt, #111827, aligné gauche, 40% de la hauteur
- Sous-titre optionnel : SemiBold 600, 20pt, muted
- Footer logo minimal

Usage : ouverture de chapitre, énoncé de problème, stat choc.

---

### LAYOUT 03 — Big Idea (une phrase, plein écran)

Structure :
- Fond blanc pur #FFFFFF ou gradient
- Une seule phrase, Inter Black 900, 64-96pt
- Mots clés colorés en #3D65E8 (sélectif, 1-2 mots max)
- Aucun autre élément sauf footer discret
- Alignement : gauche ou centré selon le rythme du deck

Usage : pitch, keynote, moment de rupture narrative.

---

### LAYOUT 04 — Titre + corps (standard)

Structure :
- Fond #F8F9FB avec gradient ou #EBEFF7
- Surtitle uppercase bleu 11pt haut gauche
- Titre : Inter Black 900, 36-44pt
- Corps : 2-4 paragraphes ou bullets, Regular 400, 14-16pt
- Marge généreuse droite (au moins 15% de la largeur)
- Footer logo

---

### LAYOUT 05 — Half text / half media

Structure :
- Fond : #F8F9FB gradient
- Colonne gauche (50%) : titre + corps ou bullets, aligné gauche
- Colonne droite (50%) : image, screenshot, mockup, ou schéma
- Séparation : espace blanc uniquement (pas de ligne, pas de fond différent)
- Image droite : bords arrondis 12-16px, shadow douce

Usage : présenter une interface, un cas, une comparaison visuelle.

---

### LAYOUT 06 — 1/3 texte + 2/3 device mockup

Structure :
- Fond : #F8F9FB gradient
- Colonne gauche (33%) : surtitle + titre + 2-3 points clés ou descriptif court
- Colonne droite (67%) : mockup device (iPad, Mac, iPhone) avec l'UI à l'intérieur
  - Mockup : cadre fin #F0F2F7, bords très arrondis pour mobile, rectangle pour Mac/iPad
  - L'UI inside est un screenshot réel ou maquette fidèle
  - Le device peut dépasser légèrement les marges (bleed subtle)

Usage : présentation de concept produit, prototype, nouvelle fonctionnalité.

---

### LAYOUT 07 — 3 colonnes

Structure :
- Fond : #F8F9FB gradient ou #FFFFFF
- Titre de slide haut gauche
- 3 colonnes égales, gap 24-32px
- Chaque colonne : titre SemiBold + contenu + lien ou label bas
- Surface colonne : #F0F2F7, border-radius 12px, padding généreux
- Pas de bordure marquée entre colonnes

Usage : 3 concepts, 3 options, 3 cas, comparaison 3 outils.

---

### LAYOUT 08 — 3 blocs

Identique au LAYOUT 07 mais en organisation verticale ou avec une ligne de hiérarchie
plus marquée. Surface de bloc plus grande, contenu plus dense par bloc possible.

---

### LAYOUT 09 — 4 blocs (2×2)

Structure :
- Fond : #F8F9FB gradient
- Titre de slide haut gauche
- Grille 2×2, gap 20px
- Chaque bloc : surface #F0F2F7, border-radius 12px, titre SemiBold + body Regular
- Largeur et hauteur des blocs égales

Usage : 4 services, 4 étapes, 4 points clés.

---

### LAYOUT 10 — 6 blocs (2×3 ou 3×2)

Structure :
- Fond : #FFFFFF ou #F8F9FB
- Titre de slide haut gauche, sous-titre descriptif optionnel
- Grille 3 colonnes × 2 lignes ou 2 colonnes × 3 lignes selon contenu
- Blocs : surface #F0F2F7, border-radius 12px, titre SemiBold 14pt + body Regular 12pt
- Label ou tag contextuel en bas de chaque bloc, en bleu #3D65E8 sur fond légèrement
  plus saturé (#E8EEF8)

Usage : boîte à outils, méthodes, fonctionnalités, compétences.

---

### LAYOUT 11 — Timeline

Structure :
- Fond : #FFFFFF avec ligne de bordure top bleue 3px
- Titre haut gauche, sous-titre descriptif 14pt muted
- Axe vertical gauche : ligne fine #E5E7EB
- Chaque entrée : date/année en muted gauche + dot bleu #3D65E8 (12px) + titre Bold +
  sous-titre Regular + détail en italic muted
- Espacement vertical généreux entre entrées (ne pas comprimer)

Usage : parcours, historique de projet, roadmap passé/présent.

---

### LAYOUT 12 — Roadmap

Structure :
- Fond : #F8F9FB gradient
- Titre haut gauche
- Axe horizontal : ligne #E5E7EB avec marqueurs ou blocs par période
- Périodes : Q1/Q2... ou Mois 1/2... ou Phase 1/2...
- Blocs de items : surface #FFFFFF ou #F0F2F7, border-radius 8px, titre + label statut
- Statuts : couleur dot ou badge (bleu = en cours, vert = livré, gris = à venir)
- Footer logo

Usage : planning de mission, roadmap produit, jalons.

---

### LAYOUT 13 — Table

Structure :
- Fond : #FFFFFF ou #F8F9FB
- Titre haut gauche
- En-têtes de colonnes : fond #3D65E8, texte blanc, Inter SemiBold 12pt
- Lignes alternées : #FFFFFF / #F0F2F7 pour lisibilité
- Cellules : Regular 400, 13pt, padding 12px
- Pas de bordures épaisses. Séparateurs horizontaux fins #E5E7EB uniquement.

---

### LAYOUT 14 — Visuel pleine largeur / pleine hauteur

Structure :
- Image ou screenshot couvre 100% du fond de slide (bleed total)
- Overlay gradient sombre ou clair selon le contenu à afficher par-dessus
- Titre en overlay : Inter Black 900, blanc ou #111827, bas gauche ou centré bas
- Aucun chrome de slide visible (pas de fond, pas de bordure, pas de footer sauf
  numéro de page discret)

Usage : transitions dramatiques, intro de section, portfolio, screenshots hero.

---

### LAYOUT 15 — Device + UI mockup en pleine largeur

Structure :
- Fond : #F8F9FB gradient
- Device (Mac, iPad, iPhone) centré ou légèrement décalé droite, 70-80% de la hauteur
- L'UI inside : screenshot réel ou maquette haute fidélité
- Titre ou label flottant gauche : Inter SemiBold 20pt, #111827
- Shadow portée sous le device : douce, opacité 15-20%
- Pas de frame supplémentaire autour du device

Usage : hero concept, showcase produit, prototype pleine résolution.

Mockup device conventions :
- iPhone : frame fin anthracite ou blanc, coins très arrondis
- iPad : frame fin aluminium, orienté portrait ou paysage selon contenu
- MacBook : frame aluminium ouvert, écran centré, base discrète
- Garder les proportions constructeur

---

## 4. Principes de mise en page

- Titre dominant par slide : le lecteur comprend l'idée sans lire le corps.
- Espace blanc généreux : ne jamais remplir plus de 70% de la surface.
- Hiérarchie forte : un seul élément « premier regard » par slide.
- Fond blanc pur #FFFFFF comme fond global de deck : interdit. Préférer #F8F9FB.
- Texte centré sur slides de contenu : interdit (centré uniquement sur couverture
  et LAYOUT 03 Big Idea).
- Mélange de polices : interdit.
- Ligne décorative sous les titres : interdit.
- Même layout répété plus de 3 slides consécutives : éviter.

---

## 5. Slides de structure

| Type | Fond | Texte | Layout |
|---|---|---|---|
| Couverture | #3D65E8 ou gradient #F8F9FB | Blanc ou #111827 | LAYOUT 01 |
| Transition / chapitre | #EBEFF7 + bordure top | #111827 | LAYOUT 02 |
| Contenu standard | #F8F9FB gradient | #111827 | LAYOUT 04 à 15 |
| Big Idea | #FFFFFF ou gradient | #111827 + accent bleu | LAYOUT 03 |
| Conclusion / CTA | #3D65E8 | Blanc | LAYOUT 01 variante |

Structure recommandée (sandwich) : couverture fond bleu, slides contenu clairs
avec gradient, conclusion fond bleu.

---

## 6. Conventions narratives

### Arc du deck

1. Situation actuelle (ancrage dans la réalité du client)
2. Tension ou problème identifié
3. Angle d'intervention et mécanisme
4. Livrables, jalons, ou solution proposée
5. Prochaine étape concrète

### Titres de slides

- Spécifiques et affirmatifs : « Les tests révèlent 3 points de friction critiques »,
  pas « Résultats des tests ».
- Le lecteur qui ne lit que les titres doit comprendre la logique du deck.
- Interdits : « Introduction », « Contexte », « Conclusion », « Sommaire ».

### Données et métriques

- Stat callout centré : chiffre très grand, label small dessous.
- Chaque métrique accompagnée de son contexte (avant/après, période, source).
- Pas de tableau brut sans visualisation ou commentaire.

---

## 7. Configurations de decks

### Deck commercial / proposition client

- Couverture : fond bleu #3D65E8, titre de mission, nom du client
- 8-12 slides maximum
- Pas de slide de sommaire
- Fermeture sur prochaine étape précise (date, action, contact)

### Deck de cas / case study

- Couverture : fond bleu #3D65E8 + titre + année
- Structure : contexte, décisions, résultats, learnings
- Stat callouts pour métriques clés
- Screenshots en pleine largeur sur slides dédiées (LAYOUT 14 ou 15)

### Deck de formation UX / design

- Chapitres avec slides de transition (LAYOUT 02)
- Exercices visuellement différenciés (fond légèrement différent)
- Timeline de session en slide d'ouverture
- Une notion par slide, illustration systématique

### Pitch / keynote

- Maximum 10 slides
- Une stat ou idée forte par slide
- Pas de bullets : narration visuelle uniquement
- Big Ideas (LAYOUT 03) en alternance avec visuals (LAYOUT 14 ou 15)

---

## 8. Anti-patterns à éviter

- Bullets denses sur fond blanc sans structure visuelle
- Texte centré sur slides de contenu
- Mélange de polices
- Icônes emoji
- Ligne décorative sous les titres (signature IA générique)
- Même layout répété sur plus de 3 slides consécutives
- Fond blanc pur #FFFFFF comme fond global
- Gradient trop saturé ou visible au premier coup d'œil

---

## 9. Vérification avant livraison

1. Logo présent : logotype en couverture, symbole en footer des slides de contenu.
2. Palette conforme à la charte du projet (par défaut : #295FEC pour le logo, #3D65E8 pour les accents, #F8F9FB pour le fond).
3. Gradient appliqué sur les slides de fond clair.
4. Typographie Inter uniquement, hiérarchie de poids respectée.
5. Un élément dominant par slide, espace blanc respecté.
6. Titres affirmatifs et spécifiques.
7. Arc narratif lisible en ne lisant que les titres.
8. Zéro emoji, zéro emdash, zéro ligne décorative sous titre.
9. Sandwich couverture/conclusion fond bleu respecté.
10. QA visuel effectué sur chaque slide (export en images, relecture).
