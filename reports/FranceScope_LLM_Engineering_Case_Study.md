# FranceScope — Étude de cas LLM Engineering

## Context engineering, contrôle des agents, évaluation et orchestration humain–IA

FranceScope est devenu un laboratoire pratique pour transformer des LLM
puissants mais imparfaits en un workflow long, contrôlé, traçable et orienté
résultat.

Cette étude ne décrit pas un nouveau modèle macroéconomique. Elle documente
l'ingénierie du workflow qui a permis de conduire un projet multi-semaines :
maintenir l'objectif, sélectionner le bon contexte, contrôler les actions,
préserver l'état, évaluer les sorties et décider quoi accepter ou geler.

## 1. Le problème d'ingénierie

Une réponse brillante à une question isolée n'était pas le problème. Le défi
était de maintenir simultanément la direction, l'état, le scope, la qualité,
l'intégrité des sources et la discipline d'exécution sur de nombreuses sessions
et itérations.

> Un LLM peut être très intelligent localement tout en étant peu fiable à
> l'échelle d'un projet de plusieurs semaines.

## 2. Modes d'échec observés

| Échec | Risque concret |
|---|---|
| Dérive du modèle | Optimiser la dernière tâche au détriment du projet |
| Perte d'état | Traiter une décision gelée comme une question ouverte |
| Approche ratée répétée | Consommer temps et tokens sans information nouvelle |
| Boucle d'exploration | Rechercher une certitude parfaite sans gain pertinent |
| Action hors scope | Créer des régressions ou du travail sans pouvoir de décision |
| Gaspillage de tokens | Noyer les contraintes importantes dans du contexte inutile |
| Surédition | Réintroduire des erreurs après une validation |
| Plausibilité locale | Produire des sorties incompatibles entre variables |
| Confusion de source | Transformer un taux ou une projection en niveau comparable |
| Confusion forecast/projection | Présenter des objets méthodologiquement différents comme un seul forecast |

## 3. Du prompt au context engineering

L'approche initiale consistait à « écrire une meilleure instruction ». La
pratique mature a consisté à contrôler un système plus large :

- état autoritatif ;
- scope et fichiers autorisés ;
- actions permises et mode de tâche ;
- décisions gelées ;
- conditions d'arrêt ;
- gates d'évaluation ;
- provenance des sources ;
- handoffs structurés.

> Le prompt est une partie du système, pas le système entier.

## 4. Anti-loop et changement de stratégie

Deux règles opérationnelles sont devenues explicites :

> **Never repeat the exact same failed tool call.**

> **If an approach fails twice without measurable progress, change hypothesis,
> tool, command, file, or implementation strategy.**

Ces règles cassent les blocages locaux. Elles transforment un échec répété en
signal de changement de stratégie plutôt qu'en invitation à reformuler
indéfiniment la même demande.

## 5. Exploration bornée et efficacité des tokens

Avant d'explorer, il fallait définir les fichiers, sources et questions
pertinents. Les lectures étaient ciblées, parfois partielles, et une condition
d'arrêt était fixée à l'avance. Les fichiers déjà validés n'étaient pas relus
sans raison opérationnelle.

> Explorer davantage n'est utile que si chaque action réduit une incertitude
> pertinente.

Chaque appel d'outil devait directement avancer la tâche. Cette discipline ne
réduit pas seulement le coût : moins de contexte, mieux sélectionné, peut
produire un meilleur raisonnement.

## 6. Scope, état gelé et plus petit changement sûr

Le scope explicite comprenait le workspace actif, les fichiers autorisés, les
valeurs V8 gelées et l'interdiction de modifier les artefacts V7/V3. Le mode de
travail était également distingué : recherche, édition, validation ou
présentation.

Une couche validée devenait autoritative et ne pouvait être rouverte que par
une revue formelle. Le changement devait rester le plus petit possible pour
corriger un problème démontré. Cela a réduit les régressions et rendu
l'attribution des effets plus claire.

> Un projet long devient fiable quand le système sait aussi ce qu'il n'a plus
> le droit de remettre en question.

## 7. Handoffs et conditions d'arrêt

Les transmissions structurées utilisaient notamment :

```text
PROJECT_VERSION
VALUES_CHANGED
FILES_UPDATED
FILES_CREATED
VALIDATION
VERDICT
NEXT_ACTION
```

Elles ont amélioré la continuité entre sessions et modèles. Les conditions
d'arrêt sont devenues une partie de la spécification : pas d'audit
supplémentaire après validation, pas de refactorisation opportuniste, pas de
nettoyage « tant qu'on y est », pas de réouverture d'un sujet gelé.

## 8. Evaluation engineering

Le système est passé de :

```text
generate → accept
```

à :

```text
generate → test → revise / reject / freeze
```

Les gates couvraient l'intégrité des données, l'ordre des scénarios, la
cohérence temporelle, la cohérence cross-variable, la plausibilité historique,
la traçabilité des sources et l'intégrité de l'horizon.

> Le modèle générait des candidats ; le framework décidait s'ils étaient
> acceptables.

## 9. Tests temporels et cross-variable

Les trajectoires étaient examinées sur les transitions 2025→2030, 2030→2040 et
2040→2050. Les relations chômage ↔ GDPpc, chômage ↔ médian et GDPpc ↔ médian
étaient également testées.

Ces contrôles ont notamment détecté un décalage du chômage à l'horizon 2030 et
une protection excessive du niveau de vie médian par rapport au PIB par
habitant. Les ajustements ont été minimaux et documentés.

