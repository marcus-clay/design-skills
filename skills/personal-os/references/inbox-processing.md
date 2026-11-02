# Traitement d'un fichier d'inbox

Ce protocole décrit ce que Claude fait quand un fichier est déposé dans `inbox/`. Il s'applique à la commande `/inbox` et à l'agent `inbox-ingestion`. Les règles de fond sont dans `ingestion-rules.md`.

## Vue d'ensemble

1. **Lire** le fichier en entier.
2. **Classer** : à traiter, déjà traité, dérivé, hors sujet, en attente.
3. **Proposer** une liste numérotée de modifications.
4. **Valider** : rien n'est écrit sans ton accord explicite.
5. **Écrire** exactement ce qui a été validé.
6. **Archiver** l'original.
7. **Tracer** dans le journal, le changelog et la liste de propagation.

## 1. Lire

- Lire le fichier en entier, y compris la fin. Un fichier lu à moitié donne des décisions fausses.
- Relire `CLAUDE.md`, `06_resources/glossary.md` et `03_team/directory.md` avant d'interpréter les noms.
- Si le fichier est illisible (image sans texte, format inconnu), ne rien déduire : le déplacer vers `_to-decide/` avec une question.
- Repérer les passages douteux de la transcription (noms inconnus, mots qui n'ont pas de sens dans le contexte) et chercher une déformation phonétique.

## 2. Classer

Donner un seul verdict par fichier, avec une ligne de raison.

| Verdict | Signification | Suite |
|---|---|---|
| À traiter | Réunion, note ou document qui apporte un fait nouveau | Étapes 3 à 7 |
| Déjà traité | Le contenu est déjà dans le journal ou l'archive | Archiver, avec renvoi vers l'endroit traité |
| Dérivé | Résumé ou préparation produit à partir du brain | Archiver, ne router aucun fait |
| Hors sujet | Sans lien avec le brain | Demander s'il faut l'archiver ou le ranger ailleurs |
| En attente | Il manque une date, un auteur ou une confirmation | `_to-decide/`, avec la question |

## 3. Proposer

La proposition est une liste numérotée. Chaque ligne donne :

- le **fichier** à modifier et la **section** ;
- l'**avant** (cité) et l'**après** (texte exact) ;
- la **source** (fichier d'inbox, passage, date) ;
- le **statut** (fait, décidé, engagé, envisagé, à reconfirmer).

Les blocs de la proposition, dans cet ordre :

1. Entrée de **journal** (domaine entre crochets, `→` `?` `!`).
2. **Décisions** pour le registre (contexte, décision, raison, conséquences).
3. **Faits datés** pour la chronologie.
4. **Faits durables** pour les fichiers de domaine (en mettant à jour la page existante).
5. **Actions** pour le board, avec porteur et horizon. Les actions déduites par Claude sont dans une liste à part, « possibles, non retenues ».
6. Mise à jour des **fiches de sujets** (statut, porteur, prochaine action).
7. Ligne de **changelog** pour chaque page externe touchée (ajouter ou remplacer).
8. **Points à reconfirmer** (noms, dates, ambiguïtés).

## 4. Valider

Tant que le message ne contient pas « valide tout » ou une liste de numéros (« valide 1, 2, 4 »), aucun fichier n'est modifié. Si tu corriges une ligne, Claude la reprend et redemande.

## 5. Écrire

- Appliquer exactement les modifications validées, rien d'autre.
- Ajouter à la fin pour les historiques, corriger en place pour les synthèses (ancienne valeur entre parenthèses, avec sa date).
- Relancer `python3 scripts/build_views.py` si une fiche a changé.
- Vérifier par une relecture rapide que chaque fichier contient bien le texte attendu et que sa taille est plausible.

## 6. Archiver

Déplacer l'original de `inbox/` vers `archive/` dès que l'écriture est terminée, sous le même nom. Ne rien supprimer. Si l'écriture a échoué en partie, laisser l'original dans `inbox/` et le dire.

## 7. Tracer

- `CHANGELOG.md` : une entrée datée, page par page, avec « ajouter » (coller à la fin) ou « remplacer » (paragraphe identifié).
- Journal : l'entrée du jour renvoie vers les fichiers de domaine sans recopier les faits.
- S'il reste des fichiers à mettre à jour plus tard (propagation), les noter dans `_to-decide/propagation.md`.

## Exemple complet

Fichier déposé : `inbox/2026-03-12_sync-portal.txt`, transcription d'un point de 25 minutes sur un produit fictif (le texte intégral est dans `example-acme/inbox/`).

**Étape 1, lecture.** Claude repère « Dina » : aucune Dina dans l'annuaire, Dana existe (VP Produit). Déformation probable. Il relève aussi la phrase « on pourrait peut-être décaler les filtres », qui n'est pas une décision.

**Étape 2, classement.** À traiter : réunion avec décision, actions et un fait qui contredit une note existante.

**Étape 3, proposition (extrait).**

```
1. 00_journal/journal.md, ajout de l'entrée du 12 mars 2026 [PROD]
2. 04_decisions/decision-register.md, ajout de D-003
   Contexte : volume de tickets de support sur la première connexion
   Décision : la checklist d'accueil v1 ne s'affiche que pour les nouveaux comptes
   Raison : limiter la charge technique avant l'été (dite par Riley)
   Conséquences : les comptes existants ne voient pas la checklist avant la v2
3. 02_product/products.md, correction en place
   Avant : API de filtres enregistrés prévue en juin 2026
   Après : prévue en avril 2026 (ancienne valeur : juin 2026, avant le 12 mars)
   Source : inbox/2026-03-12_sync-portal.txt, intervention de Riley
4. 01_steering/board.md, 3 actions
   → Morgan : préparer trois variantes de la checklist (horizon : semaine suivante)
   → Riley : confirmer la date de l'API par écrit (échéance donnée par Dana : vendredi 20 mars)
   → Sam : partager le brouillon avec Dana (horizon : cette semaine)
   Possibles, non retenues : mesurer le taux d'activation (déduit, non dit)
5. 05_scope/sheets/portal-onboarding.md, statut inchangé, prochaine action mise à jour
6. 00_journal/timeline.md, ajout de la date de décision
7. CHANGELOG.md, page « Portal, checklist d'accueil » : remplacer le paragraphe « Périmètre »
À reconfirmer : « Dina » (Dana ?), « décaler les filtres » (idée ou décision ?)
```

**Étape 4, validation.** Tu réponds : « valide tout, mais "Dina" tu l'écris Dana (à reconfirmer) ».

**Étapes 5 à 7.** Claude écrit les sept points, déplace le fichier vers `archive/`, ajoute la ligne de changelog et relance le script de vues. Le résultat est visible dans `example-acme/`.
