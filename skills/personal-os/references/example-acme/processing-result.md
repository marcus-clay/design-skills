# Résultat attendu du traitement de `inbox/2026-03-12_sync-portal.txt`

Ce fichier montre ce que Claude propose (liste numérotée) et ce qui est écrit après la réponse « valide tout ». Les fichiers du brain d'exemple sont déjà dans l'état « après » ; chaque ligne ci-dessous dit où le retrouver.

## Verdict

À traiter. Réunion de 25 minutes avec une décision, trois actions, un fait qui corrige une note existante et deux questions ouvertes.

## Ce que Claude a repéré avant de proposer

- **Nom douteux.** À 09:45, « Dina » parle. L'annuaire ne contient aucune Dina, mais Dana est présente et la phrase correspond à son rôle (elle demande une confirmation pour le comité). Déformation probable. Claude écrit « Dana (à reconfirmer) » et ne crée aucune personne.
- **Idée présentée comme décision ?** À 13:15, « on pourrait peut-être décaler les filtres à l'été » n'est pas une décision. Elle devient une question ouverte.
- **Date ambiguë.** « Avant vendredi prochain » dit un jeudi peut désigner le 13 ou le 20 mars. Claude retient le 20 mars, signale le doute et le dit dans le board.
- **Engagement flou.** Morgan dit « je peux vérifier » les noms de jetons : une offre, pas un engagement. Elle va dans « possibles, non retenues ».

## Liste proposée et résultat

| N° | Fichier | Avant | Après | Source |
|---|---|---|---|---|
| 1 | `00_journal/journal.md` | (fin du fichier : entrée du 10 février) | Entrée du 12 mars 2026 avec `→`, `?`, `!`, renvois sans recopie | Fichier d'inbox entier |
| 2 | `04_decisions/decision-register.md` | D-001 et D-002 | Ajout de D-003 (contexte, décision, raison, conséquences) | 03:30 à 05:00 |
| 3 | `00_journal/timeline.md` | Deux lignes | Deux lignes ajoutées le 2026-03-12 | 05:00 et 09:00 |
| 4 | `02_product/products.md` | « API de filtres enregistrés : prévue en juin 2026 » | « disponibilité prévue en avril 2026 (ancienne valeur : juin 2026, avant le 12 mars 2026) » | 09:00, Riley |
| 5 | `01_steering/board.md` | Aucune de ces tâches | Quatre tâches (Sam deux fois, Riley, Morgan) et trois lignes « possibles, non retenues » | 05:40, 06:20, 10:05, 21:20 |
| 6 | `05_scope/sheets/` (trois fiches) | Fiches créées lors de l'entretien de départ, sans mise à jour du jour | Statut, porteur et prochaine action mis à jour ; ligne ajoutée à l'historique | Fichier d'inbox |
| 7 | `06_resources/glossary.md` | Section « À reconfirmer » vide | Ligne « Dina, probablement Dana » | 09:45 |
| 8 | `CHANGELOG.md` | Entrée du 10 février | Entrée du 12 mars : trois pages externes (deux « remplacer », une « ajouter ») | Décision et fait corrigé |
| 9 | `archive/` | Original dans `inbox/` | Déplacé vers `archive/` après écriture | |

Après l'écriture, `python3 scripts/build_views.py` a régénéré `05_scope/views/by-status.md` et `by-owner.md`.

## Les quatre catégories, telles qu'elles ont été séparées

**Décision** : checklist v1 pour les nouveaux comptes seulement (D-003). Raison donnée : pas de capacité technique avant juillet pour migrer les comptes existants.

**Actions** (avec porteur) :
- Morgan : trois variantes de la checklist, la semaine suivante (dit par Morgan, 06:00)
- Sam : partager le brouillon avec Dana, cette semaine (dit par Sam, 06:35)
- Riley : confirmer la date de l'API par écrit, échéance demandée par Dana (« Dina »), à reconfirmer
- Sam : demander à Riley qui est propriétaire des retours de l'étude client (dit par Sam, 21:20)

**Fait nouveau** : l'API de filtres enregistrés passe de juin à avril (information la plus récente, donnée par la personne qui pilote la technique).

**Questions ouvertes** : décalage des filtres à l'été (non tranché) ; propriétaire des retours de l'étude client ; pertinence d'une table de correspondance pour les jetons.

## Points laissés à Sam

1. Confirmer que « Dina » est bien Dana.
2. Confirmer que l'échéance est le vendredi 20 mars.
3. Prendre ou écarter les trois lignes « possibles, non retenues ».

## Ce qu'un contrôle de cohérence trouverait ensuite

Lancé après l'ingestion, l'agent `consistency-check` vérifie que la date d'avril n'est écrite que dans `02_product/products.md` (hors changelog, qui contient le texte à coller), que les fiches et le board disent la même chose, et que « Dina » n'apparaît dans aucun fichier de domaine.
