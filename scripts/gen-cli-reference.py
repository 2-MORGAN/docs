#!/usr/bin/env python3
"""Genere cli/commandes.mdx depuis la sortie JSON de `nimbus docs --commands`.

Lit sur stdin une liste d'objets {command, use, short, destructive, json,
flags: [{name, type, usage, required}]}, ecrit le contenu complet de
cli/commandes.mdx sur stdout (ou dans le fichier passe en argv[1]).

Usage :
    nimbus docs --commands | python3 scripts/gen-cli-reference.py cli/commandes.mdx
"""

import argparse
import json
import sys

EXCLUDED_FLAGS = frozenset({"json", "help", "version"})


def flatten(text):
    return " ".join(str(text).split())


def escape_cell(text):
    text = flatten(text)
    text = text.replace("|", "\\|")
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    if "{" in text or "}" in text:
        return "`" + text + "`"
    return text


def full_command(entry):
    base = flatten(entry.get("command", ""))
    use = flatten(entry.get("use", ""))
    parts = use.split()
    last = base.split()[-1] if base.split() else ""
    if len(parts) > 1 and parts[0] == last:
        return (base + " " + " ".join(parts[1:])).strip()
    if use and use != last:
        return (base + " " + use).strip()
    return base


def useful_flags(entry):
    flags = entry.get("flags", []) or []
    return [
        "--" + f["name"] + (" (obligatoire)" if f.get("required") else "")
        for f in flags
        if f.get("name") not in EXCLUDED_FLAGS
    ]


def build_mdx(commands):
    groups = {}
    for entry in commands:
        if not isinstance(entry, dict) or not entry.get("command"):
            raise ValueError("entree invalide (objet {command, ...} attendu)")
        domain = flatten(entry["command"]).split()[1]
        groups.setdefault(domain, []).append(entry)
    lines = [
        "---",
        'title: "Référence des commandes"',
        'description: "Toutes les commandes de la CLI Nimbus, avec leurs flags utiles."',
        'keywords: ["cli", "commandes", "référence", "nimbus"]',
        "---",
        "",
        "{/* Généré par scripts/gen-cli-reference.py - ne pas éditer à la main. */}",
        "",
        "Cette page liste toutes les commandes de la CLI, telles que la CLI les déclare.",
        "Les flags obligatoires portent la mention (obligatoire).",
        "Si aucun flag n'est marqué, vérifiez avec l'aide de la commande sur votre installation.",
        "Pour la régénérer, lancez :",
        "",
        "`nimbus docs --commands | python3 scripts/gen-cli-reference.py cli/commandes.mdx`",
        "",
    ]
    for domain in sorted(groups):
        lines.append("## " + domain)
        lines.append("")
        lines.append("| Commande | À quoi elle sert | Flags utiles | Destructive ? |")
        lines.append("| --- | --- | --- | --- |")
        for entry in sorted(groups[domain], key=lambda e: full_command(e)):
            cmd = full_command(entry)
            short = escape_cell(entry.get("short", "")) or "-"
            flags = ", ".join("`" + f + "`" for f in useful_flags(entry)) or "aucun"
            destructive = "oui" if entry.get("destructive") else "non"
            lines.append(
                "| `" + cmd + "` | " + short + " | " + flags + " | " + destructive + " |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Genere cli/commandes.mdx depuis `nimbus docs --commands` (JSON sur stdin)."
    )
    parser.add_argument("output", nargs="?", default=None, help="fichier de sortie")
    args = parser.parse_args()
    try:
        data = json.loads(sys.stdin.read())
    except json.JSONDecodeError as exc:
        print("Erreur : JSON invalide sur stdin (" + str(exc) + ").", file=sys.stderr)
        return 1
    if not isinstance(data, list):
        print("Erreur : le JSON doit etre une liste de commandes.", file=sys.stderr)
        return 1
    try:
        text = build_mdx(data)
    except (ValueError, IndexError, KeyError) as exc:
        print("Erreur : entree inattendue (" + str(exc) + ").", file=sys.stderr)
        return 1
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(text)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
