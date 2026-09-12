# Cadre d'évaluation de FranceScope

Dans FranceScope, la génération n'était que la première étape. Une sortie
n'était pas acceptée parce qu'elle semblait plausible : elle devait passer
plusieurs niveaux de validation, portant sur les données, la cohérence
temporelle, la cohérence entre variables, l'ordre des scénarios, la
plausibilité historique, les sources et la revue adversariale.

> **Le problème n'était pas seulement de produire une prévision plausible, mais de définir ce qui permettait de l'accepter.**

Le cadre final à trois cibles évalue deux types de sorties :

1. les trajectoires et scénarios FranceScope ;
2. les analyses produites par les LLM et les extractions de sources
   institutionnelles.

## 1. La chaîne d'évaluation

```text
Sortie candidate
      ↓
Intégrité des données
      ↓
Cohérence temporelle
      ↓
Cohérence entre variables
      ↓
Ordre des scénarios
      ↓
Plausibilité historique
      ↓
Provenance et cohérence des sources
      ↓
Revue adversariale multi-modèles
      ↓
Gate de révision
      ↓
Gel / rejet / révision
```

Ces niveaux sont complémentaires. Un scénario peut respecter l'ordre
optimiste–central–pessimiste et rester temporellement incohérent. Une valeur
peut être correctement calculée et rester invalide parce que sa définition ou
son horizon ne correspondent pas à la source.

## 2. Intégrité des données

La première couche vérifie que la sortie représente bien ce qu'elle prétend
représenter :

- nom exact de la variable ;
- année ;
- scénario ;
- unité ;
- réel contre nominal ;
- pourcentage contre décimal ;
- observation contre prévision ;
- source et vintage ;
- cohérence avec les valeurs gelées.

Dans le périmètre final :

- le chômage est exprimé en pourcentage ;
- le PIB réel par habitant est exprimé en euros par personne, aux prix
  chaînés 2020 ;
- le niveau de vie médian réel est exprimé en euros par personne et par an, à
  prix constants.

Le point 2025 est un ancrage historique canonique. L'observation du chômage au
deuxième trimestre 2026 est un élément de contexte récent, pas un remplacement
du baseline formel. Cette séparation empêche une valeur observée et une valeur
prospective d'être mélangées sans le signaler.

Une erreur d'unité peut produire une trajectoire visuellement cohérente mais
économiquement fausse. C'est pourquoi l'intégrité des métadonnées précède les
tests de plausibilité.

## 3. Ordre des scénarios

Les scénarios finaux doivent conserver un ordre cohérent avec la désirabilité
de chaque variable.

Pour le chômage, variable défavorable :

```text
Dégradation faible < Dégradation centrale < Dégradation forte
```

Pour le PIB réel par habitant et le niveau de vie médian, variables favorables :

```text
Dégradation faible > Dégradation centrale > Dégradation forte
```

Cet ordre est nécessaire mais non suffisant. Trois courbes peuvent rester
correctement ordonnées tout en présentant des pentes, des ratios ou des
relations inter-variables impossibles à défendre. L'ordre est donc un gate
préliminaire, pas une preuve de cohérence complète.

## 4. Cohérence temporelle

Les trajectoires ont été examinées par blocs :

- 2025→2030 ;
- 2030→2040 ;
- 2040→2050.

Pour le chômage, l'analyse porte notamment sur la variation en points de
pourcentage par an. Pour le PIB par habitant et le niveau de vie médian, les
taux de croissance annualisés ou CAGR sont utilisés lorsque cela est pertinent.

Comparer seulement la variation brute sur cinq ans à celle sur dix ans peut
être trompeur. Une pente annualisée permet de distinguer un choc rapide d'une
détérioration progressive. Les revues ont aussi vérifié si la phase de chaque
variable racontait la même histoire : détérioration initiale, stagnation,
scarring persistant ou accélération tardive.

Un enseignement concret concerne le chômage dans le scénario least-bad. Ses
premiers points se détérioraient initialement trop vite par rapport aux phases
du PIB et du niveau de vie et à l'ancrage récent. Les pentes annualisées ont
révélé ce décalage. Les points 2030 optimiste et central ont ensuite été
révisés de 9,0 % à 8,5 % et de 9,7 % à 9,1 %. Les autres valeurs n'ont pas été
modifiées sans problème démontré.

