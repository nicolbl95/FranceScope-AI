# FranceScope AI

### Prévisions macroéconomiques de long terme sur la France, assistées par LLM

![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Data-Pandas-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/Data-NumPy-013243?logo=numpy&logoColor=white)
![Polars](https://img.shields.io/badge/Data-Polars-CD792C)
![DuckDB](https://img.shields.io/badge/Analyse-DuckDB-FFF000?logo=duckdb&logoColor=black)
![Matplotlib](https://img.shields.io/badge/Visualisation-Matplotlib-11557C)
![OpenAI](https://img.shields.io/badge/LLM-OpenAI%20%2F%20GPT-412991?logo=openai&logoColor=white)
![Anthropic](https://img.shields.io/badge/LLM-Claude%20%2F%20Anthropic-D97757)
![Context engineering](https://img.shields.io/badge/Workflow-Context%20Engineering-6F42C1)
![Évaluation multi-modèles](https://img.shields.io/badge/Évaluation-Multi--modèles-168C4A)
![Human in the loop](https://img.shields.io/badge/Contrôle-Human--in--the--loop-2563EB)
![GitHub](https://img.shields.io/badge/Engineering-VS%20Code%20%7C%20GitHub-181717?logo=github&logoColor=white)
![Formats](https://img.shields.io/badge/Artefacts-CSV%20%7C%20JSON%20%7C%20Markdown-555555)
![Techniques](https://img.shields.io/badge/Techniques-Prompt%20%7C%20Provenance%20%7C%20Validation-0F766E)

FranceScope AI est un projet de prévision macroéconomique de long terme sur la
France centré sur trois résultats finaux : chômage, PIB réel par habitant et
niveau de vie médian réel.

Le projet sert également de cas d’étude en LLM engineering : context
engineering, orchestration multi-modèles, évaluation adversariale, gestion
d’état, provenance des sources et validation reproductible sur un workflow
multi-semaines.

**Emploi + Production + Niveau de vie distribué**

## 📚 Documentation et rapports

### Rapports PDF

- [Brief recruteur FranceScope AI](reports/FranceScope_AI_Recruiter_Brief.pdf)
- [Étude de cas LLM Engineering](reports/FranceScope_LLM_Engineering_Case_Study.pdf)
- [Rapport technique V8](reports/FranceScope_V8_Technical_Report.pdf)

### Documentation principale

- [Évolution du projet](docs/project_evolution.md)
- [Workflow LLM fiable](docs/reliable_llm_workflows.md)
- [Cadre d’évaluation](docs/evaluation_framework.md)
- [Méthodologie du benchmark institutionnel](docs/institutional_benchmark_methodology.md)
- [Méthodologie](docs/methodology.md)
- [Échecs utiles et leçons](docs/failures_and_lessons.md)
- [Rapport technique Markdown](docs/technical_report.md)
- [État final du projet](docs/FINAL_PROJECT_STATE.md)
- [Limites du projet](docs/limitations.md)
- [Carte du repository](docs/REPOSITORY_MAP.md)
- [Rapport de nettoyage du repository](docs/REPOSITORY_CLEANUP_REPORT.md)

### Autres fichiers publics

- [Licence MIT](LICENSE)
- [Guide des scripts](scripts/README.md)

## Description

FranceScope a commencé comme un simulateur macroéconomique causal beaucoup plus
large, avec l’ambition de modéliser de nombreuses variables intermédiaires.
La validation a montré que ces prévisions intermédiaires créaient une
incertitude cumulative et rendaient l’ensemble difficile à contrôler.

La V8 a donc été recentrée : seules trois variables finales sont prévues
numériquement. Les autres variables restent des éléments de causalité et de
construction des scénarios, sans être transformées en fausses prévisions
détaillées.

**FranceScope est devenu plus robuste à mesure qu’il est devenu plus simple.**

## Ce que FranceScope prévoit

### Chômage

Accès à l’emploi, sécurité économique et santé du marché du travail.

### PIB réel par habitant

Capacité productive moyenne et production réelle par personne.

### Niveau de vie médian réel

Situation matérielle du ménage ou de la personne médiane après impôts,
transferts et redistribution.

**Emploi + Production + Niveau de vie distribué**

FranceScope ne prétend pas résumer toute la qualité de vie française. La santé,
la sécurité, la qualité des services publics, le patrimoine et l’environnement
ne sont pas directement inclus dans les trois cibles.

## Résultats finaux

| Indicateur | 2025 | Dégradation contenue 2050 | Centrale 2050 | Forte 2050 |
|---|---:|---:|---:|---:|
| Chômage | 7,725 % | 12,0 % | 14,0 % | 17,8 % |
| PIB réel / hab. | 38 360 € | 36 500 € | 34 000 € | 30 000 € |
| Niveau de vie médian réel | 25 952,51 € | 24 700 € | 23 300 € | 20 800 € |

Les libellés publics correspondent à une dégradation contenue (*least-bad*),
une détérioration centrale et une détérioration forte. La dégradation contenue
n’est donc pas une trajectoire de prospérité : elle reste défavorable par
rapport à 2025.

Ces trajectoires sont des scénarios conditionnels FranceScope, pas des
prévisions institutionnelles officielles.

![Comparaison des scénarios finaux](outputs/charts/final_scenario_comparison.png)

Les valeurs gelées et leurs métadonnées sont disponibles dans
[final_three_target_forecasts.csv](data/final/final_three_target_forecasts.csv).

## Logique des scénarios

Les trois scénarios partagent des pressions structurelles :

- vieillissement et pression budgétaire ;
- dette et charge d’intérêt ;
- sous-investissement et productivité faible ;
- désindustrialisation, énergie et climat ;
- contraintes politiques et hystérèse du chômage.

Ils diffèrent surtout par le calendrier, la sévérité et la durée des crises, la
qualité de la reprise, le *scarring* et la force des facteurs compensateurs.

## Pourquoi c’est aussi un projet LLM Engineering

Le défi principal n’était pas d’obtenir une bonne réponse une fois. Il fallait
maintenir des LLM puissants mais imparfaits alignés sur un objectif complexe
pendant plusieurs semaines.

| Problème observé | Réponse d’ingénierie |
|---|---|
| Dérive du modèle | objectif et scope explicites |
| Boucles / répétitions | anti-loop rules |
| Exploration infinie | bounded exploration |
| Gaspillage de tokens | targeted reads |
| Perte d’état | frozen state + handoffs |
| Surédition | smallest safe change + stop conditions |
| Sorties localement plausibles mais incohérentes | temporal + cross-variable evals |
| Biais d’un seul modèle | adversarial multi-model review |
| Sources ambiguës | provenance registry |
| Confusion forecast / projection | source-type taxonomy |
| Extrapolation non justifiée | horizon integrity |

**Le prompt est une partie du système, pas le système entier.**

## Context engineering

- scope explicite et fichiers autoritatifs ;
- décisions gelées et conditions d’arrêt ;
- recherche bornée et minimisation des tokens ;
- handoffs structurés entre étapes ;
- contrôle de la provenance et des types de sources ;
- évaluations ciblées avant toute révision.

La qualité du contexte ne dépend pas seulement de la sélection des tokens :
elle dépend aussi du contrôle de la provenance.

## Comparaison avec les institutions

### Références de chômage

- consensus 2026 : **8,2 %** ;
- consensus 2027 : **8,4 %** ;
- Banque de France 2028 : **7,8 %** ;
- référence structurelle de la Commission européenne : **7,1 % en 2030**,
  **6,7 % en 2040** et **6,3 % en 2050**.

Cette trajectoire CE est une projection structurelle de long terme, pas un
consensus multi-institution homogène.

- Pas de niveau institutionnel GDPpc en euros par personne directement
  comparable jusqu’en 2050.
- Pas de prévision institutionnelle directe de long terme du niveau de vie
  médian.
- FranceScope conserve `NA` plutôt que d’inventer une valeur.

**NA > fausse précision**

![Comparaison du chômage avec les institutions](outputs/charts/institutional_unemployment.png)

Les sources et classifications sont conservées dans le
[registre institutionnel](data/institutional/institutional_source_registry.csv).

## Pourquoi FranceScope est plus adverse

Les références institutionnelles tendent à privilégier :

- des trajectoires démographiques et de participation ;
- une normalisation progressive de la productivité ;
- des hypothèses de politique publique de référence ;
- un *scarring* permanent plus limité.

FranceScope donne davantage de poids à :

- la pression budgétaire et la charge du service de la dette ;
- le sous-investissement, la faiblesse du capital et de la productivité ;
- la compétitivité et la désindustrialisation ;
- les contraintes politiques, les chocs répétés et les reprises faibles ;
- l’hystérèse du chômage et le *scarring* cumulé.

FranceScope ne prétend pas que les institutions ont tort ; il explore un cadre
structurel conditionnel plus adverse.

## Revue multi-modèles

La revue multi-modèles ne remplace pas la validation : elle sert à produire des
objections testables et à limiter le biais d’un seul modèle.

```text
Résultat candidat
      ↓
Critique externe
      ↓
Hypothèse testable
      ↓
Reproduction du problème
      ↓
Vérification données / méthodologie
      ↓
Révision uniquement si justifiée
```

## Workflow

```text
Données historiques
        ↓
Sources institutionnelles
        ↓
Provenance / normalisation
        ↓
Recherche structurelle
        ↓
Scénarios
        ↓
Prévisions candidates
        ↓
Évaluations temporelles + cross-variable
        ↓
Revue multi-modèles
        ↓
Revision gate
        ↓
Résultats gelés
```

## Ce que j’ai conçu

J’ai défini le périmètre V8, les trois cibles, l’architecture des scénarios,
les critères d’acceptation, les règles de context engineering, les gates de
provenance et d’horizon, la revue adversariale multi-modèles et les conditions
d’arrêt.

Les modèles ont accéléré la recherche, l’analyse, la critique, le code et la
documentation. J’ai conservé la responsabilité des arbitrages, de la
validation des sources, de la cohérence finale et du gel des résultats.

## Aller plus loin

- [Données finales](data/final/)
- [Graphiques publics](outputs/charts/)

## Limites

L’incertitude augmente avec l’horizon, particulièrement vers 2050. Ces
trajectoires sont des scénarios conditionnels, non des prophéties ni un
remplacement des prévisions institutionnelles. Le projet final ne prétend pas
représenter toute l’économie française : il privilégie trois variables
lisibles, traçables et évaluables.
