# Cas d'usage

Chaque scénario suit la même forme : la situation, ce qu'on dit à Claude, ce que Claude fait, le résultat. Les personnes et produits sont fictifs (ceux d'Acme Corp, voir `example-acme/`).

## 1. Product design au quotidien

**Situation.** Morgan, designer produit, enchaîne trois réunions dans la journée sur Acme Portal. Le soir, ses notes sont dispersées et elle ne sait plus quelle décision a été prise sur quel écran.

**Ce qu'on dit à Claude.** Elle dépose ses trois fichiers de notes dans `inbox/` et tape `/inbox`.

**Ce que Claude fait.** Il traite les fichiers un par un. Pour chacun, il sépare décisions, actions, faits et questions ouvertes, et propose l'avant et l'après de chaque fichier concerné. Il signale un nom douteux dans la deuxième transcription. Après validation, il écrit, archive les originaux et met à jour les fiches de sujets.

**Résultat.** Le lendemain matin, `/review-board` donne à Morgan ses cinq actions de la semaine avec leurs sources. Le registre contient deux nouvelles décisions avec leur raison. Aucune note n'a été recopiée à la main.

## 2. Head of design : définir la stratégie et piloter l'activité

**Situation.** Sam, head of design, doit présenter à Dana (VP Produit) la répartition de l'équipe entre trois sujets, et savoir où l'activité est bloquée.

**Ce qu'on dit à Claude.** « Lance le script de vues, puis donne-moi les sujets en attente et ce qui bloque, par porteur. Ensuite, demande à l'agent decision-advisor d'éprouver l'idée de mettre une personne de plus sur les filtres d'Insights. »

**Ce que Claude fait.** Il lance `build_views.py`, lit les vues par statut et par porteur, puis liste les sujets en attente avec leur prochaine action. L'agent `decision-advisor` relit le registre et les fiches, puis rend ses hypothèses non vérifiées (la date de l'API n'est pas confirmée par écrit), deux alternatives et trois questions à poser à Dana.

**Résultat.** Sam arrive à la réunion avec une page de position où chaque ligne a sa source. Les points non confirmés sont écrits comme tels. L'arbitrage obtenu est ajouté au registre à l'étape suivante.

## 3. Concevoir un parcours

**Situation.** Morgan doit concevoir le parcours d'arrivée dans Acme Portal pour les nouveaux comptes.

**Ce qu'on dit à Claude.** « Rassemble tout ce que le brain dit sur l'accueil des nouveaux comptes : décisions, contraintes techniques, questions ouvertes. Propose ensuite une description du parcours, étape par étape, avec les états et les cas limites. »

**Ce que Claude fait.** Il lit la fiche du sujet, le registre (D-003 limite la checklist aux nouveaux comptes), le fichier produit et les comptes rendus archivés. Il rend un brouillon dans la réponse : étapes, ce que voit la personne à chaque étape, règles de gestion, cas limites (compte invité, compte sans droits), et une section « À confirmer » pour tout ce qui n'est pas documenté.

**Résultat.** Un texte de parcours sourcé, que Morgan relit et corrige. Une fois validé, il devient la référence du sujet : la maquette et le prototype en sont les vues, pas l'inverse.

## 4. Designer avec un MCP (par exemple Figma) en s'appuyant sur le brain

**Situation.** Un MCP est un connecteur qui donne à Claude Code l'accès à un outil externe, ici un outil de maquettes. Morgan l'a branché pour que Claude puisse lire et créer des écrans.

**Ce qu'on dit à Claude.** « Crée dans le fichier de maquettes les écrans de la checklist d'accueil, à partir de la fiche du sujet et du parcours validé. Ne fais que ce que la fiche justifie. »

**Ce que Claude fait.** Il relit la fiche et le parcours, liste les écrans à produire et te demande validation de cette liste avant de toucher au fichier. Il crée ensuite les écrans en nommant les éléments selon la convention du brain, signale ce qui sort de la fiche (« hors périmètre »), et ne supprime rien dans le fichier sans confirmation.

**Résultat.** Les maquettes suivent le texte, pas l'inverse. Une ligne est ajoutée à `CHANGELOG.md` pour dire quelles pages du fichier ont été touchées. Si le texte change plus tard, la maquette se met à jour par la même voie.

## 5. Déployer des prototypes

**Situation.** Riley, directeur technique, veut tester la checklist avec cinq clients avant l'été. Morgan doit fournir un prototype cliquable.

**Ce qu'on dit à Claude.** « À partir du parcours validé du sujet d'accueil, construis un prototype cliquable dans le dossier `~/prototypes/portal-onboarding`. N'écris rien dans le brain. »

**Ce que Claude fait.** Il lit le parcours, annonce ce qu'il va produire (écrans, interactions, ce qui est volontairement simulé), puis construit le prototype dans le dossier désigné. Il note les écarts avec le parcours dans sa réponse. Une fois le prototype testé, il propose un dépôt dans `inbox/` des retours de test.

**Résultat.** Un prototype jouable, séparé du brain. Les retours de test passent ensuite par `/inbox` comme n'importe quelle matière : ils produisent des faits, des décisions et des actions sourcés.

## 6. Concevoir des présentations

**Situation.** Sam présente l'état du périmètre design au comité produit, devant des personnes qui ne sont pas designers.

**Ce qu'on dit à Claude.** « Utilise l'agent deliverables-writer pour un plan de présentation de huit diapositives : où nous en sommes, ce qui est décidé, ce qui bloque, ce que nous demandons. Lecteurs : le comité produit, sans vocabulaire de design. »

**Ce que Claude fait.** L'agent lit les vues du périmètre, le registre et le board. Il propose le plan diapositive par diapositive : un message par diapositive, des phrases complètes, les sources en note. Il distingue ce qui est décidé de ce qui est envisagé. Il écrit un seul brouillon, sans engagement à la place de Sam.

**Résultat.** Un plan prêt à mettre en forme dans l'outil de présentation habituel. Si la présentation est ensuite modifiée, le brain reste la source : on corrige le brain, puis la présentation.

## 7. Mettre à jour la mémoire de tous les contenus après un changement (propagation)

**Situation.** Dana annonce que le lancement d'Acme Insights passe de septembre à octobre. Cette date figure dans la fiche du sujet, le fichier produit, le board, deux pages externes et un support de présentation.

**Ce qu'on dit à Claude.** `/propagate Lancement d'Acme Insights décalé de septembre à octobre 2026, annoncé par Dana le 12 mars.`

**Ce que Claude fait.**

1. Il cherche la date dans tout le brain (recherche de texte) et dresse la liste des endroits concernés.
2. Il choisit un seul fichier source (le fichier produit) et propose d'y corriger la valeur, avec l'ancienne entre parenthèses et sa date.
3. Il propose pour chaque autre fichier de renvoyer vers la source au lieu de recopier la date.
4. Il propose une entrée de chronologie et, si une décision est en jeu, une entrée de registre.
5. Il liste dans `CHANGELOG.md` les pages externes à mettre à jour (« remplacer » le paragraphe identifié) et les supports à reprendre à la main.
6. Il attend ta validation, écrit, puis fait relire le résultat par `consistency-check`.

**Résultat.** Un seul endroit porte la nouvelle date. Rien n'a été oublié, parce que la liste vient d'une recherche et pas de la mémoire. Les outils externes sont mis à jour à partir du changelog, dans l'ordre.
