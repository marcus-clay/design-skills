# design-skills

Des skills pour Claude et Codex autour du produit, du design, du prototypage et de l'animation. Chaque skill est un dossier avec un fichier `SKILL.md` : on le dépose dans son outil, et l'outil l'utilise quand la demande correspond.

Ce dépôt réunit deux familles :
- **Les skills de ce dépôt**, libres d'usage sous licence MIT.
- **Les skills recommandées**, écrites par d'autres : l'index les signale avec leur auteur et renvoie vers leur source, sans rien copier.

## Index

<!-- index:start -->
### Produit et stratégie

| Skill | Ce qu'elle fait | Où |
|---|---|---|
| `socle` | Méthode en cinq étapes pour démarrer un produit digital : structurer, outiller, construire, livrer, élargir. | [dossier](skills/socle) |
| `direction-design` | Feuille de route de conception, cadence d'instances et argumentaires pour peser dans un arbitrage. | [dossier](skills/direction-design) |

### Design et UX

| Skill | Ce qu'elle fait | Où |
|---|---|---|
| `direction-design` | Feuille de route de conception, cadence d'instances et argumentaires pour peser dans un arbitrage. | [dossier](skills/direction-design) |
| `ux-et-design-thinking` | Regard de méthode sur un parcours ou un écran : job à accomplir, faits d'usage, réutilisation de composants. | [dossier](skills/ux-et-design-thinking) |
| Emil Design Eng | La philosophie de finition d'interface et de choix d'animation d'Emil Kowalski. | [recommandée, par Emil Kowalski](https://github.com/emilkowalski/skills) |
| Impeccable | Une skill et vingt-quatre commandes (polish, audit, critique, animate...) pour guider et contrôler le design d'une interface. | [recommandée, par Paul Bakaus](https://impeccable.style) |
| Figma Console MCP | Un serveur MCP qui relie l'IA à Figma : lire et créer des designs, des tokens et des composants, avec ses commandes internes (skills figma-*). | [recommandée, par TJ Pitre, Southleft](https://docs.figma-console-mcp.southleft.com) |

### Facilitation

| Skill | Ce qu'elle fait | Où |
|---|---|---|
| `facilitation-ateliers` | Déroulé d'atelier ou de réunion : format, participants, durée et livrable. | [dossier](skills/facilitation-ateliers) |

### Prototypage

| Skill | Ce qu'elle fait | Où |
|---|---|---|
| `prototype-anime` | Un parcours d'écrans joué comme un film, sur mobile et desktop : doigt ou curseur, saisie, caméra. Démos en direct. | [dépôt dédié](https://github.com/marcus-clay/prototype-anime-skill), [démos](https://marcus-clay.github.io/prototype-anime-skill/) |
| `ship-to-show` | Transformer un prototype en étude de cas publiée, en sept phases, avec vidéos et contenu bilingue. | [dossier](skills/ship-to-show) |
| Figma Console MCP | Un serveur MCP qui relie l'IA à Figma : lire et créer des designs, des tokens et des composants, avec ses commandes internes (skills figma-*). | [recommandée, par TJ Pitre, Southleft](https://docs.figma-console-mcp.southleft.com) |

### Animation

