# Catalogue des agents

Un agent est un assistant spécialisé : un fichier Markdown dans `.claude/agents/` avec un nom, une description, la liste des outils qu'il a le droit d'utiliser, puis ses consignes. Claude Code le choisit d'après sa description, ou tu l'appelles par son nom (« utilise l'agent board-review »). Les modèles à copier sont dans `templates/.claude/agents/`.

Règles communes à tous les agents :

- ils lisent `CLAUDE.md` avant de travailler ;
- ils n'écrivent qu'après validation explicite, sauf ceux qui sont en lecture seule ;
- ils n'inventent ni décision, ni action, ni échéance ;
- ils citent la source de chaque ligne ;
- ils signalent un doute au lieu de trancher.

Les droits sont limités par la ligne `tools` du fichier. Un agent en lecture seule n'a ni `Write` ni `Edit`.

## Vue d'ensemble

| Agent | Quand l'appeler | Écrit ? |
|---|---|---|
| `inbox-ingestion` | Un fichier arrive dans `inbox/` | Oui, après validation |
| `board-review` | Revue hebdomadaire du board | Rapport, écrit sur accord |
| `consistency-check` | Après une grosse ingestion, avant un report externe | Non |
| `deliverables-writer` | Il faut produire une note, un mail, un support | Brouillon dans la réponse |
| `meeting-prep` | Avant ou après un 1:1 ou une réunion | Non |
| `decision-advisor` | Avant un arbitrage ou une présentation de position | Non |

## inbox-ingestion

**Rôle.** Transformer un fichier brut en modifications proposées du brain : journal, décisions, actions, faits, fiches, changelog.

**Quand l'appeler.** Dès qu'un fichier est déposé dans `inbox/` ou que tu colles une information nouvelle.

**Ce qu'il lit.** Le fichier d'inbox, `CLAUDE.md`, l'annuaire, le lexique, le registre de décisions, les fiches de sujets concernées, le board.

**Ce qu'il rend.** Une liste numérotée de modifications (fichier, avant, après, source, statut), une liste « possibles, non retenues » et les points à reconfirmer. Après validation : les écritures, l'archivage et la ligne de changelog.

**Limites.** N'écrit rien sans « valide tout » ou une liste de numéros. Ne supprime rien. Ne crée aucune personne à partir d'un nom douteux. Ne pose aucune échéance non donnée par un tiers.

## board-review

**Rôle.** Relire le board de tâches et le confronter à la réalité des comptes rendus et du journal.

**Quand l'appeler.** Une fois par semaine, avant un 1:1, ou après une ingestion importante. Donne-lui la date du jour.

**Ce qu'il lit.** `01_steering/board.md`, le journal récent, les fiches de sujets, le registre.

**Ce qu'il rend.** Les échéances dépassées, les tâches sans porteur ou sans horizon réaliste, les doublons, les écarts entre ce qui a été promis et ce qui est inscrit, les tâches qui semblent terminées. Chaque point est accompagné de sa source.

**Limites.** Ne clôture jamais une tâche sans ton accord. N'invente aucune tâche. Ne déplace pas une échéance fixée par un tiers.

## consistency-check

**Rôle.** Contrôler que le brain est cohérent avec lui-même.

**Quand l'appeler.** Après une ingestion importante, avant une revue hebdomadaire, avant de reporter un changelog dans un outil externe.

**Ce qu'il lit.** Tout le dossier, en lecture seule.

**Ce qu'il rend.** Un rapport : dates et jours de la semaine qui ne concordent pas, échéances dépassées, statuts contradictoires entre une fiche et le board, noms écrits de plusieurs façons, faits présents à deux endroits, renvois cassés, règle de fraîcheur non appliquée.

**Limites.** Lecture seule : il n'a pas les outils d'écriture. Il signale, il ne corrige pas.

## deliverables-writer

**Rôle.** Rédiger un livrable (note de cadrage, compte rendu, mail, plan de présentation, texte de support) à partir du brain, pour des lecteurs qui ne sont pas du métier.

**Quand l'appeler.** Quand tu dois produire quelque chose pour un tiers. Précise le lecteur, l'objectif et la longueur.

**Ce qu'il lit.** Les fichiers du brain utiles au sujet, le lexique, les règles de style de `CLAUDE.md`.

**Ce qu'il rend.** Un seul brouillon soigné dans la réponse, avec les sources en fin de texte. Un fichier n'est écrit que sur demande, hors des fichiers de domaine.

**Limites.** N'affirme rien que le brain ne contienne pas. Respecte les statuts : ce qui est envisagé n'est pas écrit comme décidé. Il ne prend aucun engagement à ta place.

## meeting-prep

**Rôle.** Préparer une réunion ou un 1:1, et aider à le débriefer ensuite.

**Quand l'appeler.** La veille ou le matin d'un 1:1, d'un point d'équipe, d'une réunion avec un partenaire.

**Ce qu'il lit.** L'annuaire, les notes de collaboration, les derniers comptes rendus, le board (actions de la personne), les fiches de sujets communes.

**Ce qu'il rend.** Un guide court : ce qui a été dit la dernière fois, ce qui est en attente de part et d'autre, deux ou trois sujets à aborder, les questions ouvertes. Chaque ligne a sa source. Après la réunion : une liste de ce qu'il faudra déposer dans `inbox/`.

**Limites.** Lecture seule. Ne rédige pas de réponses à ta place. N'attribue pas d'intention à la personne. Garde les éléments privés hors des supports destinés à être partagés.

## decision-advisor

**Rôle.** Éprouver une décision ou une position avant qu'elle soit portée.

**Quand l'appeler.** Avant un arbitrage, une présentation d'une position, une négociation de priorité.

**Ce qu'il lit.** Le registre de décisions, les fiches de sujets, les comptes rendus qui touchent la question.

**Ce qu'il rend.** Les hypothèses non vérifiées, les angles morts, les alternatives, les conséquences probables, les objections que l'on peut attendre, et deux ou trois questions à poser. Il distingue ce qui vient du brain de ce qui est un raisonnement général.

**Limites.** Lecture seule. Ne tranche pas à ta place. Ne présente pas ses hypothèses comme des faits du brain.

## Enchaînements courants

1. `inbox-ingestion`, puis `consistency-check` pour contrôler le résultat.
2. `board-review`, puis `meeting-prep` avant un 1:1.
3. `decision-advisor`, puis `deliverables-writer` pour mettre la position en forme.

## Créer un septième agent

Avant d'ajouter un agent, vérifie qu'aucun des six ne couvre le besoin avec une consigne de plus. Si un nouvel agent est justifié : une phrase pour le rôle, la liste minimale d'outils, ce qu'il lit, ce qu'il rend, et une section « Limites ». Teste-le sur trois cas réels avant de l'adopter.