## 10. Revue adversariale multi-modèles

Des modèles indépendants ont été utilisés comme critiques, pas comme un vote :

```text
candidat → critique externe → hypothèse explicite
→ reproduction → vérification des preuves → revision gate
```

Un désaccord devenait utile seulement lorsqu'il pouvait être transformé en test.
Les critiques ont contribué à examiner le calendrier du chômage et la relation
entre PIBpc et niveau de vie médian.

> Le désaccord entre modèles devenait utile seulement lorsqu'il était
> transformé en test.

## 11. Raisonnement orienté provenance

Chaque référence devait être qualifiée par source, date, variable exacte, type
de forecast, horizon, justification déclarée, niveau de confiance et historique
des transformations.

La taxonomie distingue `OBSERVED`, `DIRECT_FORECAST`,
`LONG_RUN_PROJECTION`, `STRUCTURAL_ASSUMPTION` et `DERIVED_PROXY`. Un taux de
croissance, une projection structurelle et une observation ne sont pas
interchangeables.

## 12. L'erreur sémantique des jalons GDPpc CE

Les jalons CE de croissance du PIB réel par habitant étaient publiés comme des
taux à certains horizons. Leur composition mathématique était possible, mais
supposait à tort un taux constant et une continuité sémantique suffisante pour
produire un niveau en euros jusqu'en 2050.

La trajectoire dérivée a été retirée.

> Une opération mathématique peut être correcte et son utilisation
> méthodologiquement fausse.

La leçon d'ingénierie est que la provenance et la sémantique doivent être
validées avant toute transformation.

## 13. NA plutôt que fausse précision

Aucun forecast institutionnel long terme directement comparable du niveau de
vie médian n'a été identifié. Aucun niveau institutionnel GDPpc comparable
n'existait non plus.

La décision a été de conserver `NA`, plutôt que de fabriquer une continuité
visuelle ou numérique.

> **NA > fausse précision**

Cette décision est un contrôle de confiance et une mesure anti-hallucination,
pas une lacune à dissimuler.

## 14. Human-in-the-loop

| Les LLM ont accéléré | J'ai conservé la responsabilité de |
|---|---|
| recherche | l'objectif du projet |
| code | l'architecture |
| extraction | le sens des scénarios |
| synthèse | la confiance dans les sources |
| critique | les critères d'acceptation |
| documentation | ce qu'il fallait geler et quand simplifier |

> Human-directed, machine-accelerated — not model-autonomous.

Les modèles ont accéléré l'exécution, mais n'ont pas décidé seuls de la
structure finale, de la confiance accordée aux sources ou de l'acceptation des
résultats.

## 15. Évolution de ma pratique

| Instinct initial | Pratique mature |
|---|---|
| Ajouter du détail au modèle | Réduire la surface de prévision |
| Ajouter du raisonnement | Renforcer les évaluations |
| Ajouter du contexte | Curater le contexte |
| Réessayer | Forcer un changement de stratégie |
| Recherche ouverte | Exploration bornée |
| État conversationnel | État gelé et handoffs |
| Confiance dans un modèle | Revue adversariale |
| Remplir les trous | Préférer `NA` |
| Conserver les abstractions | Retirer l'Index inutile |

## 16. Leçons clés

1. Capacité et fiabilité sont différentes.
2. La qualité du prompt ne suffit pas.
3. L'état doit être explicite.
4. L'évaluation compte davantage que la génération seule.
5. Les conditions d'arrêt sont une fonctionnalité.
6. Plus de contexte n'est pas toujours mieux.
7. La revue multi-modèles doit produire des tests.
8. La provenance est une contrainte d'ingénierie.
9. Une donnée manquante peut être la bonne sortie.
10. Le jugement humain reste architectural.

## 17. Compétences démontrées

- **Context engineering** : scope, sélection de contexte, état gelé et handoffs.
- **Agent control** : anti-loop, exploration bornée et stop conditions.
- **Evaluation engineering** : tests temporels, cross-variable et revue
  adversariale.
- **Multi-model orchestration** : critiques indépendantes et test d'hypothèses.
- **State management** : décisions autoritatives et transmissions structurées.
- **Tool-use discipline** : appels pertinents, lectures ciblées et changements
  minimaux.
- **Token efficiency** : réduction du contexte inutile et des répétitions.
- **Source / provenance engineering** : typage, horizon et politique `NA`.
- **Human-in-the-loop systems** : architecture, arbitrage et gel.
- **Data / software engineering** : Python, CSV, scripts de validation et
  graphiques reproductibles.

## 18. Limitations

FranceScope n'est pas une plateforme de production d'agents autonomes. Plusieurs
contrôles reposent sur des instructions disciplinées, des fichiers, des scripts
et des manifests ; toutes les règles ne sont pas imposées par un framework
d'orchestration dédié.

La revue multi-modèles n'est pas une peer review scientifique. Les workflows
restent dépendants de la qualité des sources, de la discipline d'exécution et
du jugement humain. La prévision de long terme reste incertaine.

## Conclusion

FranceScope m'a appris que l'ingénierie LLM ne consiste pas seulement à obtenir
de bonnes réponses. Elle consiste à construire un environnement dans lequel les
erreurs deviennent détectables, les décisions traçables, le contexte
contrôlable et l'arrêt explicite.

Le projet est devenu plus fiable à mesure que le workflow devenait plus
contraint, plus testable et plus human-directed.
