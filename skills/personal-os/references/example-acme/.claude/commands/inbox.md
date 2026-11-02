---
description: Traiter les fichiers déposés dans inbox/ (journal, décisions, actions, faits, fiches, changelog, archivage)
argument-hint: [nom d'un fichier de inbox/, facultatif]
---
Traite ce qui est déposé dans `inbox/`. Si un nom de fichier est donné ici, traite uniquement celui-ci : $ARGUMENTS. Sinon, traite les fichiers un par un, dans l'ordre, et présente chaque cas séparément.

Utilise l'agent `inbox-ingestion` et suis le protocole de `CLAUDE.md`.

1. Liste `inbox/` en ignorant `README.md`. S'il n'y a rien, dis-le et arrête-toi.
2. Lis chaque fichier en entier. Donne un verdict par fichier : à traiter, déjà traité, dérivé, hors sujet, en attente.
3. Pour chaque fichier à traiter, présente la liste numérotée de modifications (fichier, avant, après, source, statut), les actions « possibles, non retenues » et les points à reconfirmer.
4. N'écris rien tant que je n'ai pas écrit « valide tout » ou une liste de numéros.
5. Après validation : écris, relance `python3 scripts/build_views.py`, ajoute l'entrée de `CHANGELOG.md`, déplace l'original vers `archive/`, puis liste ce qui a été fait.

Contexte Acme : l'inbox reçoit surtout les transcriptions du point hebdomadaire Portal et Insights. Le fichier d'exemple est `inbox/2026-03-12_sync-portal.txt`.
