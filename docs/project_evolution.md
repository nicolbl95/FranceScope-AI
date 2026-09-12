# Évolution du projet FranceScope

FranceScope a changé substantiellement au cours de son développement. Ce
n'était pas une dérive de périmètre sans direction : chaque réorientation a
répondu à une faiblesse observée, à une ambiguïté de source ou à un résultat
difficile à défendre. Le projet est passé d'un simulateur causal très large à
un cadre de scénarios centré sur trois résultats finaux, avec une évaluation
plus stricte et une meilleure provenance.

> **FranceScope est devenu plus robuste à mesure qu'il est devenu plus simple.**

Ce document raconte deux évolutions parallèles :

1. l'évolution de l'architecture macroéconomique ;
2. l'évolution du workflow humain–LLM qui a permis de la cadrer, de la tester
   et finalement de la simplifier.

## 1. La vision initiale : simuler les mécanismes

L'ambition initiale était de construire un simulateur causal détaillé de
l'économie française à long terme, capable de représenter jusqu'en 2050 de
nombreuses interactions entre variables, tendances structurelles et chocs.
L'idée était de partir d'un réseau causal riche pour dériver les conséquences
sur la production et les conditions de vie.

Cette approche était attractive pour de bonnes raisons :

- elle rendait les mécanismes économiques explicites ;
- elle permettait de relier les chocs à des canaux concrets ;
- elle offrait une architecture de scénarios ;
- elle semblait plus réaliste qu'une extrapolation directe de trois séries.

L'objectif n'était donc pas de produire un modèle complexe pour lui-même, mais
de rendre visibles les chaînes de transmission : investissement, emploi,
productivité, finances publiques, démographie, commerce et conditions de vie.

## 2. V1–V7 : l'expansion du modèle causal

Les versions historiques ont progressivement couvert un grand nombre de
domaines : investissement et crédit, demande des ménages, commerce extérieur,
inflation, revenus du travail, chômage, démographie, productivité, énergie,
climat, pression budgétaire, risques géopolitiques et scarring. Des boucles de
rétroaction non linéaires reliaient notamment dette, coût de financement,
investissement, activité, emploi et recettes publiques.

Le travail réalisé à ce stade n'était pas inutile. Il a permis d'expliciter des
identités comptables, de documenter des canaux, de corriger des doublons, de
tester des décalages temporels, d'améliorer la cohérence du commerce et de
formaliser des mécanismes comme les seuils de chômage et la persistance des
chocs. Les documents V3 décrivent par exemple des états structurels, des
régimes macroéconomiques, des hazards, des boucles souveraineté–banques, des
canaux climatiques et des effets de productivité de l'IA.

V7 représente donc une étape exploratoire importante : il a conservé une
intuition causale riche et de nombreux artefacts de recherche. Il a surtout
révélé les limites pratiques d'une architecture où presque chaque mécanisme
devient potentiellement une nouvelle prévision numérique.

Les éléments historiques V3/V7 restent disponibles comme provenance et comme
matériau de réflexion. Ils ne constituent pas le périmètre numérique final.

## 3. Ce qui a commencé à casser

### Trop de variables numériques intermédiaires

Chaque variable intermédiaire ajoutait une hypothèse, une convention d'unité,
un horizon et une relation à valider. Une valeur numérique supplémentaire peut
sembler raisonnable isolément tout en augmentant la surface totale de
l'incertitude.

### Incertitude cumulative

Dans un réseau causal, les erreurs ne restent pas localisées. Une hypothèse
sur le capital influence la productivité, le PIB, l'emploi et les recettes ;
une hypothèse sur le chômage influence ensuite les revenus et la demande. Même
si chaque équation est plausible, l'incertitude combinée devient difficile à
quantifier et à expliquer.

### Validation difficile

Un grand modèle peut être cohérent avec ses propres équations sans être
facilement défendable face à des données observées ou à des références
institutionnelles. Il devient difficile de répondre simplement à la question :
quels sont exactement les résultats finaux, et quelle preuve justifie chacun
d'eux ?

