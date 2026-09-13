# Évolution du projet FranceScope

FranceScope a évolué d'un simulateur causal très large vers un cadre de
scénarios centré sur trois résultats finaux. Chaque réorientation a répondu à
une faiblesse observée : complexité croissante, sources ambiguës, validation
difficile ou sorties localement plausibles mais globalement incohérentes.

> **FranceScope est devenu plus robuste à mesure qu'il est devenu plus simple.**

## 1. L'ambition initiale

L'objectif était de simuler jusqu'en 2050 les interactions entre
investissement, emploi, productivité, finances publiques, démographie,
commerce, énergie, climat et conditions de vie. Un réseau causal riche devait
relier les chocs à leurs conséquences sur la production et la population.

Cette ambition rendait les mécanismes visibles, mais elle supposait aussi de
transformer presque chaque mécanisme en variable numérique. Les versions V1 à
V7 ont ainsi accumulé des domaines, des boucles de rétroaction, des régimes
macroéconomiques et des artefacts de recherche. Elles ont été utiles pour
expliciter les canaux, les identités comptables et les décalages temporels,
mais elles ont aussi révélé le coût de cette architecture.

## 2. Quand la complexité a réduit la crédibilité

Chaque sortie intermédiaire ajoutait une hypothèse, une unité, un horizon et
une relation à vérifier. Les erreurs se propageaient du capital vers la
productivité, le PIB, l'emploi et les recettes, puis retournaient vers la
demande. Une trajectoire pouvait être plausible isolément tout en produisant
une histoire globale incohérente.

Les difficultés principales ont été :

- l'incertitude cumulative et la validation de centaines de relations ;
- le double comptage de chocs décrits sous plusieurs noms ;
- la confusion entre granularité et précision ;
- des niveaux de vie trop protégés dans des scénarios où la base fiscale se
  dégradait ;
- des trajectoires annuelles compatibles avec une équation mais incompatibles
  avec les autres variables.

La question décisive est donc devenue : **les résultats racontent-ils ensemble
la même histoire économique ?** La complexité du modèle ne garantissait pas la
crédibilité de la prévision.

## 3. Le pivot V8

V8 a réduit la surface de prévision numérique à trois cibles :

1. le taux de chômage ;
2. le PIB réel par habitant ;
3. le niveau de vie médian réel.

Les autres facteurs — dette, investissement, productivité, salaires, emploi,
démographie, énergie, climat, géopolitique, commerce, IA, automatisation et
confiance — sont restés des causes, des risques ou des éléments de contexte.
Ils structurent les scénarios sans être présentés comme des forecasts
autonomes.

Cette séparation a réduit les hypothèses numériques non soutenues, rendu la
validation plus ciblée et amélioré la traçabilité entre une valeur et sa
source. Les scénarios V8 diffèrent par le timing, la sévérité, la durée, la
récupération et le scarring ; le scénario least-bad n'est donc pas une
prospérité sans choc.

L'ancien Index composite a été supprimé. Les trois variables brutes étaient
déjà lisibles, tandis que la normalisation et les poids égaux ajoutaient un
choix normatif sans information indépendante suffisante. Le projet ne recrée
pas cet Index.

## 4. Scénarios et cohérence inter-variables

Les risques sont recherchés séparément des cibles : stress souverain ou
financier, crise bancaire, récession, chocs énergétiques ou climatiques,
conflit, fragmentation commerciale et crise institutionnelle. Les clusters
évitent de compter plusieurs fois une même transmission ; les risques
informent les scénarios sans devenir automatiquement des séries chiffrées.

Avec trois cibles, l'évaluation est devenue plus exigeante. Elle couvre l'ordre
des scénarios, les relations chômage–PIB, chômage–niveau de vie et PIB–niveau
de vie, le ratio médian/PIB, les phases de transition, les pentes annualisées
et l'ancrage observé. Les points ne sont gelés qu'après ces contrôles conjoints
et après correction des incohérences de calibration. Le PIB n'a pas besoin de
suivre exactement le chômage : participation, heures travaillées,
productivité, automatisation et composition démographique modifient leurs
relations.

## 5. Benchmark, provenance et données manquantes

