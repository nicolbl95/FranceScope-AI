# FranceScope AI

### Prévisions macroéconomiques de long terme sur la France, assistées par LLM

![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Data-Pandas-150458?logo=pandas&logoColor=white)
![NumPy%20%2F%20Polars](https://img.shields.io/badge/Data-NumPy%20%20%2F%20Polars-013243)
![DuckDB](https://img.shields.io/badge/Data-DuckDB-FFF000?logo=duckdb&logoColor=black)
![Matplotlib](https://img.shields.io/badge/Visualisation-Matplotlib-11557C)
![LLM](https://img.shields.io/badge/LLM-OpenAI%20%2F%20Claude-6F42C1)
![Context engineering](https://img.shields.io/badge/Workflow-Context%20Engineering-6F42C1)
![Évaluation](https://img.shields.io/badge/Évaluation-Multi--modèles-168C4A)
![Provenance](https://img.shields.io/badge/Validation-Provenance%20%7C%20CSV%20%7C%20JSON%20%7C%20Markdown-0F766E)

FranceScope AI est un projet de prévision macroéconomique de long terme sur la
France. Il combine recherche assistée par LLM, ingénierie du contexte,
scénarios conditionnels, comparaison institutionnelle, évaluation et
provenance des sources.

La V8 prévoit numériquement trois résultats finaux : chômage, PIB réel par
habitant et niveau de vie médian réel. Les autres variables servent à structurer
les mécanismes et les scénarios, sans être transformées en fausses prévisions
détaillées.

## Documentation principale

[Lire la documentation principale du projet](docs/main_documentation.md)

## Résultats finaux

| Scénario | Année | Chômage | PIB réel / hab. | Niveau de vie médian réel |
|---|---:|---:|---:|---:|
| Ancrage observé | 2025 | 7,725 % | 38 360 € | 25 952,51 € |
| Dégradation contenue | 2030 | 8,5 % | 39 700 € | 26 500 € |
| Dégradation contenue | 2040 | 10,0 % | 39 000 € | 25 800 € |
| Dégradation contenue | 2050 | 12,0 % | 36 500 € | 24 700 € |
| Centrale | 2030 | 9,1 % | 38 500 € | 25 800 € |
| Centrale | 2040 | 12,0 % | 36 500 € | 25 000 € |
| Centrale | 2050 | 14,0 % | 34 000 € | 23 300 € |
| Forte détérioration | 2030 | 11,3 % | 37 000 € | 25 000 € |
| Forte détérioration | 2040 | 14,7 % | 34 000 € | 23 100 € |
| Forte détérioration | 2050 | 17,8 % | 30 000 € | 20 800 € |

Ces trajectoires sont des scénarios conditionnels FranceScope, pas des
prévisions institutionnelles officielles. Même la trajectoire « contenue »
reste une détérioration structurelle par rapport à 2025.

![Comparaison des scénarios finaux](outputs/charts/final_scenario_comparison.png)

## Pourquoi FranceScope diverge des institutions

FranceScope explore un cadre structurel conditionnel plus adverse ; il ne
prétend pas que les institutions ont tort. Les références institutionnelles
combinent des prévisions directes de court terme et des projections
structurelles de long terme, qui ne forment pas un consensus homogène jusqu’en
2050.

FranceScope donne davantage de poids à la pression budgétaire persistante, à la
charge d’intérêt, au sous-investissement, à la faiblesse de la productivité,
au vieillissement, aux chocs répétés et au *scarring*. Les repères chômage
retenus sont : consensus 2026 **8,2 %**, consensus 2027 **8,4 %**, Banque de
France 2028 **7,8 %**, puis Commission européenne **7,1 % en 2030**, **6,7 % en
2040** et **6,3 % en 2050**.

## LLM Engineering

Le projet est aussi un cas d’étude de **context engineering** : scope
explicite, décisions gelées, recherche bornée, règles anti-boucle, lectures
ciblées, gestion d’état, handoffs, provenance, revue adversariale
multi-modèles et validation humaine.

**Le prompt est une partie du système, pas le système entier.** Les autres
modèles servent à produire des objections testables ; ils ne votent pas sur la
réponse. Le workflow est humainement dirigé et accéléré par les machines.

## Ressources complémentaires

- [Méthodologie du benchmark institutionnel](docs/institutional_benchmark_methodology.md)
- [Workflow LLM fiable](docs/reliable_llm_workflows.md)
- [Cadre d’évaluation](docs/evaluation_framework.md)
- [Échecs utiles et leçons](docs/failures_and_lessons.md)
- [Licence MIT](LICENSE)