### Risque de double comptage

Les mêmes pressions peuvent apparaître sous plusieurs noms : risque
géopolitique, énergie, commerce, inflation et productivité peuvent parfois
représenter une partie du même choc. Les traiter comme des événements
indépendants surestime alors le risque cumulé. La formalisation des clusters de
risques dans V8 a précisément cherché à éviter ce problème.

### Cohérence locale contre cohérence globale

Une équation ou une trajectoire annuelle peut sembler raisonnable seule, tandis
que l'histoire globale ne l'est pas. Un chômage trop élevé trop tôt peut être
incompatible avec les phases du PIB et du niveau de vie ; un niveau de vie trop
protégé peut supposer une capacité redistributive difficile à maintenir lorsque
la base fiscale se dégrade.

### Faux sentiment de précision

La granularité d'un simulateur peut donner une impression de rigueur supérieure
à celle des données disponibles. Des séries détaillées et des sorties
probabilistes ne compensent pas une source mal comprise ou une hypothèse
normative non signalée.

> **Complexité du modèle ≠ crédibilité de la prévision.**

## 4. Le pivot V8 : prévoir les résultats, pas chaque mécanisme

Le choix architectural majeur de V8 a été de réduire la surface de prévision
numérique à exactement trois cibles :

1. le taux de chômage ;
2. le PIB réel par habitant ;
3. le niveau de vie médian réel.

La dette, l'investissement, la démographie, la productivité, le climat,
l'énergie, la géopolitique et les conditions financières n'ont pas disparu.
Ils sont devenus des éléments de preuve causale, des moteurs de scénarios et du
contexte structurel, plutôt que des objectifs numériques indépendants.

Cette distinction a amélioré le projet de plusieurs façons :

- moins d'hypothèses numériques non soutenues ;
- validation plus ciblée ;
- interprétation plus directe ;
- comparaison plus lisible entre scénarios ;
- traçabilité plus claire entre une valeur et son origine.

La triade finale correspond à trois dimensions distinctes :

- **emploi** : accès au travail et sécurité économique ;
- **production** : capacité productive moyenne par personne ;
- **niveau de vie distribué** : résultat matériel de la personne médiane après
  salaires, impôts et transferts.

Elle remplace des dizaines de sorties par un petit ensemble de résultats
interprétables. C'est aussi pourquoi l'ancien Index composite a finalement été
retiré : une fois les trois cibles conservées, la normalisation et les poids
égaux ajoutaient une abstraction normative sans information indépendante
suffisante.

## 5. La construction des scénarios

V8 a reconstruit l'architecture autour d'un socle structurel commun et de
différences explicites de timing, de sévérité, de durée, de récupération et de
scarring. Tous les scénarios conservent des pressions comme le vieillissement,
la contrainte budgétaire, le sous-investissement, la productivité et la
compétitivité. Ils ne diffèrent pas par une opposition simpliste entre « aucun
choc » et « beaucoup de chocs ».

Les trois scénarios finaux sont :

- **Dégradation faible / least-bad** : les chocs sont plus tardifs ou mieux
  contenus, la récupération est plus forte et le scarring plus limité ;
- **Dégradation centrale** : les faiblesses structurelles persistent, des
  crises matérielles surviennent et la récupération reste partielle ;
- **Dégradation forte** : des chocs précoces ou composés se combinent à une
  récupération faible, une forte hystérèse et un scarring élevé.

« Faible » ne signifie donc pas prospérité. Le scénario least-bad reste une
détérioration structurelle ; il est seulement le moins défavorable des trois.
Cette précision a été ajoutée explicitement lors du contrôle de défendabilité
théorique V8.08d.

## 6. Séparer les risques des prévisions

Les risques ont été recherchés dans une couche séparée de la sélection des
cibles. La taxonomie couvre notamment :

