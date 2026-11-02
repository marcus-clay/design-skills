---
name: personal-os
description: "OS personnel avec Claude Code. À utiliser pour créer ou faire évoluer un second cerveau (un « brain »), un dossier de fichiers Markdown qui sert de mémoire et de tableau de bord à Claude Code. Déclencher quand on veut structurer son travail, traiter une inbox (comptes rendus, transcriptions, notes), mettre en place des règles d'ingestion, des agents, des commandes ou des vues générées, préparer un 1:1, tenir un registre de décisions, ou propager un changement dans tous ses contenus."
---

# OS personnel avec Claude Code

Cette skill aide à construire un « brain » : un dossier de fichiers texte (au format Markdown, lisible dans n'importe quel éditeur) où Claude Code range ce que tu lui confies, retrouve ce qui a été décidé et prépare tes prochaines étapes. Elle guide pas à pas, avec des questions simples au départ et des modèles à copier ensuite.

Principe de lecture : suis les étapes dans l'ordre la première fois. Les fichiers de `references/` contiennent le détail et les modèles. Tu peux t'y reporter au fil de l'eau.

## 0. À quoi ça sert et ce qu'on obtient

Sans mémoire, chaque conversation avec Claude repart de zéro. Avec un brain, la conversation devient jetable et le dossier devient la mémoire : ce qui compte est écrit dans un fichier, et Claude relit les fichiers avant de répondre.

Ce qu'on obtient au bout de la mise en place :

- Une boîte de dépôt (`inbox/`) où tu glisses n'importe quelle matière brute : transcription de réunion, notes, mail copié, capture.
- Un traitement en quatre catégories : les décisions (avec leur raison), les actions (avec leur porteur), les faits nouveaux, les questions ouvertes.
- Un journal, un registre de décisions et une chronologie qui ne se réécrivent jamais : on ajoute, on ne modifie pas.
- Des fiches de sujets (un fichier par chantier) et des tableaux de synthèse régénérés par un petit script.
- Des agents spécialisés (ingestion, revue de board, vérification de cohérence, rédaction, préparation de 1:1, conseil sur une décision) et des commandes courtes (`/inbox`, `/journal`...).
- Un fichier de suivi des changements (`CHANGELOG.md`) qui dit quoi reporter dans un outil externe (wiki, outil de tickets, présentation).

Rien n'est écrit sans ton accord : Claude propose, tu valides, puis il écrit.

## 1. Prérequis

- Claude Code installé et fonctionnel sur ta machine (commande `claude` disponible dans un terminal).
- Un dossier vide, par exemple `~/brain`. Il sera la seule zone où Claude a le droit d'écrire pour ce projet.
- Python 3 pour le script de vues (facultatif, rien d'autre à installer).
- Un éditeur de texte qui ouvre le Markdown. Un dépôt Git est conseillé, car il permet de revenir en arrière, mais il n'est pas obligatoire.

Ouvre un terminal dans le dossier vide et lance `claude`.

## 2. L'entretien de départ

Claude pose ces sept questions, une par une, en attendant ta réponse à chacune. Les réponses courtes suffisent. Voici ce qu'il fait de chaque réponse.

| Question | Ce que Claude en fait |
|---|---|
| 1. Quel est ton rôle et ton équipe, en une phrase ? | Remplit la section « Qui je suis » de `CLAUDE.md` pour que Claude s'adresse à toi au bon niveau. |
| 2. Quels sont tes trois à cinq chantiers en cours ? | Crée une fiche de sujet par chantier dans `05_scope/sheets/`. |
| 3. Avec quelles personnes travailles-tu le plus (prénom, rôle) ? | Remplit `03_team/directory.md` et prépare la liste des noms à reconfirmer. |
| 4. Quelles matières reçois-tu (transcriptions, mails, notes, captures) ? | Règle le tri de `inbox/` et la liste des formats que Claude sait lire. |
| 5. Où doit être reporté ce que tu produis (wiki, outil de tickets, présentations) ? | Adapte `CHANGELOG.md` : une ligne par page à mettre à jour, avec « ajouter » ou « remplacer ». |
| 6. Dans quelle langue écris-tu, et quelles règles d'écriture veux-tu ? | Remplit la section « Style » de `CLAUDE.md`. |
| 7. À quel rythme veux-tu des revues (jour, semaine, avant un 1:1) ? | Choisit les commandes et agents à installer en premier (étape 5). |

Avant de continuer, Claude résume ce qu'il a compris en dix lignes et attend ton accord.

## 3. Créer la structure

Claude propose l'arborescence décrite dans `references/structure.md`, puis la crée après ton accord. Les dossiers de base sont :

- `inbox/` et `archive/` : le dépôt des matières brutes et leur rangement une fois traitées.
- `00_journal/` : journal et chronologie (ajout seulement).
- `01_steering/` : pilotage, avec le board de tâches.
- `02_product/` : faits durables sur les produits.
- `03_team/` : annuaire des personnes, notes de collaboration.
- `04_decisions/` : registre de décisions (ajout seulement).
- `05_scope/` : fiches de sujets et vues générées.
- `06_resources/` : lexique, documents de référence.
- `scripts/` : le script de vues.
- `.claude/` : agents et commandes.

Règle d'or : un fichier, un sujet, un nom neutre. Aucun fichier ne porte le nom d'une personne. Ce qui concerne une personne va dans l'annuaire.

Copie ensuite les modèles de `references/templates/` en remplaçant les champs entre crochets par tes réponses de l'étape 2.

## 4. Écrire le fichier d'instructions CLAUDE.md

`CLAUDE.md` est lu automatiquement par Claude Code à chaque session. Il contient les règles du jeu. Pars du modèle `references/templates/CLAUDE.md` et vérifie qu'il dit au moins :

1. Qui tu es et comment Claude doit s'adresser à toi.
2. Ce que Claude fait quand une information nouvelle arrive (le protocole d'ingestion, voir `references/ingestion-rules.md`).
3. La règle de fraîcheur, les fichiers en ajout seulement, la règle « un fait, un seul fichier ».
4. Les règles de sûreté de l'étape 9.
5. Le style d'écriture que tu as choisi à la question 6.
6. La liste des noms propres souvent déformés par les outils de transcription, à compléter au fil du temps.

Garde ce fichier court : une à deux pages. Le détail vit dans les fichiers de `references/`, que Claude lit au besoin.

## 5. Ajouter les agents et les commandes

Un agent est un assistant spécialisé qui a ses propres consignes et ses propres droits. Une commande est un raccourci que tu tapes dans Claude Code (par exemple `/inbox`). Les deux sont de simples fichiers Markdown dans `.claude/`.

Commence petit. Installe d'abord :

- l'agent `inbox-ingestion` et la commande `/inbox` (pour traiter ce que tu déposes) ;
- la commande `/journal` (pour consigner une note rapide).

Ajoute ensuite, quand le besoin se présente : `board-review`, `consistency-check`, `deliverables-writer`, `meeting-prep`, `decision-advisor`, et les commandes `/review-board`, `/prep-1to1`, `/propagate`. Le rôle de chacun est dans `references/agents.md`, les modèles à copier dans `references/templates/.claude/`.

Après chaque ajout, demande à Claude de vérifier que le fichier est lu : tape `/agents` pour voir la liste.

## 6. Premier essai : déposer une note et la faire traiter

1. Écris ou colle une note réelle (même courte) dans `inbox/`, par exemple `inbox/2026-01-15_point-equipe.txt`.
2. Tape `/inbox`.
3. Claude lit le fichier, repère les passages douteux, croise avec l'existant et te rend une liste numérotée de modifications proposées, avec pour chacune : le fichier, l'avant, l'après et la source.
4. Réponds « valide 1, 2, 4 » ou « valide tout ». Sans réponse claire, rien n'est écrit.
5. Claude écrit, déplace l'original dans `archive/`, note ce qui a été fait dans `CHANGELOG.md` et relance le script de vues.

Le protocole complet est dans `references/inbox-processing.md`. Un exemple de bout en bout, avec la note brute et le résultat, est dans `references/example-acme/`.

## 7. Les routines

Quatre rythmes suffisent pour commencer.

- **Chaque jour (5 minutes).** Dépose ce qui est arrivé dans `inbox/`, tape `/inbox`, valide. En fin de journée, tape `/journal` pour une note libre.
- **Après une réunion.** Dépose la transcription ou tes notes, tape `/inbox`. Vérifie en priorité les décisions et leur raison, puis les actions et leur porteur.
- **Chaque semaine.** Tape `/review-board`, puis demande à l'agent `consistency-check` de contrôler dates, statuts et noms. Relance le script de vues.
- **Avant un 1:1.** Tape `/prep-1to1 [prénom]`. L'agent `meeting-prep` rassemble ce qui a été dit, ce qui est en attente et les questions ouvertes, avec la source de chaque ligne.

## 8. Faire évoluer

- **Ajouter un sujet.** Copie `references/templates/scope-sheet.md` dans `05_scope/sheets/`, remplis les champs, puis lance le script de vues.
- **Ajouter un agent.** Copie un modèle de `references/templates/.claude/agents/`, change son nom, sa description et ses consignes. Teste-le sur un cas réel avant de l'adopter.
- **Ajouter une vue.** Écris ou fais écrire un petit script qui lit les fiches et produit un tableau. Il lit, il ne modifie jamais les fiches. Le script `references/scripts/build_views.py` sert de point de départ.
- **Un changement touche plusieurs contenus.** Utilise `/propagate` (voir le cas d'usage dans `references/use-cases.md`).

Avant d'ajouter quoi que ce soit, pose-toi quatre questions. Est-ce que cela m'évite de perdre une décision et sa raison ? Est-ce que cela me dit la prochaine action et son porteur sur chaque chantier ? Est-ce que cela réduit l'effort pour passer d'un sujet à un autre ? Est-ce que cela laisse une trace utile à mon équipe ? Si la réponse est non partout, ne l'ajoute pas.

## 9. Règles de sûreté

1. **Propose, valide, écrit.** Claude présente d'abord ce qu'il compte modifier. Il n'écrit qu'après ton accord explicite.
2. **Ne jamais inventer.** Une décision ou une action qui n'est pas dans le texte n'est pas créée. Si la raison d'une décision manque, on écrit « raison non documentée ».
3. **Signaler le doute.** Quand un passage est ambigu ou qu'un nom ressemble à une déformation de transcription, Claude le dit et pose la question au lieu de trancher.
4. **Ne rien supprimer sans accord.** Aucun fichier n'est supprimé ni déplacé hors du flux prévu (inbox vers archive) sans que tu l'aies demandé.
5. **Distinguer le fait, l'engagement et l'idée.** Ce qui est fait, ce que tu as promis à quelqu'un et ce que tu envisages sont trois statuts différents. Une suggestion de Claude n'est jamais présentée comme un engagement.
6. **Garder la provenance.** Chaque ligne importante renvoie à sa source (fichier, date).

## Liste de vérification

- [ ] `claude` démarre dans le dossier du brain et lit `CLAUDE.md`.
- [ ] Les sept questions de l'étape 2 ont reçu une réponse et un résumé validé.
- [ ] Les dossiers de l'étape 3 existent, sans fichier au nom d'une personne.
- [ ] Le journal, le registre de décisions et la chronologie sont déclarés « ajout seulement » dans `CLAUDE.md`.
- [ ] La règle de fraîcheur et la règle « un fait, un seul fichier » figurent dans `CLAUDE.md`.
- [ ] L'agent `inbox-ingestion` et la commande `/inbox` apparaissent dans `/agents` et dans la liste des commandes.
- [ ] Un premier essai a été mené jusqu'au bout : proposition, validation, écriture, archivage, ligne de `CHANGELOG.md`.
- [ ] `python3 scripts/build_views.py` s'exécute sans erreur et produit les vues.
- [ ] Les quatre routines de l'étape 7 sont notées quelque part que tu consultes.
- [ ] Les règles de sûreté de l'étape 9 sont copiées dans `CLAUDE.md`.

## Fichiers de la skill

| Fichier | Contenu |
|---|---|
| `references/structure.md` | Arborescence recommandée et rôle de chaque dossier |
| `references/ingestion-rules.md` | Règles d'ingestion, avec exemples avant et après |
| `references/inbox-processing.md` | Protocole de traitement d'un fichier d'inbox, exemple complet |
| `references/agents.md` | Catalogue des six agents |
| `references/use-cases.md` | Sept scénarios d'usage |
| `references/templates/` | Modèles à copier (instructions, board, registre, journal, fiches, agents, commandes) |
| `references/scripts/build_views.py` | Script de génération des vues |
| `references/example-acme/` | Brain d'exemple complet et fictif |
