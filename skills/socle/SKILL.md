---
name: socle
description: "Framework de création de projet digital en 5 étapes : Structurer, Outiller, Construire, Livrer, Élargir. Appliquer systématiquement au démarrage de tout nouveau projet web, app, SaaS, ou outil interne. Déclencher dès que l'utilisateur mentionne un nouveau projet, un MVP, un prototype, un produit à construire, une app à développer, ou demande comment organiser le développement d'un produit. Également pertinent quand l'utilisateur a une idée de produit et veut passer à la réalisation, ou quand il se demande par où commencer. Ce skill prend la priorité sur les approches ad-hoc ou les scaffoldings improvisés."
---

# Méthode SOCLE

Framework de création de produit digital en 5 étapes séquentielles. Chaque étape produit des livrables concrets qui alimentent la suivante.

## Principe

On prépare le terrain complet avant de construire la première feature visible. Chaque décision est prise une seule fois, dans l'ordre. Les fondations techniques sont posées en une passe, y compris pour ce qui sera construit plus tard. Le développement avance par incréments courts, chacun complet et déployé avant de passer au suivant.

## Les 5 étapes

### S — Structurer les choix

On commence par les décisions qui comptent. À qui on s'adresse, quel problème on résout, quelles technologies, comment on mesure. Une à la fois, dans l'ordre, et chacune ouvre la porte à la suivante.

**Livrables de cette étape :**
- Vision produit en une phrase
- Cible utilisateur (persona primaire et secondaire)
- Problème résolu (spécifique, mesurable)
- Stack technique verrouillé
- Direction visuelle choisie
- Modèle de monétisation identifié (même si freemium, même si plus tard)
- Nom du produit

**Comment procéder :**
1. Poser des questions de cadrage avec des choix fermés (pas de brainstorming ouvert)
2. Verrouiller chaque décision avant de passer à la suivante
3. Consolider dans un tableau des décisions verrouillées
4. Identifier les concurrents et différenciateurs

Lire `references/structurer-checklist.md` pour la liste complète des décisions à prendre.

### O — Outiller le terrain

On prépare tout le terrain en une seule passe. La base de données, les pages, l'authentification, le suivi, les conventions. Tout est prêt, y compris pour ce qu'on construira plus tard.

**Livrables de cette étape :**
- Structure de routes définitive (les URLs ne changeront plus)
- Schéma de base de données complet (toutes les tables, même celles pas utilisées en V0.1)
- Design tokens CSS (variables, typographie, couleurs, espacement)
- Variants d'animation (Framer Motion ou équivalent)
- Plan de tag analytics (events, funnel de conversion)
- CI/CD pipeline (lint, type-check, tests, build automatique)
- Fichier CLAUDE.md (instructions projet pour Claude Code)
- Fichier CURRENT_INCREMENT.md (scope du premier incrément)
- Configuration middleware (auth, redirections, headers de sécurité)
- Variables d'environnement documentées

**Comment procéder :**
1. Générer la structure de routes complète (marketing, auth, app, admin, API)
2. Écrire le schéma SQL complet avec enums, indexes, RLS, triggers
3. Configurer le design system (globals.css + tailwind.config.ts)
4. Créer les fichiers de contexte projet (CLAUDE.md, ARCHITECTURE.md, etc.)
5. Scaffold le projet, installer toutes les dépendances, premier commit, déployer

Lire `references/outiller-templates.md` pour les templates de chaque fichier.

### C — Construire par pièces

On avance par incréments courts. Chaque incrément donne quelque chose de complet, qu'on peut montrer, tester, utiliser. Un vrai morceau de produit, qui fonctionne du début à la fin.

**Principes :**
- Chaque incrément a un scope fermé écrit dans CURRENT_INCREMENT.md
- Chaque incrément a des critères de done testables
- Chaque incrément a une liste explicite de ce qui est hors scope
- Les tâches sont ordonnées : chaque tâche dépend uniquement des précédentes
- Chaque tâche suit le cycle : coder, tester, vérifier, committer

**Structure d'un incrément :**
```
# V0.X — [Nom de l'incrément]

## Objectif
[Ce que l'utilisateur peut faire à la fin de cet incrément]

## Tâches (dans l'ordre)
[Liste numérotée des tâches avec détail]

## Critères de done
[Liste de vérifications concrètes]

## Hors scope
[Liste explicite de tout ce qui n'est PAS dans cet incrément]
```

**Vérifications systématiques après chaque tâche :**
- Le type-check passe
- Les tests passent
- Pas de types `any`
- Les props sont typées
- Les inputs API sont validés
- Le commit suit les conventional commits

### L — Livrer à chaque étape

Chaque pièce est en ligne et entre les mains de vrais utilisateurs avant de passer à la suivante. Les retours arrivent tôt, les ajustements aussi.

