# CLAUDE.md, instructions pour Claude Code

Ce dossier est le brain de travail de [Prénom], [rôle] dans [équipe ou entreprise]. `README.md` est l'index pour les humains ; ce fichier s'adresse à toi, Claude.

## Qui je suis

[Une à trois phrases : rôle, équipe, ce que tu attends de Claude.]

## Quand une information nouvelle arrive

Quand [Prénom] partage un compte rendu, une note, une transcription ou tout autre élément nouveau :

1. Ajouter une entrée datée dans `00_journal/journal.md`. Domaine entre crochets, symboles `→` (action), `?` (question), `!` (point de vigilance), rien devant un fait brut. Les décisions s'écrivent en toutes lettres.
2. Extraire les actions et les proposer pour `01_steering/board.md`, avec leur porteur. Ne jamais fixer d'échéance sauf si un tiers l'a donnée.
3. Router les décisions vers `04_decisions/decision-register.md` (contexte, décision, raison, conséquences ; « raison non documentée » si absente). Router les faits datés vers `00_journal/timeline.md` et les faits durables vers le fichier de domaine concerné, en mettant à jour la page existante.
4. Mettre à jour la fiche du sujet dans `05_scope/sheets/` puis lancer `python3 scripts/build_views.py`.
5. Ne jamais répéter un fait déjà écrit ailleurs : renvoyer vers le fichier.
6. Ajouter une entrée dans `CHANGELOG.md`, page par page, avec « ajouter » ou « remplacer ».
7. Archiver l'original de `inbox/` vers `archive/` une fois l'écriture terminée.

## Règles de fonctionnement

- La conversation est jetable, le dossier est la mémoire. Lire les fichiers avant de répondre sur un sujet du brain.
- Séparer à l'ingestion quatre catégories : décisions (avec leur raison), actions (avec leur porteur), faits nouveaux, questions ouvertes.
- Historiques en ajout seulement : journal, registre de décisions, chronologie.
- Règle de fraîcheur : la source la plus récente et la plus officielle l'emporte. Corriger en place, garder l'ancienne valeur entre parenthèses avec sa date.
- Un fait vit dans un seul fichier.
- Aucun volume annoncé à la main : calculer par script ou ne pas l'écrire.
- Un seul écrivain par fichier à la fois.

## Sûreté

- Proposer d'abord, écrire après validation explicite.
- Ne jamais inventer une décision, une action ou une échéance. Signaler l'ambiguïté plutôt que trancher.
- Ne rien supprimer ni déplacer sans accord, hors du flux inbox vers archive.
- Distinguer ce qui est fait, ce qui est engagé devant quelqu'un et ce qui est envisagé. Une suggestion de Claude n'est jamais présentée comme engagée.
- Chaque fait écrit porte sa source.

## Convention de domaines

[PIL] Pilotage · [PROD] Produit · [EQ] Équipe · [OUT] Outils · [VEILLE] Veille · [Ajouter les tiens]

## Style d'écriture

- Langue : [français]. Typographie : [accents sur les majuscules, guillemets « », espace insécable avant : ; ? !].
- Phrases complètes, ton simple, sans jargon devant des lecteurs extérieurs au métier.
- [Tes autres règles : mots à éviter, format des dates, etc.]

## Vigilance transcription

Les outils de transcription déforment certains noms. Avant de créer une personne, chercher une déformation phonétique dans `03_team/directory.md` et `06_resources/glossary.md`. Ne jamais corriger un nom de mémoire.

[Noms déformés connus : graphie observée → graphie probable]

## Principe de structuration

Un fichier, un sujet, un nom neutre. Aucun fichier ne porte le nom d'une personne. Une information sur une personne va dans `03_team/directory.md` ou `03_team/collaboration-notes.md`.

## Ce que ce brain ne couvre pas

[Documents qui restent ailleurs pour éviter la duplication.]
