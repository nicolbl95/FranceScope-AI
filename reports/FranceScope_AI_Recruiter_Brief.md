# FranceScope AI

## Prévisions macroéconomiques de long terme sur la France, assistées par LLM

FranceScope est un projet de prévision macroéconomique de long terme centré
sur trois résultats : **chômage**, **PIB réel par habitant** et **niveau de vie
médian réel**.

Le projet est aussi un cas d'étude sur la manière de rendre des workflows LLM
longs plus fiables grâce au context engineering, aux évaluations adversariales,
à la provenance des sources et au contrôle human-in-the-loop.

> Emploi + Production + Niveau de vie distribué

## Résultats 2050

| Indicateur | 2025 | Dégradation faible | Dégradation centrale | Dégradation forte |
|---|---:|---:|---:|---:|
| Chômage | 7,725 % | 12,0 % | 14,0 % | 17,8 % |
| PIB réel par habitant | 38 360 € | 36 500 € | 34 000 € | 30 000 € |
| Niveau de vie médian réel | 25 952,51 € | 24 700 € | 23 300 € | 20 800 € |

Ces trajectoires sont conditionnelles : elles représentent différents niveaux
de détérioration structurelle, de timing des crises, de récupération et de
scarring. L'ancien Index composite a été retiré ; les trois cibles restent
lisibles séparément.

## Comparaison institutionnelle

Les références sont séparées par nature :

- consensus court terme : chômage 2026 à 8,2 % et 2027 à 8,4 % ;
- prévision directe Banque de France : 7,8 % en 2028 ;
- référence CE long terme : 7,1 % en 2030, 6,7 % en 2040 et 6,3 % en 2050.

FranceScope ne dit pas que les institutions ont tort. Il utilise un cadre
conditionnel qui donne davantage de poids au stress budgétaire persistant, au
sous-investissement, à l'hystérèse, aux crises répétées et au scarring.

> **NA > fausse précision.**

Il n'existe pas de niveau institutionnel GDPpc de long terme directement
comparable, ni de prévision institutionnelle long terme directement comparable
du niveau de vie médian. Ces lacunes restent `NA`.

## Le vrai défi : rendre les LLM fiables sur un projet long

| Problème observé | Réponse d'ingénierie |
|---|---|
| Dérive du modèle | Objectif explicite et scope |
| Répétition d'échecs | Anti-loop rules |
| Exploration infinie | Bounded exploration |
| Gaspillage de tokens | Targeted reads |
| Perte d'état | Frozen decisions et handoffs |
| Sorties incohérentes | Évaluations temporelles et cross-variable |
| Biais d'un modèle | Revue adversariale multi-modèles |
| Sources mal interprétées | Gates de provenance |
| Over-editing | Smallest safe change et stop conditions |

> Le principal défi n'était pas d'obtenir une bonne réponse une fois. Il
> fallait maintenir la cohérence du système pendant plusieurs semaines.

Workflow : données historiques → sources institutionnelles → recherche →
prévisions candidates → évaluations → critique multi-modèles → revision gate →
sorties gelées.

## De la complexité à la robustesse

V1–V7 : simulateur causal large → dizaines de variables intermédiaires →
incertitude composée et validation difficile → pivot V8 → trois cibles finales →
évaluations temporelles et cross-variable → revue adversariale multi-modèles →
Index retiré → benchmark institutionnel → provenance valeur par valeur.

> **Le projet est devenu meilleur en devenant plus simple.**

La compétence importante n'était pas de protéger l'idée initiale, mais de
reconnaître quand l'architecture ne justifiait plus sa complexité et de changer
de direction.

## Mon rôle

J'ai conçu :

- l'architecture des scénarios ;
- la sélection finale des trois cibles ;
- les critères de cohérence ;
- les règles de context engineering ;
- les gates de validation ;
- le workflow multi-modèles ;
- la méthodologie de provenance ;
- les pivots principaux du projet.

Les LLM ont accéléré la recherche, le code, l'extraction de données, la
critique, la synthèse et la documentation. J'ai conservé la responsabilité de
décider quelles preuves retenir, quand réorienter l'IA, quoi geler, quelles
hypothèses rouvrir, et quels résultats étaient méthodologiquement
indéfendables.

> Le workflow est devenu **human-directed and machine-accelerated**, pas
> model-autonomous.

## Compétences démontrées

- **Context engineering** : scope, sélection de contexte, état gelé, handoffs.
- **Agent control** : anti-loop, exploration bornée, stop conditions.
- **Evaluation engineering** : évaluations temporelles, cross-variable,
  revue adversariale.
- **Multi-model orchestration** : critiques indépendantes et test
  d'hypothèses.
- **Source et provenance** : sources primaires, typage, intégrité de l'horizon,
  politique `NA`.
- **Software et data engineering** : Python, CSV, validation et graphiques
  reproductibles.
- **Jugement human-in-the-loop** : architecture, acceptation, simplification et
  décisions de risque.

## Pour aller plus loin

- [README](../README.md)
- [Rapport technique](../docs/technical_report.md)
- [Workflows LLM fiables](../docs/reliable_llm_workflows.md)
- [Évolution du projet](../docs/project_evolution.md)
- [Cadre d'évaluation](../docs/evaluation_framework.md)
- [Méthodologie institutionnelle](../docs/institutional_benchmark_methodology.md)

FranceScope n'est pas seulement un projet de forecasting. C'est un cas d'étude
sur la manière de transformer des LLM puissants mais imparfaits en un workflow
contrôlé, auditable et orienté résultat.
