---
description: Revue hebdomadaire du board et du périmètre
argument-hint: [date du jour, facultatif]
---
Fais la revue hebdomadaire. Date du jour : $ARGUMENTS (si elle n'est pas donnée, demande-la).

1. Lance `python3 scripts/build_views.py` pour rafraîchir les vues.
2. Appelle l'agent `board-review` sur `01_steering/board.md`.
3. Appelle l'agent `consistency-check` sur le dossier.
4. Présente en un seul message : les échéances dépassées, les sujets en attente depuis plus de deux semaines, les incohérences à corriger, et trois questions pour moi.
5. Ne modifie aucun fichier. J'écrirai « applique » suivi des numéros si je veux des corrections.

Horizons du board d'Acme : cette semaine, semaine suivante, ce mois-ci, plus tard.