## 5. Cohérence entre variables

Les relations principales examinées sont :

- chômage ↔ PIB réel par habitant ;
- chômage ↔ niveau de vie médian ;
- PIB réel par habitant ↔ niveau de vie médian.

FranceScope n'impose pas une élasticité déterministe entre ces variables. Le
cadre pose une question plus robuste : les trois séries racontent-elles la même
histoire macroéconomique ?

Par exemple, une baisse du PIB par habitant plus rapide alors que la hausse du
chômage ralentit peut être défendable si le vieillissement, la participation,
les heures travaillées, la productivité ou le PIB par travailleur jouent un rôle
important. À l'inverse, un niveau de vie médian qui devient progressivement
trop protégé dans le scénario le plus défavorable peut supposer une capacité
redistributive incompatible avec la faiblesse des salaires et de la base
fiscale.

Le contrôle vise donc les contradictions substantielles, pas l'imposition d'une
relation mécanique qui ferait disparaître les mécanismes économiques
pertinents.

## 6. Diagnostics de relations et de ratios

Des diagnostics secondaires ont servi à détecter des incohérences :

- ratio niveau de vie médian / PIB par habitant ;
- écart entre scénarios selon l'horizon ;
- différence de PIB par habitant par point de chômage ;
- différence de niveau de vie par point de chômage ;
- élargissement de l'incertitude entre 2030, 2040 et 2050.

> **Les ratios servaient à détecter des incohérences, pas à forcer les données à respecter une formule.**

Ils ne constituent donc pas des équations de calibration cachées. Un ratio
inhabituel déclenche une revue de mécanisme et de source ; il ne suffit pas à
justifier une correction automatique.

## 7. Plausibilité historique

Les analogues historiques contraignent l'espace des scénarios sans devenir des
prévisions mécaniques. Les références françaises comprennent notamment :

- la persistance du chômage au début des années 1990 ;
- la crise financière mondiale ;
- la crise de la zone euro ;
- le choc de la COVID ;
- la stagnation récente.

Les comparaisons internationales incluent l'Espagne, la Grèce, le Portugal,
l'Italie et le Japon. Ces épisodes permettent de tester si une combinaison de
chômage, production et niveau de vie se situe dans une plage historiquement
défendable.

Un analogue n'est jamais transféré automatiquement à la France. Il sert à
poser une question de plausibilité : une telle combinaison a-t-elle déjà
existé, dans quel régime institutionnel et avec quelle durée ? Les différences
de démographie, de monnaie, de protection sociale et de structure productive
restent explicites.

## 8. Contrôle des ancrages récents

Deux références temporelles sont distinguées :

- le baseline annuel observé de 2025 ;
- l'ancrage contextuel du chômage observé au deuxième trimestre 2026.

Le second a permis de tester si les points 2030 impliquaient une détérioration
compatible avec la phase récente. Il n'a pas été utilisé pour réécrire
l'historique ni pour transformer 2026 en nouveau baseline.

Cette distinction est importante pour l'évaluation : une observation récente
peut contraindre une transition sans devenir elle-même une prévision ou un
remplacement silencieux de la définition officielle.

## 9. Revue adversariale multi-modèles

Un autre modèle pouvait jouer le rôle de critique, de vérificateur de
plausibilité ou d'évaluateur adversarial. Le processus était :

1. un modèle critique la sortie ;
2. la critique est convertie en hypothèse explicite ;
3. le problème est reproduit ;
4. les données et la méthodologie sont vérifiées ;
5. une révision n'est acceptée que si elle est justifiée.

Les exemples comprennent :

- une protection potentiellement excessive du niveau de vie par rapport au PIB ;
- un mauvais timing du chômage optimiste ;
- un décalage du chômage central sur l'horizon 2030.

> **Le second modèle n'était pas une autorité : il était un générateur d'hypothèses adversariales.**

Le désaccord entre modèles n'est donc pas résolu par vote. Il devient une
source de tests supplémentaires.

## 10. Évaluation de la traçabilité des sources

Les valeurs institutionnelles sont évaluées au niveau de la source. Un
datapoint affiché doit, lorsque l'information est disponible, conserver :

- institution ;
- publication ;
- date ;
- variable ;
- année ;
- unité ;
- définition ;
- type de prévision ;
- URL source ;
- justification.