- stress souverain et financier ;
- crise bancaire ou récession ;
- choc énergétique et climatique ;
- conflit ou escalade géopolitique ;
- fragmentation commerciale ;
- crise politique ou institutionnelle.

Les risques composés sont regroupés en clusters afin d'éviter de compter
plusieurs fois une même transmission. Les probabilités et les descriptions de
risque informent la construction des scénarios, mais ne sont pas converties
mécaniquement en dizaines de séries de prévisions intermédiaires.

Cette séparation est une amélioration méthodologique importante : la recherche
peut documenter ce qui pourrait arriver sans prétendre que chaque mécanisme
dispose d'un niveau numérique prévisible avec la même précision.

## 7. Le problème de cohérence

Avec seulement trois cibles, l'évaluation est devenue plus exigeante, pas moins.
La question n'était plus seulement :

> « Chaque nombre est-il plausible isolément ? »

Elle est devenue :

> « Ces nombres racontent-ils ensemble la même histoire économique ? »

Les contrôles ont porté notamment sur :

- l'ordre des scénarios ;
- chômage contre PIB par habitant ;
- chômage contre niveau de vie médian ;
- PIB contre niveau de vie ;
- ratio niveau de vie médian / PIB par habitant ;
- les phases 2025→2030, 2030→2040 et 2040→2050 ;
- les pentes annualisées ;
- l'ancrage au chômage observé de 2026.

Cela a permis de distinguer une incohérence économique d'une simple différence
de trajectoire. Le PIB par habitant n'a pas besoin de bouger exactement comme le
chômage : participation, âge de la population active, heures travaillées,
productivité, automatisation et PIB par travailleur peuvent modifier la
relation. En revanche, une protection croissante du niveau de vie médian dans
le scénario le plus dégradé devait rester compatible avec la capacité fiscale
et les salaires.

Les points n'ont été gelés qu'après ces contrôles conjoints. Le processus est
documenté par les revues de forme des trajectoires V8.05b, V8.07b, V8.08b et
V8.08c. Par exemple, les points de chômage 2030 optimiste et central ont été
réduits de 9,0 % à 8,5 % et de 9,7 % à 9,1 % afin de mieux respecter l'ancrage
observé et les phases du PIB et du niveau de vie.

## 8. La revue adversariale multi-modèles

Des modèles IA indépendants ont été utilisés pour challenger les sorties. La
critique externe n'était pas acceptée automatiquement : chaque objection
devait devenir une hypothèse testable dans le workflow principal.

Deux exemples ont été particulièrement utiles :

- la question d'une protection trop forte du niveau de vie médian par rapport
  au PIB dans les scénarios défavorables ;
- la cohérence dynamique du chômage entre l'ancrage récent, 2030 et les
  décennies suivantes.

Les désaccords ont donc déclenché des vérifications de ratio, de pente,
d'horizon et de cohérence inter-variable. Ils n'ont pas été tranchés par vote
entre modèles.

> **Le désaccord entre modèles est devenu un outil d'évaluation, pas un mécanisme de vote.**

## 9. La décision de supprimer l'Index

Les versions antérieures conservaient un Index FranceScope, construit à partir
des trois dimensions principales avec une normalisation et des pondérations.
Après le recentrage de V8, cet agrégat n'apportait plus assez d'information
indépendante :

- les trois variables brutes étaient déjà lisibles ;
- les poids égaux constituaient un choix normatif ;
- la normalisation ajoutait une couche d'abstraction ;
- l'Index pouvait détourner l'attention de la cohérence des résultats réels.

La décision finale a donc été de ne pas recalculer l'Index et de conserver les
trois trajectoires comme surface de sortie.

> **Une métrique synthétique ne vaut la peine que si elle apporte une information supplémentaire.**

## 10. L'ajout du benchmark institutionnel

Le benchmark institutionnel a été ajouté après le gel des trajectoires
FranceScope. Son objectif n'était pas de copier une prévision officielle, mais
de répondre à une question distincte :

