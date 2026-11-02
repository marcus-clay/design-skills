# Brain d'Acme Corp (exemple fictif)

Dossier de travail de Sam, head of design chez Acme Corp. Entreprise, personnes, produits et dates sont inventés. Ce fichier est l'index pour les humains ; les règles pour Claude Code sont dans `CLAUDE.md`.

## Par où commencer

| Je veux | J'ouvre |
|---|---|
| Voir mes tâches | `01_steering/board.md` |
| Retrouver une décision et sa raison | `04_decisions/decision-register.md` |
| Savoir où en est un sujet | `05_scope/views/by-status.md` |
| Voir ce qui attend chaque personne | `05_scope/views/by-owner.md` |
| Retrouver ce qui s'est passé un jour donné | `00_journal/journal.md` |
| Savoir qui est qui | `03_team/directory.md` |
| Savoir quoi reporter dans les outils externes | `CHANGELOG.md` |

## L'exemple de traitement

Le fichier `inbox/2026-03-12_sync-portal.txt` est une transcription brute, laissée dans `inbox/` pour montrer l'état de départ. Après traitement, il irait dans `archive/` : les sources citées dans le brain portent déjà ce chemin final. Le résultat attendu est détaillé dans `processing-result.md`, et on le retrouve dans le journal, le registre, la chronologie, le board, les fiches, le fichier produit et le changelog.

## Routines

- Chaque jour : déposer dans `inbox/`, taper `/inbox`, valider.
- Chaque semaine : `/review-board`, puis l'agent `consistency-check`.
- Avant un 1:1 : `/prep-1to1 Dana` (ou Riley, Morgan).

Les volumes ne sont pas écrits ici : `scripts/build_views.py` les calcule.