Cette règle peut être résumée ainsi :

> **Pas de valeur orpheline.**

Une valeur sans source, horizon ou définition ne peut pas être comparée à une
trajectoire FranceScope avec le même niveau de confiance qu'une observation
documentée.

## 11. Évaluation du type de source

La taxonomie distingue :

- `OBSERVED` : valeur historique observée ;
- `DIRECT_FORECAST` : prévision directe publiée pour un horizon donné ;
- `LONG_RUN_PROJECTION` : projection structurelle conditionnelle ;
- `STRUCTURAL_ASSUMPTION` : hypothèse de scénario ou de mécanisme ;
- `DERIVED_PROXY` : proxy ou transformation qui ne doit pas être présenté comme
  une prévision directe.

Une projection structurelle de la Commission européenne sur le chômage des
20–64 ans peut être une référence utile sans être une prévision directe
identique à la définition FranceScope. Cette distinction est conservée dans
les fichiers institutionnels et dans l'interprétation.

## 12. Compatibilité des définitions

Les contrôles portent sur :

- le périmètre d'âge du chômage ;
- PIB total contre PIB par habitant ;
- réel contre nominal ;
- euros contre parité de pouvoir d'achat ;
- fréquence annuelle contre trimestrielle ;
- définition du niveau de vie médian ;
- observation contre série modélisée.

L'exemple du chômage européen est important : une valeur portant sur les
20–64 ans peut être utile pour un repère de long terme, mais elle n'est pas
silencieusement identique à toutes les définitions ou fréquences du projet.

Cette vérification empêche qu'une comparaison apparemment précise masque en
réalité deux concepts différents.

## 13. Intégrité de l'horizon

Les règles d'horizon sont explicites :

- ne pas prolonger une prévision court terme jusqu'en 2050 ;
- ne pas traiter un jalon de croissance comme un taux moyen sur tout
  l'intervalle ;
- ne pas convertir un taux de croissance insuffisant en niveau ;
- ne pas appeler un proxy une prévision officielle.

L'erreur de niveau de PIB réel par habitant dérivé des jalons européens est un
cas concret. Le calcul pouvait être arithmétiquement correct, mais la source ne
justifiait pas un niveau institutionnel comparable. La trajectoire de niveau a
été supprimée ; les jalons de croissance ont été conservés comme références.

> **Une erreur d'horizon ou de définition peut être plus dangereuse qu'une erreur arithmétique.**

## 14. Évaluer la justification institutionnelle

Pour chaque référence, le cadre sépare :

- l'explication explicitement donnée par l'institution ;
- l'interprétation de FranceScope.

Si aucune justification source n'est disponible, cela doit être indiqué. Le
workflow ne doit pas attribuer à une institution un mécanisme qu'elle n'a pas
déclaré. Cette séparation est particulièrement importante lorsque FranceScope
explique pourquoi ses scénarios sont plus défavorables sans prétendre que les
institutions sont « erronées ».

## 15. Le gate de révision

Une valeur gelée ne doit pas changer simplement parce que :

- un autre modèle ne l'aime pas ;
- une courbe plus lisse semble plus esthétique ;
- un diagnostic isolé paraît inhabituel.

Une révision nécessite au moins :

- une incohérence démontrée ;
- une preuve plus forte ;
- ou une erreur de source ou de définition.

La philosophie est celle d'une révision ciblée, généralement en un nombre limité
de passes. Chaque changement doit être attribuable à un problème précis et
repasser les validations concernées.

## 16. La plus petite révision sûre

Lorsqu'un problème est démontré, le cadre change le plus petit nombre de cellules
nécessaire. Les exemples incluent :

- un point de chômage optimiste sur un horizon donné ;
- les deux points de chômage 2030 révélés incohérents avec la phase récente ;
- certains points du niveau de vie lorsque le ratio avec le PIB impliquait une
  protection excessive.

Cette approche améliore :

- la traçabilité ;
- le risque de régression ;
- la validation post-révision ;
- l'attribution causale de l'amélioration.

## 17. Les états d'acceptation

Les revues utilisent un vocabulaire commun :

