# FranceScope AI

### Prévisions macroéconomiques de long terme sur la France, assistées par LLM

![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Data-Pandas-150458?logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Visualisation-Matplotlib-11557C)
![LLM](https://img.shields.io/badge/LLM-OpenAI%20%2F%20Claude-6F42C1)
![Context engineering](https://img.shields.io/badge/Workflow-Context%20Engineering-6F42C1)
![Provenance](https://img.shields.io/badge/Validation-Provenance%20%7C%20%C3%89valuation-0F766E)

FranceScope AI est un projet de scénarios macroéconomiques de long terme
consacré à la France. Il combine données historiques, recherche assistée par
LLM, scénarios conditionnels, comparaison institutionnelle et contrôles de
provenance.

Le projet est à la fois un problème économique réel et un cas d’étude
d’ingénierie des LLM : comment produire une analyse ambitieuse sans laisser
des modèles imparfaits dériver hors du périmètre, des sources ou des décisions
gelées ?

## Documentation principale

[Lire la documentation principale du projet](docs/main_documentation.md)

Elle présente la thèse économique, les trois scénarios, les données
historiques, la méthode de prévision, les comparaisons institutionnelles, les
trois graphiques finaux et le workflow d’ingénierie LLM.

## Pourquoi ce projet ?

J’ai construit FranceScope pour tester une autre hypothèse sur la trajectoire
économique de long terme de la France. Les projections institutionnelles sont
des repères essentiels, mais je pense qu’elles sous-pondèrent parfois la
persistance et l’interaction de certaines fragilités structurelles françaises :
dette et déficits élevés, croissance et productivité faibles,
sous-investissement, vieillissement, problèmes de compétitivité et exposition
aux chocs mondiaux.

La question n’est pas de choisir arbitrairement des chiffres plus pessimistes.
FranceScope demande ce qui se passe lorsque ces mécanismes se renforcent
mutuellement, avec des crises répétées, des chocs énergétiques, climatiques,
géopolitiques ou financiers, une faiblesse des partenaires commerciaux et un
*scarring* durable. Les trois scénarios testent alors différents degrés de
détérioration selon le timing, la sévérité, l’interaction des chocs, la reprise,
les facteurs compensateurs et les pertes persistantes.

## LLM Engineering

Le projet est un cas d’étude de **context engineering** : périmètre explicite,
décisions gelées, recherche bornée, règles anti-boucle, lectures ciblées,
gestion d’état, handoffs, provenance, revue adversariale multi-modèles et
validation humaine.

**Le prompt est une partie du système, pas le système entier.** Les autres
modèles produisent des objections testables ; ils ne votent pas sur la réponse.
Le workflow est humainement dirigé et accéléré par les machines.

## Ressources complémentaires

### Méthodologie du benchmark institutionnel
[Voir le document](docs/institutional_benchmark_methodology.md)

Explique comment les prévisions institutionnelles, projections de long terme,
valeurs dérivées et statuts `NA` sont classés et validés. À lire pour comprendre
la discipline de provenance des sources.

### Workflow LLM fiable
[Voir le document](docs/reliable_llm_workflows.md)

Décrit les règles de context engineering, de contrôle des agents, de gestion
d’état, de décisions gelées et de handoffs développées dans le projet.

### Cadre d’évaluation
[Voir le document](docs/evaluation_framework.md)

Présente les critères d’acceptation, de rejet et de révision : cohérence
temporelle et inter-variables, ordre des scénarios, provenance et revue
adversariale.

### Échecs utiles et leçons
[Voir le document](docs/failures_and_lessons.md)

Montre comment les erreurs de complexité, de définition des sources et de
cohérence globale ont conduit à une architecture plus simple et plus robuste.

### Licence MIT
[Voir la licence](LICENSE)

Licence open source du dépôt.
