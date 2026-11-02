# Structure recommandée du brain

Cette arborescence est un point de départ. Les numéros en tête de dossier servent à les garder dans un ordre stable dans l'explorateur de fichiers. Renomme ce que tu veux, à condition de garder les mêmes rôles et de mettre à jour `CLAUDE.md`.

```
brain/
  CLAUDE.md                  règles lues par Claude Code à chaque session
  README.md                  index pour les humains
  CHANGELOG.md               ce qu'il faut reporter dans les outils externes
  inbox/                     matières brutes à traiter
  archive/                   originaux traités (jamais modifiés)
  00_journal/
    journal.md               journal daté (ajout seulement)
    timeline.md              faits datés (ajout seulement)
    activity/                vues générées jour par jour
  01_steering/
    board.md                 tâches par horizon
  02_product/                un fichier par produit ou par thème
  03_team/
    directory.md             annuaire des personnes
    collaboration-notes.md   contexte relationnel, une sous-section par personne
  04_decisions/
    decision-register.md     décisions et raisons (ajout seulement)
  05_scope/
    sheets/                  une fiche par sujet
    views/                   tableaux générés (ne pas éditer)
  06_resources/
    glossary.md              lexique et noms à reconfirmer
  _to-decide/                ce qui attend une réponse
  scripts/
    build_views.py
  .claude/
    agents/                  un fichier par agent
    commands/                un fichier par commande
```

## Rôle de chaque dossier

**`inbox/`** reçoit tout ce qui est brut : transcription, notes, mail copié, capture d'écran. Aucun traitement n'y est fait à la main. On y dépose, Claude traite. Le dossier doit être vide ou presque après chaque passage.

**`archive/`** garde l'original de chaque fichier traité, sous le même nom, daté. C'est la source en cas de doute sur ce qui a vraiment été dit. On ne modifie jamais un fichier archivé.

**`00_journal/`** contient les historiques. Le journal raconte ce qui s'est passé, jour par jour, avec des renvois vers les fichiers où vivent les faits. La chronologie liste les événements datés (lancement, décision, jalon). Les deux fonctionnent en ajout seulement. Le sous-dossier `activity/` reçoit les vues générées par script, jamais écrites à la main.

**`01_steering/`** est le pilotage : le board de tâches, classées par horizon (cette semaine, semaine suivante, mois, plus tard). Une tâche a un porteur et une source. Une échéance n'est posée que si une tierce personne l'a donnée.

**`02_product/`** décrit ce qui dure : produits, offres, fonctionnement, contraintes. Un fichier par produit ou par thème. Un fait durable vit ici et nulle part ailleurs.

**`03_team/`** contient l'annuaire (tableau : prénom, rôle, périmètre, dernière mise à jour) et les notes de collaboration (comment travailler avec chaque personne, ses attentes connues). Une information sur une personne va là, jamais dans un fichier à son nom.

**`04_decisions/`** contient le registre. Chaque entrée a quatre champs : contexte, décision, raison, conséquences. La raison est le champ le plus important. Si elle n'est pas connue, on écrit « raison non documentée ».

**`05_scope/`** décrit le périmètre, c'est-à-dire l'ensemble des sujets suivis. Chaque sujet a une fiche dans `sheets/` avec un petit en-tête structuré (identifiant, statut, porteur, prochaine action, horizon, source). Le script `build_views.py` lit ces fiches et écrit des tableaux dans `views/`. Les fiches sont la source, les vues sont des dérivés.

**`06_resources/`** garde les documents de référence : lexique, glossaire, modèles de documents, noms de personnes ou de produits à reconfirmer.

**`_to-decide/`** reçoit ce que Claude ne peut pas traiter seul : fichier illisible, date manquante, auteur inconnu, contradiction à arbitrer. Chaque élément y est accompagné d'une question.

**`scripts/`** contient les petits programmes qui produisent les vues. Ils lisent les fichiers, ils n'écrivent que dans les dossiers de vues.

**`.claude/`** contient la configuration de Claude Code : `agents/` pour les assistants spécialisés, `commands/` pour les raccourcis.

## Principe : un fichier, un sujet, un nom neutre

- Un fichier traite d'un seul sujet. Si un fichier commence à mélanger deux sujets (une personne et un chantier, par exemple), on le signale et on propose de le séparer.
- Le nom du fichier est neutre et décrit le sujet : `decision-register.md`, `onboarding-checklist.md`. Jamais un prénom, jamais une date dans un fichier de synthèse.
- Un fait vit dans un seul fichier. Les autres y renvoient par un lien ou une mention, ils ne le recopient pas.
- Les fichiers de synthèse se corrigent en place. Les historiques (journal, registre, chronologie) ne se réécrivent jamais.
- Les outils externes (wiki, outil de tickets, messagerie) sont des vues du brain. La source reste dans le dossier.

## Ce qu'il ne faut pas y mettre

- Des documents qui existent déjà ailleurs et qui n'ont pas de lien avec le suivi : on les référence, on ne les copie pas.
- Des volumes écrits à la main (« 42 fiches »). Un chiffre annoncé finit toujours par ne plus coller. On le calcule par script ou on ne l'écrit pas.
- Des informations sensibles qui n'ont pas à être dans un dossier de travail (mots de passe, données personnelles inutiles).
