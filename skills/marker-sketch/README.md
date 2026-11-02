# marker-sketch

Skill pour Claude (claude.ai) et Claude Code : transforme une idée en croquis au feutre sur papier à points, en SVG (noir, blanc, gris, ombres portées, un accent rare). Quatre modes : Croquis, Live (réunion, atelier), Atelier (schémas denses), Interactif (évolution maintenant, ensuite, plus tard).

Le point d'entrée est `SKILL.md`. Le reste est chargé à la demande : `references/` (grammaire visuelle, quinze familles de diagrammes, métaphores, symboles, mode Live, maquettes, interactif), `assets/` (noyau de style, 47 symboles, police Patrick Hand sous licence OFL, moteur interactif), `scripts/` (assemblage, contrôle, rendu PNG, serveur Live, constructeur de schémas), `examples/` (six croquis, deux pages interactives).

## Installer dans claude.ai

1. Ouvrir Customize, puis Skills (`claude.ai/customize/skills`).
2. Téléverser `marker-sketch.zip` (le zip contient le dossier `marker-sketch/` à sa racine, c'est ce que claude.ai attend).
3. Activer la skill. L'exécution de code doit être activée pour que les scripts tournent.
4. Tester : « Dessine-moi en croquis le parcours d'une demande de support, de l'e-mail à la résolution ».

## Installer dans Claude Code

macOS et Linux, pour tous les projets :

```bash
mkdir -p ~/.claude/skills && unzip -o marker-sketch.zip -d ~/.claude/skills/
```

Pour un seul projet (à versionner avec le dépôt) :

```bash
mkdir -p .claude/skills && unzip -o marker-sketch.zip -d .claude/skills/
```

Windows (PowerShell) :

```powershell
Expand-Archive -Force marker-sketch.zip -DestinationPath "$HOME\.claude\skills"
```

Ou avec le script fourni : `bash marker-sketch/install.sh` (installe aussi les dépendances Python).

Vérifier : lancer `claude`, taper `/skills` (la skill `marker-sketch` doit apparaître) ou `/marker-sketch`. Si le dossier `~/.claude/skills` n'existait pas au démarrage de la session, lancer `/reload-skills`.

## Dépendances (facultatives, recommandées)

```bash
pip install fonttools playwright && playwright install chromium
```

`fonttools` convertit le texte en tracés (rendu identique partout), `playwright` produit les PNG de contrôle et teste les pages interactives. Sans elles, `compose.py` fonctionne avec la police incorporée.

## Commandes utiles

```bash
python3 scripts/compose.py draft.svg -o croquis.svg --outline          # assembler un dessin brut
python3 scripts/compose.py --catalog                                   # lister les symboles
python3 scripts/check.py draft.svg [--live]                            # contrôler avant livraison
python3 scripts/render.py croquis.svg                                  # PNG de contrôle
python3 scripts/live.py draft.svg                                      # projection en direct (localhost:8765)
python3 scripts/compose.py brut.svg --interactive scenes.json -o page.html
python3 examples/build_examples.py                                     # régénérer les exemples
```

## Licences

Police Patrick Hand : SIL Open Font License (`assets/fonts/LICENSE-patrick-hand.txt`). Reste du dossier : licence MIT (voir le fichier LICENSE à la racine du dépôt).
