---
description: Propager un changement dans tous les contenus du brain et lister les reports externes
argument-hint: [le changement, avec sa date et sa source]
---
Un changement est survenu : $ARGUMENTS

1. Cherche dans tout le dossier (Grep) chaque endroit où l'ancienne valeur ou le sujet apparaît. Liste-les avec fichier et ligne.
2. Choisis le fichier source (celui où le fait doit vivre) et propose la correction en place, avec l'ancienne valeur entre parenthèses et sa date.
3. Pour chaque autre fichier, propose de renvoyer vers la source au lieu de recopier.
4. Propose, si besoin, une entrée de journal, de chronologie et de registre de décisions.
5. Liste dans `CHANGELOG.md` les pages externes à mettre à jour (ajouter ou remplacer) et les supports à reprendre à la main.
6. Présente la liste numérotée et attends « valide tout » ou des numéros. N'écris rien avant.
7. Après écriture, appelle l'agent `consistency-check` et rends son rapport.