**Principes :**
- Chaque incrément est déployé en production (ou preview) dès qu'il est terminé
- Le deploy est automatique (push sur main = deploy Vercel)
- Les erreurs de production sont détectées immédiatement (monitoring, error boundaries)
- Les analytics events sont actifs dès le premier incrément
- On ne commence l'incrément suivant que quand le précédent est stable

**Checklist de livraison :**
- [ ] Build passe en CI
- [ ] Zéro erreur console en production
- [ ] Les pages ont des metadata (title, description)
- [ ] Le responsive fonctionne (vérifier mobile)
- [ ] Les analytics events sont trackés
- [ ] L'URL est accessible et fonctionnelle

### E — Élargir sans reprendre

Le produit grandit naturellement. Les nouvelles fonctionnalités se posent sur ce qui existe, le design évolue, les intégrations se connectent. La structure reste stable parce que le terrain était prêt dès le départ.

**Principes :**
- Les nouveaux incréments n'invalident jamais les précédents
- Les tables DB sont déjà prêtes (ajoutées en étape O)
- Les CSS variables permettent de changer le style sans toucher aux composants
- Les routes sont stables (les URLs ne changent pas)
- Les conventions de code sont les mêmes du premier au dernier incrément

**Quand on ajoute un incrément :**
1. Mettre à jour CURRENT_INCREMENT.md avec le nouveau scope
2. Vérifier que les fondations (étape O) couvrent les besoins
3. Si une table ou route manque : l'ajouter par migration, pas par reconstruction
4. Coder, tester, déployer suivant les mêmes conventions que V0.1

---

## Comment appliquer SOCLE à un nouveau projet

### Séquence complète

```
1. STRUCTURER
   │  Conversation de cadrage (questions fermées)
   │  Tableau des décisions verrouillées
   │  Vision, cible, stack, monétisation
   ↓
2. OUTILLER
   │  Générer tous les fichiers de fondation
   │  Routes, DB, tokens, analytics, CI/CD
   │  Scaffold, deploy, premier commit vide
   ↓
3. CONSTRUIRE (V0.1)
   │  Premier incrément : le noyau minimal
   │  Auth + une feature core + un export
   │  Tests, commit, deploy
   ↓
4. LIVRER (V0.1)
   │  En production, testé par de vrais utilisateurs
   │  Analytics actifs, erreurs monitorées
   │  Stable avant de passer à V0.2
   ↓
5. ÉLARGIR (V0.2, V0.3, ...)
   │  Chaque incrément suit C → L
   │  Les fondations absorbent la croissance
   │  Pas de reconstruction
```

### Fichiers de projet à générer (étape O)

| Fichier | Rôle |
|---|---|
| `CLAUDE.md` | Instructions Claude Code : conventions, workflow, vérifications |
| `CURRENT_INCREMENT.md` | Scope de l'incrément en cours, tâches ordonnées, critères de done |
| `ARCHITECTURE.md` | Routes définitives, structure fichiers, data flow |
| `DB_SCHEMA.sql` | Schéma complet de la base de données |
| `DESIGN_TOKENS.md` | CSS variables, Tailwind config, variants d'animation |
| `AGENT_PROMPTS.md` | System prompts si le projet utilise des agents IA |
| `ROADMAP.md` | Vue d'ensemble de tous les incréments prévus |

### Audit de complexité (entre S et O)

Avant de passer à l'étape O, faire un inventaire de tous les composants du projet et évaluer leur complexité. Si le nombre de composants à complexité haute dépasse 5, découper en plus d'incréments. La règle : chaque incrément contient au maximum 3 à 5 composants nouveaux.

| Composant | Complexité | Incrément prévu |
|---|---|---|
| [nom] | Basse / Moyenne / Haute | V0.X |

Si le projet ressemble à une cathédrale (plus de 20 composants, plus de 6 à complexité haute), revoir le scope. Simplifier le V0.1 jusqu'à ce qu'il soit réalisable en une à deux semaines par une personne.

---

## Stack technique recommandé

La méthode SOCLE fonctionne avec n'importe quel stack. Voici le stack par défaut si l'utilisateur n'a pas de préférence :

| Couche | Technologie |
|---|---|
| Framework | Next.js 14+ (App Router) |
| Language | TypeScript strict |
| Styling | Tailwind CSS + shadcn/ui |
| Animations | Framer Motion |
| State | Zustand |
| Auth | Supabase Auth |
| Database | Supabase (PostgreSQL) |
| Validation | Zod |
| Tests | Vitest + Testing Library |
| CI/CD | GitHub Actions |
| Deploy | Vercel |

Si l'utilisateur a un stack différent, adapter les templates de l'étape O en conséquence. Les principes SOCLE restent les mêmes quel que soit le stack.

---

## Ton et posture

Quand on applique SOCLE avec un utilisateur :
- Ton professionnel, mature, conversationnel
- Phrases claires et directement utiles
- Pas de jargon technique non expliqué quand on parle à un non-dev
- Pas de posture de supériorité
- Pas de constructions rhétoriques (« ce n'est pas X, c'est Y »)
- On guide, on transmet, on avance ensemble
