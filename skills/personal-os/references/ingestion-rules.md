# Règles d'ingestion

L'ingestion est le moment où une information nouvelle (compte rendu, transcription, note, mail) entre dans le brain. Ces règles sont courtes pour être appliquées à chaque fois. Copie-les dans `CLAUDE.md` ou renvoie-y.

## 1. Les quatre catégories

À la lecture d'un texte, Claude sépare quatre sortes d'éléments et ne les mélange jamais.

| Catégorie | Définition | Où elle va |
|---|---|---|
| Décision | Un choix a été fait, par quelqu'un qui a le droit de le faire | `04_decisions/decision-register.md`, avec contexte, décision, raison, conséquences |
| Action | Quelqu'un doit faire quelque chose | `01_steering/board.md`, avec son porteur et son horizon |
| Fait nouveau | Une information vraie, utile, qui n'est pas une décision ni une action | Le fichier de domaine concerné, et `00_journal/timeline.md` s'il est daté |
| Question ouverte | Un point que personne n'a tranché | Le journal (symbole `?`), et la fiche du sujet |

Le champ le plus important est la **raison** d'une décision. Sans raison, la décision se rediscute dans trois mois. Si la raison n'est pas dans le texte, on écrit « raison non documentée » et on la demande.

## 2. Notation du journal

Chaque entrée du journal porte un domaine entre crochets, par exemple `[PROD]`. Ensuite :

- `→` devant une action ;
- `?` devant une question ouverte ;
- `!` devant un point de vigilance ;
- rien devant un fait brut.

Les décisions s'écrivent en toutes lettres (« Décision : ... »), sans symbole.

## 3. Les historiques s'écrivent en ajout seulement

Le journal, le registre de décisions et la chronologie ne se réécrivent pas. On ajoute à la fin. Si une décision est changée plus tard, on ajoute une nouvelle entrée qui renvoie à l'ancienne, on ne modifie pas l'ancienne.

Les fichiers de synthèse (fiches, annuaire, fichiers de produits), eux, se corrigent en place.

Avant, dans le registre :

```
D-002 | 2026-02-10 | Revue de design le mardi
```

Après un changement (ajout d'une entrée, l'ancienne reste intacte) :

```
D-002 | 2026-02-10 | Revue de design le mardi
D-006 | 2026-05-04 | Revue de design le jeudi (remplace D-002)
```

## 4. La règle de fraîcheur

Quand deux informations se contredisent, la plus récente et la plus officielle l'emporte. On corrige le fichier de synthèse en place, on garde l'ancienne valeur entre parenthèses avec sa date.

Avant :

```
Disponibilité de l'API de filtres : juin 2026
```

Après (information donnée le 12 mars par la personne qui pilote la technique) :

```
Disponibilité de l'API de filtres : avril 2026 (ancienne valeur : juin 2026, avant le 12 mars 2026)
```

« Plus officielle » veut dire : un document validé l'emporte sur une conversation, une personne responsable du sujet l'emporte sur un avis extérieur. En cas de doute sur l'autorité, Claude signale le conflit et demande.

## 5. Un fait vit dans un seul fichier

Quand un fait existe déjà dans un fichier de domaine, le journal et les autres fichiers y renvoient. Ils ne le recopient pas.

Avant (fait recopié à trois endroits, qui se désynchronisent) :

```
journal.md       : « L'équipe passe à 4 designers. »
directory.md     : « Équipe design : 4 personnes. »
README.md        : « 4 designers. »
```

Après (le fait vit dans l'annuaire, le reste renvoie) :

```
journal.md       : « Arrivée d'une designer, voir 03_team/directory.md. »
directory.md     : tableau à jour (source unique)
README.md        : « Équipe : voir 03_team/directory.md. »
```

De la même façon, les volumes (« 12 sujets ») ne s'écrivent pas à la main : le script de vues les calcule.

## 6. Les noms propres à reconfirmer

Les outils de transcription déforment les noms de façon récurrente (une personne devient un autre prénom proche, un outil devient un mot courant). Règles :

1. Si un nom ne correspond à personne de connu, chercher d'abord une déformation phonétique dans l'annuaire et le lexique.
2. Ne jamais corriger de mémoire. Proposer la correction, indiquer le doute, demander confirmation.
3. Les noms douteux sont notés dans `06_resources/glossary.md`, section « À reconfirmer », avec la graphie observée, la graphie probable et la source.
4. Une personne n'est créée dans l'annuaire que si sa présence est confirmée.

Exemple. Dans la transcription : « Dina confirme que la maquette part vendredi. » L'annuaire contient Dana (VP Produit) et aucune Dina. Claude écrit dans sa proposition : « "Dina" est probablement Dana (déformation phonétique). À reconfirmer. En attendant, je note "Dana (à reconfirmer)". »

## 7. Ne jamais inventer une décision ou une action

- Une décision n'existe que si le texte dit qu'elle a été prise (« on part sur... », « c'est validé »). Une idée évoquée (« on pourrait... ») est une question ouverte ou un fait, pas une décision.
- Une action n'existe que si quelqu'un l'a formulée ou acceptée. Ce que Claude déduit lui-même va dans une liste séparée, « possibles, non retenues », pour que tu les prennes ou les écartes.
- Une échéance n'est posée que si elle a été donnée par un tiers ou par un document officiel. Sinon, l'action reçoit un horizon large (« ce mois-ci », « plus tard »).
- On ne présente jamais une suggestion de Claude comme un engagement de la personne.

Avant / après :

Texte : « Peut-être qu'on pourrait repousser les filtres à l'été, on verra. »

Mauvais traitement : « Décision : les filtres sont repoussés à l'été. »

Bon traitement : « ? Les filtres pourraient être repoussés à l'été (évoqué, non tranché). Personne n'a décidé. »

## 8. Signaler l'ambiguïté plutôt que trancher

Quand un passage peut se lire de deux façons, Claude écrit les deux lectures et pose la question. Exemples d'ambiguïtés : un « on » sans sujet clair (qui s'engage ?), une date sans année, un pronom (« il valide » : qui ?), un chiffre contradictoire entre deux phrases.

## 9. Provenance de chaque ligne

Chaque fait écrit dans un fichier de synthèse porte sa source : le nom du fichier d'inbox (ou de l'archive), la date, et si utile le passage. Format conseillé en fin de ligne : `(source : archive/2026-03-12_sync.txt, 12 mars)`.

Une ligne ne renvoie jamais à un document dérivé (une préparation, un résumé) mais à l'original. Les documents que Claude a lui-même produits ne sont pas des sources : aucun fait n'en est extrait.

## 10. Les statuts

Un élément porte l'un de ces statuts, et un seul : **fait** (c'est arrivé), **décidé** (choix enregistré dans le registre), **engagé** (tu t'es engagé devant quelqu'un), **envisagé** (tu y penses, rien n'est promis), **à reconfirmer** (source douteuse). Ne jamais faire monter un élément d'un statut à l'autre sans un texte qui le justifie.

## 11. Résumé en huit lignes (à copier dans CLAUDE.md)

1. Lire les fichiers avant de répondre sur un sujet du brain.
2. Séparer décisions, actions, faits, questions ouvertes.
3. Journal, registre, chronologie : ajout seulement.
4. Fraîcheur : le plus récent et le plus officiel l'emporte, l'ancienne valeur reste entre parenthèses.
5. Un fait, un seul fichier.
6. Noms propres de transcription : jamais corrigés de mémoire.
7. Rien d'inventé : ni décision, ni action, ni échéance.
8. Chaque ligne a sa source.