Le benchmark institutionnel a été ajouté après le gel des trajectoires. Il
répond à une question distincte : que projettent les institutions, et pourquoi
FranceScope diffère-t-il ? Il ne constitue pas un quatrième scénario.
Banque de France, Commission européenne, OCDE, FMI, INSEE et Eurostat ont été
comparés selon leurs horizons publiés, sans prolongation silencieuse.

La taxonomie distingue `OBSERVED`, `DIRECT_FORECAST`,
`LONG_RUN_PROJECTION`, `STRUCTURAL_REFERENCE`,
`DERIVED_INSTITUTIONAL_REFERENCE`, `ILLUSTRATIVE_PROXY` et `NA`. Une valeur
convertie dans la même unité n'est pas nécessairement comparable : l'horizon,
la définition et le statut de la source comptent autant que l'arithmétique.
Les jalons de croissance européens ne justifiaient pas la fabrication d'un
niveau de PIB par habitant ; cette trajectoire a été retirée.

De même, aucun forecast institutionnel direct et comparable du niveau de vie
médian réel à long terme n'a été trouvé. Les niveaux non comparables restent
`NA` plutôt que de devenir un benchmark fabriqué.

## 6. Revue adversariale et workflow LLM

Des modèles indépendants ont challengé les sorties, mais leurs critiques
n'ont jamais été acceptées par vote. Chaque objection devait devenir une
hypothèse testable, puis déclencher une vérification de ratio, de pente, de
phase ou de source. Le désaccord entre modèles est ainsi devenu un outil
d'évaluation.

Le workflow a progressivement introduit :

- un scope explicite et des décisions gelées ;
- une recherche bornée et des lectures ciblées ;
- des règles anti-boucle et des conditions d'arrêt ;
- une gestion explicite de l'état et des handoffs ;
- la règle du plus petit changement sûr ;
- des manifests et contrôles de provenance ;
- une validation humaine des décisions finales.

Cette évolution illustre plusieurs leçons d'AI Engineering : la capacité d'un
modèle n'est pas sa fiabilité ; plus de contexte n'est pas toujours un meilleur
contexte ; plus de raisonnement ne garantit pas une meilleure exécution ; et
l'évaluation compte davantage que la génération. L'état doit être explicite,
les conditions d'arrêt font partie du système, et `NA` peut être le résultat
correct.

## 7. Responsabilité humaine et état final

Les LLM ont accéléré la recherche, le code, la critique, la synthèse et la
documentation. L'humain a conservé la responsabilité de l'architecture, du
périmètre, des hypothèses gelées, du rejet des sorties insuffisamment fondées
et de la décision de simplifier.

L'état final V8 est donc un cadre de scénarios avec trois cibles, des variables
causales explicatives, un benchmark institutionnel séparé, une provenance
explicite et une validation temporelle, inter-variable et adversariale.
L'histoire des versions antérieures reste une provenance et un matériau de
réflexion ; V8 est l'état numérique autoritatif.

> **Human-directed, machine-accelerated.**

## 8. Leçons pour l'ingénierie des systèmes LLM

1. La complexité n'est pas la crédibilité : la surface de sortie doit suivre la
   force des preuves.
2. L'évaluation doit précéder l'acceptation d'une génération plausible.
3. Le contexte utile est sélectionné, hiérarchisé et lié à la décision.
4. Les conditions d'arrêt empêchent les boucles sans amélioration mesurable.
5. Les décisions gelées et les handoffs rendent l'état reproductible.
6. Le désaccord multi-modèles vaut lorsqu'il devient un test vérifiable.
7. La provenance compte autant que l'arithmétique.
8. La simplification peut améliorer la correction, l'auditabilité et la
   lisibilité.

## 9. Documentation connexe

- [README recruteur](../README.md)
- [Workflow LLM fiable](reliable_llm_workflows.md)
- [Cadre d'évaluation](evaluation_framework.md)
- [Méthodologie du benchmark institutionnel](institutional_benchmark_methodology.md)
- [Rapport technique](technical_report.md)
- [Échecs et leçons](failures_and_lessons.md)
- [Archive des versions historiques](../archive/historical_versions/README.md)
