# [Nom du brain]

Dossier de travail de [Prénom], [rôle]. Ce fichier est l'index pour les humains. Les règles pour Claude Code sont dans `CLAUDE.md`.

## Par où commencer

| Je veux | J'ouvre |
|---|---|
| Voir mes tâches | `01_steering/board.md` |
| Retrouver une décision et sa raison | `04_decisions/decision-register.md` |
| Savoir où en est un sujet | `05_scope/views/by-status.md` |
| Voir ce qui m'attend, par personne | `05_scope/views/by-owner.md` |
| Retrouver ce qui s'est passé un jour donné | `00_journal/journal.md` |
| Savoir qui est qui | `03_team/directory.md` |
| Savoir quoi reporter dans les outils externes | `CHANGELOG.md` |

## Routines

- Chaque jour : déposer dans `inbox/`, taper `/inbox`, valider.
- Après une réunion : déposer la transcription, taper `/inbox`.
- Chaque semaine : `/review-board`, puis l'agent `consistency-check`.
- Avant un 1:1 : `/prep-1to1 [prénom]`.

## Règles en une ligne

Proposer, valider, écrire. Un fait, un seul fichier. Les historiques s'écrivent en ajout seulement.

Les volumes ne sont pas écrits ici : ils sont calculés par `scripts/build_views.py`.