> « Que projettent les institutions, et pourquoi FranceScope diffère-t-il ? »

La recherche a examiné la Banque de France, la Commission européenne, l'OCDE,
le FMI, l'INSEE et Eurostat. Les horizons publiés ont été conservés sans
prolongation silencieuse. Le benchmark est une référence à côté des scénarios,
pas un quatrième scénario FranceScope.

Cette séparation rend visible une différence essentielle entre :

- une prévision directe à court terme ;
- une projection structurelle de long terme ;
- une observation historique ;
- un proxy dérivé ;
- une hypothèse de scénario.

## 11. Le problème de provenance

Le projet a progressivement établi une taxonomie explicite :

- `OBSERVED` ;
- `DIRECT_FORECAST` ;
- `LONG_RUN_PROJECTION` ;
- `STRUCTURAL_ASSUMPTION` ;
- `DERIVED_PROXY`.

Cette distinction est indispensable lorsque les horizons et les définitions ne
sont pas identiques. Une valeur ne devient pas une prévision comparable
simplement parce qu'elle peut être convertie dans la même unité.

Le cas du PIB réel par habitant de la Commission européenne est instructif. Des
jalons de croissance potentielle ont d'abord été interprétés trop agressivement
pour construire une trajectoire de niveau. Le calcul était mathématiquement
valide, mais le sens de la source ne justifiait pas cette transformation : les
jalons ne garantissaient ni un taux constant entre les dates, ni un niveau
institutionnel directement comparable. La trajectoire de niveau a donc été
retirée ; les taux de croissance restent conservés comme référence
structurelle.

> **Une transformation mathématiquement valide peut être méthodologiquement fausse si la variable source est mal comprise.**

## 12. Accepter les données manquantes

Aucun forecast institutionnel direct et comparable du niveau de vie médian réel
à long terme n'a été trouvé. Le projet conserve l'ancrage observé de 2025 et
laisse `NA` au-delà, au lieu de fabriquer un benchmark.

De même, les niveaux institutionnels de PIB réel par habitant non directement
comparables ont été retirés. Cette décision peut sembler moins spectaculaire,
mais elle rend la comparaison plus honnête.

> **Une valeur manquante est préférable à une précision artificielle.**

## 13. L'évolution du workflow LLM

L'évolution macroéconomique s'est accompagnée d'une évolution du workflow
humain–LLM.

### Au début

Les instructions étaient plus ouvertes et supposaient davantage que le modèle
conserverait spontanément la direction du projet sur une longue séquence. Cette
approche facilitait l'exploration, mais elle laissait trop de décisions
implicites.

### Contraintes observées

Les difficultés rencontrées ont été traitées comme des contraintes
d'ingénierie :

- dérive par rapport à l'objectif ;
- boucles et répétitions ;
- approches échouées relancées sans changement de stratégie ;
- actions inutiles et gaspillage de tokens ;
- perte de l'état du projet ;
- recherches trop larges ;
- modifications de composants déjà validés ;
- mélange entre exploration historique et périmètre final.

### Refonte du workflow

Le workflow a ensuite introduit :

- un scope explicite ;
- des règles anti-loop ;
- une exploration bornée ;
- des conditions d'arrêt ;
- la minimisation des tokens ;
- des décisions gelées ;
- la règle du plus petit changement sûr ;
- des manifests de validation ;
- des handoffs structurés entre agents et modèles.

C'est à ce moment que FranceScope est devenu un véritable exercice de context
engineering. Le contexte n'est pas seulement une quantité d'informations : il
doit être sélectionné, hiérarchisé, maintenu et vérifié.

## 14. Mon rôle dans une architecture human-in-the-loop

La division du travail s'est clarifiée.

Les LLM ont accéléré :

- la recherche ;
- la génération de code ;
- la critique ;
- la synthèse ;
- la documentation ;
- l'analyse de candidats.

L'humain a conservé la responsabilité de :