- **STRONG** : cohérence clairement établie ;
- **ACCEPTABLE** : trajectoire défendable avec un mécanisme explicite ;
- **WEAK** : point nécessitant une revue supplémentaire ;
- **INCONSISTENT** : contradiction qui ne peut pas rester gelée.

Un bloc de trajectoire final ne doit pas rester `WEAK` ou `INCONSISTENT`.
`ACCEPTABLE` n'est pas synonyme de certain : cela signifie que l'hypothèse est
explicite et qu'aucune contradiction rédhibitoire n'a été trouvée.

## 18. Les manifests de validation

Les manifests rendent les contrôles lisibles par une machine et par un
relecteur. Ils peuvent conserver :

- les valeurs modifiées ;
- les fichiers mis à jour ;
- les checks passés ;
- l'état de calcul ou non de l'Index ;
- l'état de modification ou non de V7 ;
- le verdict.

Ils forment une piste d'audit entre une révision et la décision de gel. Cette
structure réduit la dépendance à la mémoire conversationnelle du modèle.

## 19. Critères de gel final

Une couche peut être gelée lorsque :

- les valeurs source sont vérifiées ;
- les définitions sont comprises ;
- l'ordre des scénarios est valide ;
- les contrôles temporels passent ;
- les contrôles inter-variables passent ;
- aucun état `WEAK` ou `INCONSISTENT` non résolu ne subsiste ;
- la critique adversariale a été traitée ;
- la révision éventuelle a été revalidée ;
- l'humain accepte le résultat.

Le gel transforme alors une sortie candidate en état autoritatif. Toute
réouverture ultérieure doit être explicitement motivée.

## 20. Exemples d'évaluations

| Problème détecté | Évaluation qui l'a révélé | Résultat |
|---|---|---|
| Protection trop forte du niveau de vie par rapport au PIB | Ratio médian / PIB et revue théorique | Révision des points concernés et protection rendue plus défendable |
| Chômage optimiste trop rapide au début | Pentes annualisées et comparaison aux phases du PIB et du niveau de vie | Point 2030 ramené de 9,0 % à 8,5 % |
| Décalage du chômage central à l'horizon court | Ancrage chômage 2026 Q2 et revue early-horizon | Point 2030 ramené de 9,7 % à 9,1 % |
| Niveau institutionnel de PIB par habitant insuffisamment fondé | Gate de provenance et intégrité d'horizon | Niveau dérivé supprimé ; taux de croissance conservés |
| Benchmark institutionnel long terme du niveau de vie absent | Recherche de source directe et contrôle de comparabilité | `NA` conservé après 2025 |

## 21. Ce que cela démontre pour l'ingénierie LLM

Le cadre matérialise :

- la conception de critères d'évaluation ;
- les tests adversariaux ;
- la validation des sources ;
- les quality gates adaptés à la tâche ;
- les manifests lisibles par machine ;
- le contrôle des régressions ;
- la revue human-in-the-loop ;
- la séparation entre génération et acceptation.

> **Le modèle générait des candidats ; le framework décidait s'ils étaient acceptables.**

L'intérêt LLM engineering n'est donc pas seulement de demander une meilleure
réponse. Il consiste à définir les conditions d'acceptation, à transformer les
critiques en tests, à conserver l'état et à refuser une précision que les
sources ne soutiennent pas.

## 22. Limitations et limites

- Il n'existe pas encore de backtesting statistique des résultats 2050.
- Les contrôles de long terme sont principalement des évaluations de
  plausibilité et de cohérence, pas des mesures de précision prédictive.
- Certains seuils d'évaluation restent qualitatifs.
- Les analogues historiques sont imparfaits.
- Une revue multi-modèles ne constitue pas une validation scientifique
  indépendante.

Le cadre réduit les erreurs évitables et rend les décisions auditables ; il ne
supprime ni l'incertitude macroéconomique ni la part de jugement des scénarios.

## 23. Documentation connexe

- [README recruteur](../README.md) ;
- [évolution du projet](project_evolution.md) ;
- [workflow LLM fiable](reliable_llm_workflows.md) ;
- [méthodologie du benchmark institutionnel](institutional_benchmark_methodology.md) ;
- [échecs et leçons](failures_and_lessons.md) — documentation en cours ;
- [rapport technique](technical_report.md) — documentation en cours ;
- [état final du projet](FINAL_PROJECT_STATE.md).
