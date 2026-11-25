# Instructions pour les agents — documentation Nimbus

Site Mintlify publié depuis `main`. Dépôt **public** : aucun secret, aucune faille, aucun détail d'infrastructure, aucun chemin du code privé.

## Lecteurs
Un grand débutant, et son agent IA qui n'a que cette documentation. L'interface web et la CLI ont la même place : si une fonctionnalité n'existe que d'un côté, la page le dit.

## Règles
- Écrire en français, vouvoiement, phrases complètes, pas de tiret cadratin, pas de jargon non défini.
- Décrire le comportement actuel, vérifié dans le code de CNP (frontend, backend, CLI), jamais de mémoire. Marquer « à vérifier sur votre installation » ce qui dépend de la configuration déployée, et « Dépend de » ce qui n'est pas encore livré.
- Libellés d'interface en gras, mot pour mot. Messages d'erreur exacts.
- Chaque commande citée existe dans `nimbus docs --commands` et se lance telle quelle. `--input` prend un fichier ou `-`.
- Toujours une cible explicite dans les exemples de déploiement (`--cluster-id k3s-oracle`).
- Une règle a une seule page de référence ; les autres y renvoient.
- Un changement de slug ajoute une redirection dans `docs.json`.

## Gabarit d'une page de fonctionnalité
1. Frontmatter `title`, `description` (avec les mots qu'un débutant taperait), `keywords`. Pas de titre de niveau 1.
2. **En bref** : tableau où, commande, qui, quand ça prend effet, réversible.
3. **Avant de commencer** : prérequis et comment les vérifier.
4. **Faire** : onglets Interface et CLI.
5. **Vérifier**, **Limites**, **Si ça échoue** (message, cause, geste).
6. **Pour un agent** : à demander, accord obligatoire, constat du résultat.
7. **Voir aussi** : trois liens au plus.

## Pièges MDX
Dans le texte, `<VALEUR>` et `{` sont toujours dans du code. Commentaires en `{/* */}`.

## Mettre à jour
- `cli/commandes.mdx` est générée, ne pas l'éditer : `nimbus docs --commands | python3 scripts/gen-cli-reference.py cli/commandes.mdx`.
- Une nouvelle fonctionnalité met à jour sa page, `plateforme/visite-guidee`, `cli/interface-ou-cli`, `docs.json` et, si un agent s'en sert, `agents/recettes`.
- `llms.txt` est écrit à la main et pointe d'abord vers `agents/`.
- Contrôles : liens internes, compilation MDX (`mint dev` ou `mint broken-links`), commandes comparées à `nimbus docs --commands`.