- définir les objectifs ;
- décider de l'architecture ;
- rejeter les sorties insuffisamment fondées ;
- choisir ce qui devait être gelé ;
- rouvrir une hypothèse ;
- décider quand simplifier ;
- évaluer la crédibilité ;
- déterminer la direction finale du projet.

> **Le workflow est devenu dirigé par l'humain et accéléré par la machine, non autonome du modèle.**

## 15. Avant / après

| Dimension | FranceScope historique | FranceScope final |
|---|---|---|
| Sorties numériques | Nombreuses variables macro | 3 cibles finales |
| Complexité | Simulateur causal large | Cadre de scénarios ciblé |
| Validation | Centrée sur les équations et le modèle | Centrée sur les résultats et leur cohérence |
| Comparaison institutionnelle | Limitée ou hétérogène | Couche avec provenance et classifications |
| Workflow LLM | Davantage ouvert | Explicitement contraint |
| Gestion de l'état | Partiellement implicite | Décisions gelées et handoffs |
| Évaluation | Contrôles de modèle | Contrôles temporels, inter-variables et adversariaux |
| Index composite | Conservé dans les versions historiques | Supprimé du framework final |
| Données manquantes | Plus grande tentation de dériver | `NA` préféré à la précision non soutenue |

## 16. Les leçons majeures

1. **La complexité n'est pas la crédibilité.** La surface de sortie doit rester
   proportionnée à la force des preuves.
2. **L'évaluation compte davantage que la génération.** Une sortie plausible
   n'est qu'un candidat tant qu'elle n'a pas passé les contrôles.
3. **Plus de contexte n'est pas toujours un meilleur contexte.** Le contexte
   utile est ciblé, structuré et lié à la décision en cours.
4. **Les conditions d'arrêt sont essentielles.** Elles empêchent l'exploration
   de devenir une boucle sans amélioration mesurable.
5. **La fiabilité LLM exige un contrôle explicite de l'état.** Les décisions
   gelées et les handoffs évitent de reconstruire le projet à chaque étape.
6. **Le désaccord multi-modèles est utile lorsqu'il est opérationnalisé.** Une
   critique devient un test, pas une autorité.
7. **La provenance compte autant que l'arithmétique.** Une bonne formule sur une
   mauvaise interprétation de source reste une mauvaise méthode.
8. **La simplification peut être une amélioration d'ingénierie.** Réduire la
   surface finale peut renforcer l'auditabilité.
9. **`NA` peut être le résultat correct.** L'absence de donnée comparable doit
   rester visible.
10. **Le jugement humain reste architectural.** Le modèle accélère le travail,
    mais ne décide pas seul de ce qui est défendable.

## 17. Ce que le projet démontre

FranceScope démontre des compétences qui dépassent la production d'une
trajectoire macroéconomique :

- LLM engineering et context engineering ;
- contrôle d'agents et conception de garde-fous ;
- design d'évaluation ;
- orchestration et revue multi-modèles ;
- ingénierie de données et de recherche ;
- gestion de la provenance ;
- validation logicielle et analytique ;
- arbitrage entre cohérence, précision et lisibilité ;
- décisions de produit et de périmètre.

La valeur du projet tient donc autant à la manière dont le problème a été
structuré, contrôlé et révisé qu'aux chiffres finaux eux-mêmes.

## 18. Documentation connexe

- [README recruteur](../README.md) ;
- [état final du projet](FINAL_PROJECT_STATE.md) ;
- [workflow LLM fiable](reliable_llm_workflows.md) — documentation en cours ;
- [cadre d'évaluation](evaluation_framework.md) — documentation en cours ;
- [méthodologie du benchmark institutionnel](institutional_benchmark_methodology.md) ;
- [rapport technique](technical_report.md) — documentation en cours ;
- [échecs et leçons](failures_and_lessons.md) — documentation en cours ;
- [archive des versions historiques](../archive/historical_versions/README.md).
