---
description: Ajouter une entrée au journal à partir d'une note libre
argument-hint: [note en une ou deux phrases, facultatif]
---
Ajoute une entrée datée à `00_journal/journal.md` à partir de ce que je dis : $ARGUMENTS

Si je n'ai rien écrit, demande-moi ce qui s'est passé aujourd'hui.

1. Propose l'entrée (domaine entre crochets, symboles `→` `?` `!`, rien devant un fait brut, décisions en toutes lettres) et montre-la avant d'écrire.
2. Si un fait existe déjà dans un fichier de domaine, renvoie vers ce fichier au lieu de le recopier.
3. Si la note contient une décision, une action ou un fait daté, propose aussi le routage vers le registre, le board ou la chronologie, sans l'appliquer.
4. N'écris qu'après mon accord, et seulement à la fin du fichier.