| Skill | Ce qu'elle fait | Où |
|---|---|---|
| `prototype-anime` | Un parcours d'écrans joué comme un film, sur mobile et desktop : doigt ou curseur, saisie, caméra. Démos en direct. | [dépôt dédié](https://github.com/marcus-clay/prototype-anime-skill), [démos](https://marcus-clay.github.io/prototype-anime-skill/) |
| `drawing-animated-diagrams` | Diagrammes SVG pour React qui se dessinent à l'entrée dans l'écran, en encre et en gris. S'appuie sur diagram-storytelling et Emil Design Eng. | [dossier](skills/drawing-animated-diagrams) |
| Emil Design Eng | La philosophie de finition d'interface et de choix d'animation d'Emil Kowalski. | [recommandée, par Emil Kowalski](https://github.com/emilkowalski/skills) |
| Impeccable | Une skill et vingt-quatre commandes (polish, audit, critique, animate...) pour guider et contrôler le design d'une interface. | [recommandée, par Paul Bakaus](https://impeccable.style) |
| Transitions dev | Une collection de transitions CSS prêtes à l'emploi : modales, menus, badges, panneaux, onglets. | [recommandée, par Jakub Antalik](https://transitions.dev) |
| Transitions polish | Affiner des animations existantes selon une échelle de durées, de distances, de flous et de courbes. | [recommandée, par Jakub Antalik](https://transitions.dev) |

### Illustration et schémas

| Skill | Ce qu'elle fait | Où |
|---|---|---|
| `drawing-animated-diagrams` | Diagrammes SVG pour React qui se dessinent à l'entrée dans l'écran, en encre et en gris. S'appuie sur diagram-storytelling et Emil Design Eng. | [dossier](skills/drawing-animated-diagrams) |
| `resource-illustrations` | Vignettes de cartes de ressources : un fragment de la chose, des annotations, une touche d'accent. | [dossier](skills/resource-illustrations) |
| `marker-sketch` | Croquis au feutre sur papier à points, en SVG, avec quatre modes dont un mode interactif. | [dossier](skills/marker-sketch) |
| `diagram-storytelling` | Zonings, wireframes, parcours et schémas minimalistes pour slides : une idée par diagramme. | [dossier](skills/diagram-storytelling) |

### Présentations

| Skill | Ce qu'elle fait | Où |
|---|---|---|
| `diagram-storytelling` | Zonings, wireframes, parcours et schémas minimalistes pour slides : une idée par diagramme. | [dossier](skills/diagram-storytelling) |
| `slides` | Tokens de design, quinze mises en page et conventions narratives pour des présentations. | [dossier](skills/slides) |
<!-- index:end -->

## Skills recommandées : source et installation

Elles appartiennent à leurs auteurs et gardent leur licence : le plus fiable est de les installer depuis leur source, dont la page à jour indique la procédure.

<!-- external:start -->
### Emil Design Eng

Par Emil Kowalski. [Dépôt](https://github.com/emilkowalski/skills)

La procédure d'installation à jour se trouve dans le README de son dépôt.

### Impeccable

Par Paul Bakaus, licence Apache 2.0. [Dépôt](https://github.com/pbakaus/impeccable) · [Site](https://impeccable.style)

```bash
npx impeccable install
```

### Transitions dev

Par Jakub Antalik. [Dépôt](https://github.com/Jakubantalik/transitions.dev) · [Site](https://transitions.dev)

```bash
npx skills add Jakubantalik/transitions.dev
```

Licence propre : usage libre, redistribution de la bibliothèque interdite. Elle est donc à installer depuis sa source.

### Transitions polish

Par Jakub Antalik. [Site](https://transitions.dev)

Complément de Transitions dev, à installer depuis la même source (voir transitions.dev).

### Figma Console MCP

Par TJ Pitre, Southleft, licence MIT. [Dépôt](https://github.com/southleft/figma-console-mcp) · [Site](https://docs.figma-console-mcp.southleft.com)

Nécessite un jeton d'accès Figma. Non affilié à Figma.
<!-- external:end -->

## Installer une skill de ce dépôt

Chaque skill a son archive dans la page [Releases](../../releases/latest). Remplacer `NOM` par le nom de la skill (par exemple `slides`).

| Outil | Installation |
|---|---|
| **Claude.ai** (compte Pro) | **Réglages**, **Capacités**, **Skills**, puis téléverser `NOM.zip` tel quel, sans le décompresser |
| **Claude Code** | `curl -L -o NOM.zip https://github.com/marcus-clay/design-skills/releases/latest/download/NOM.zip`, puis `unzip -o NOM.zip -d ~/.claude/skills` |
| **Codex** | La même archive, avec `unzip -o NOM.zip -d ~/.agents/skills` |

Les outils détectent la skill sans redémarrage ; en cas de doute, taper `/skills` pour la voir dans la liste. Le [guide pas à pas de prototype-anime](https://github.com/marcus-clay/prototype-anime-skill/blob/main/GUIDE.md) détaille l'installation des trois outils, liens d'installation compris.

## Structure du dépôt

```
skills/<nom>/SKILL.md    une skill par dossier, avec ses fichiers de référence
catalog/skills.json      les données de l'index : thèmes, résumés, sources des skills recommandées
scripts/build.mjs        vérifie les skills, met à jour l'index ci-dessus et fabrique les archives
```

Après un ajout ou une modification : `node scripts/build.mjs` met l'index à jour, et `node scripts/build.mjs --zip` écrit les archives dans `dist/`.

## Ajouter une skill

1. Créer `skills/<nom>/SKILL.md`, avec `name: <nom>` et une `description` qui dit quand la déclencher.
2. L'ajouter dans `catalog/skills.json`, avec ses thèmes et un résumé d'une phrase.
3. Lancer `node scripts/build.mjs`.

## Licence

[MIT](LICENSE). Une exception : la police Patrick Hand fournie avec `marker-sketch` est sous licence SIL Open Font License (voir `skills/marker-sketch/assets/fonts/`). Les skills recommandées gardent la licence de leur auteur.
