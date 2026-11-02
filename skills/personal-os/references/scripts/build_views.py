#!/usr/bin/env python3
"""Génère des vues (tableaux) à partir des fiches de sujets.

Ce que fait le script
    Il lit chaque fichier .md du dossier des fiches (par défaut 05_scope/sheets).
    Chaque fiche commence par un petit en-tête délimité par deux lignes « --- »,
    avec une paire « clé: valeur » par ligne. Exemple :

        ---
        id: PRT-ONB
        title: Checklist d'accueil
        status: engagé
        owner: Morgan
        next_action: Préparer trois variantes
        horizon: Semaine suivante
        source: archive/2026-03-12_sync-portal.txt
        ---

    Il écrit ensuite deux fichiers dans le dossier des vues (par défaut
    05_scope/views) : by-status.md (sujets groupés par statut) et
    by-owner.md (sujets groupés par porteur).

Règles
    - Les fiches sont la source, les vues sont des dérivés : ne jamais modifier
      une vue à la main, modifier la fiche puis relancer le script.
    - Le script lit les fiches, il ne les modifie jamais.
    - Il ne dépend d'aucune bibliothèque externe (Python 3.8 ou plus).
    - Il s'arrête avec le code 1 si une fiche est invalide (champ manquant,
      statut inconnu, identifiant en double) et n'écrit alors aucune vue.

Utilisation
    python3 scripts/build_views.py
    python3 scripts/build_views.py chemin/vers/fiches chemin/vers/vues

    Sans argument, les chemins sont calculés à partir de l'emplacement du
    script (dossier parent du dossier scripts/).

Personnalisation
    Modifier STATUSES pour changer le vocabulaire des statuts, REQUIRED pour
    changer les champs obligatoires.
"""
import sys
from pathlib import Path

STATUSES = ["engagé", "en attente", "ouvert", "envisagé", "fait"]
REQUIRED = ["id", "title", "status", "owner", "next_action", "horizon", "source"]
COLUMNS = ["id", "title", "status", "owner", "next_action", "horizon", "source"]
HEADERS = ["ID", "Sujet", "Statut", "Porteur", "Prochaine action", "Horizon", "Source"]


def parse_sheet(path):
    """Retourne (champs, erreurs) pour une fiche. Lit l'en-tête simple clé: valeur."""
    errors = []
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None, [f"{path.name}: en-tête absent (la première ligne doit être « --- »)"]
    fields = {}
    closed = False
    for number, line in enumerate(lines[1:], start=2):
        if line.strip() == "---":
            closed = True
            break
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"{path.name}:{number}: ligne sans « clé: valeur »")
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    if not closed:
        errors.append(f"{path.name}: en-tête non fermé (deuxième « --- » manquant)")
    for key in REQUIRED:
        if not fields.get(key):
            errors.append(f"{path.name}: champ « {key} » manquant ou vide")
    status = fields.get("status")
    if status and status not in STATUSES:
        errors.append(f"{path.name}: statut « {status} » inconnu (attendus : {', '.join(STATUSES)})")
    return fields, errors


def cell(value):
    """Rend une valeur compatible avec une cellule de tableau Markdown."""
    return value.replace("|", "/").replace("\n", " ")


def table(rows):
    out = ["| " + " | ".join(HEADERS) + " |", "|" + "---|" * len(HEADERS)]
    for row in rows:
        out.append("| " + " | ".join(cell(row[c]) for c in COLUMNS) + " |")
    return "\n".join(out)


def build(rows, key, order, title):
    parts = [
        f"# {title}",
        "",
        "Vue générée par scripts/build_views.py. Ne pas modifier à la main : "
        "modifier la fiche du sujet puis relancer le script.",
        "",
    ]
    groups = {}
    for row in rows:
        groups.setdefault(row[key], []).append(row)
    names = [n for n in order if n in groups] + sorted(n for n in groups if n not in order)
    for name in names:
        group = sorted(groups[name], key=lambda r: r["id"])
        parts += [f"## {name} ({len(group)})", "", table(group), ""]
    return "\n".join(parts)


def main(argv):
    root = Path(__file__).resolve().parent.parent
    sheets_dir = Path(argv[1]) if len(argv) > 1 else root / "05_scope" / "sheets"
    views_dir = Path(argv[2]) if len(argv) > 2 else root / "05_scope" / "views"
    if not sheets_dir.is_dir():
        print(f"Dossier des fiches introuvable : {sheets_dir}", file=sys.stderr)
        return 1

    rows, errors, seen = [], [], {}
    for path in sorted(sheets_dir.glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        fields, problems = parse_sheet(path)
        errors += problems
        if fields is None or problems:
            continue
        if fields["id"] in seen:
            errors.append(f"{path.name}: identifiant « {fields['id']} » déjà utilisé par {seen[fields['id']]}")
            continue
        seen[fields["id"]] = path.name
        rows.append(fields)

    if errors:
        print("Fiches invalides, aucune vue écrite :", file=sys.stderr)
        for message in errors:
            print("  - " + message, file=sys.stderr)
        return 1

    views_dir.mkdir(parents=True, exist_ok=True)
    (views_dir / "by-status.md").write_text(
        build(rows, "status", STATUSES, "Sujets par statut") + "\n", encoding="utf-8")
    owners = sorted({r["owner"] for r in rows})
    (views_dir / "by-owner.md").write_text(
        build(rows, "owner", owners, "Sujets par porteur") + "\n", encoding="utf-8")
    print(f"{len(rows)} fiche(s) lue(s), 2 vues écrites dans {views_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
