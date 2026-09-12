# Échecs utiles et leçons d'ingénierie

FranceScope s'est construit par essais, contrôles et révisions successives.
Les problèmes rencontrés n'ont pas été traités comme de simples défauts
locaux à corriger. Ils ont servi de signaux sur l'architecture, le workflow
LLM, la provenance et les critères d'acceptation.

> **Un bon système n'est pas celui qui ne se trompe jamais, mais celui qui rend ses erreurs détectables, explicables et corrigibles.**

Chaque cas suit la même structure d'analyse :

- **PROBLÈME OBSERVÉ** — le symptôme constaté ;
- **POURQUOI C'ÉTAIT IMPORTANT** — le risque créé pour le projet ;
- **DIAGNOSTIC** — la cause ou la limite identifiée ;
- **DÉCISION** — la réponse d'ingénierie choisie ;
- **RÉSULTAT** — ce qui a changé après la réponse ;
- **LEÇON** — le principe réutilisable.

Les sous-titres peuvent regrouper **DIAGNOSTIC**, **DÉCISION** et **RÉSULTAT**
lorsqu'ils décrivent une même décision, mais chaque cas conserve cette chaîne
de raisonnement.

## 1. La complexité n'était pas la crédibilité

### Problème observé

Les versions V1 à V7 ont progressivement représenté de nombreuses variables
macroéconomiques et leurs interactions : investissement, crédit, demande,
commerce, inflation, travail, démographie, productivité, énergie, climat,
finances publiques et risques géopolitiques.

### Pourquoi c'était important

Cette architecture était riche et utile pour raisonner sur les mécanismes, mais
chaque variable intermédiaire numérique ajoutait des hypothèses et une nouvelle
surface à valider. La sophistication pouvait donner une impression de rigueur
supérieure à la force réelle des preuves.

### Diagnostic

Le problème n'était pas seulement une équation mal codée. La surface de
prévision elle-même était trop large pour rester facilement défendable.

### Décision et résultat

V8 a réduit la surface numérique à trois cibles : chômage, PIB réel par
habitant et niveau de vie médian réel. Les autres domaines sont devenus des
moteurs de scénarios, des éléments de preuve ou du contexte structurel.

Le résultat est plus facile à auditer, à comparer et à expliquer.

### Leçon

> **Complexité du modèle ≠ crédibilité de la prévision.**

Pour un ingénieur, savoir abandonner une architecture devenue contre-productive
est parfois plus important que savoir lui ajouter une fonctionnalité.

## 2. La plausibilité locale ne garantissait pas la cohérence globale

### Problème observé

Des valeurs individuelles de chômage, de PIB par habitant et de niveau de vie
pouvaient sembler plausibles séparément, alors que leurs pentes, leurs phases ou
leurs ratios racontaient des histoires différentes.

### Pourquoi c'était important

Une sortie locale convaincante peut devenir incohérente lorsqu'elle est replacée
dans le temps ou comparée aux autres cibles. Le risque était d'accepter trois
bonnes phrases ou trois bons nombres qui ne formaient pas un scénario
économique défendable.

### Diagnostic

Les contrôles de plausibilité individuelle ne suffisaient pas. Il fallait
évaluer les relations entre variables et les transitions 2025→2030,
2030→2040 et 2040→2050.

### Décision et résultat

Des revues temporelles et cross-variable ont été introduites. Elles ont révélé
notamment un timing trop pessimiste du chômage optimiste au début de l'horizon,
un décalage central sur 2030 et une protection du niveau de vie à comparer plus
strictement au PIB.

Les points ont été révisés uniquement lorsqu'une incohérence démontrée le
justifiait.

### Leçon

> **Une sortie peut sembler raisonnable seule et devenir incohérente dès qu'on la compare au reste du système.**

Cela a transformé l'évaluation d'un contrôle de sortie unique en un contrôle de
relations.

## 3. Plus de raisonnement ne produisait pas toujours une meilleure exécution

### Problème observé

Un LLM pouvait continuer à lire, rechercher, comparer ou auditer alors que les
éléments nécessaires à la décision étaient déjà disponibles.

### Pourquoi c'était important

La réflexion supplémentaire pouvait augmenter la latence, le bruit et le coût
sans réduire l'incertitude pertinente. Elle pouvait même réintroduire des
questions déjà gelées.

### Diagnostic

Le problème était un manque de conditions d'arrêt et de limites d'exploration,
pas un manque de puissance de raisonnement.

### Décision et résultat

Le workflow a introduit l'exploration bornée, les recherches ciblées, les
conditions d'arrêt et l'interdiction des audits sans risque identifié.

### Leçon

> **Plus de raisonnement n'est utile que s'il réduit l'incertitude pertinente.**

L'autonomie utile implique aussi de reconnaître que la tâche est terminée.

## 4. Les approches échouées pouvaient se répéter

### Problème observé

Après un échec d'outil, de commande ou d'hypothèse, le modèle pouvait réessayer
une opération pratiquement identique.

### Pourquoi c'était important

Un modèle capable peut rester prisonnier d'un motif local d'exécution. Chaque
nouvelle tentative donne l'impression d'une activité, mais aucune information
nouvelle n'est produite.

### Diagnostic et décision

Deux règles explicites ont été introduites :

> **Never repeat the exact same failed tool call.**

> **If an approach fails twice without measurable progress, change the hypothesis, tool, command, file, or implementation strategy.**

### Résultat et leçon

Le changement de stratégie est devenu obligatoire après deux échecs sans
progrès mesurable.

> **Une règle anti-loop transforme l'échec en signal de changement de stratégie.**

## 5. Une action techniquement valide pouvait être sans rapport avec l'objectif

### Problème observé

Certains appels d'outils ou audits étaient valides en eux-mêmes mais ne
rapprochaient pas du livrable : recherche trop large, nettoyage annexe,
refactorisation ou validation redondante.

### Pourquoi c'était important

L'activité de l'agent pouvait augmenter alors que la valeur de décision restait
nulle. Cela compliquait aussi la revue en ajoutant des modifications étrangères
au problème.

### Décision et résultat

La règle suivante a été appliquée :

> **Every tool call must directly advance the requested task.**

Chaque action devait être reliée à une question, une décision ou une
validation. Le travail sans valeur de décision a été écarté.

### Leçon

> **L'autonomie utile n'est pas la capacité à faire plus, mais à faire uniquement ce qui rapproche du résultat.**

## 6. L'état du projet pouvait dériver ou être perdu

### Problème observé

Sur un projet long, des décisions déjà validées pouvaient redevenir ambiguës :
valeurs gelées, couches méthodologiques acceptées, distinction entre V7 et V8,
ou statut du benchmark institutionnel.

### Pourquoi c'était important

La perte d'état crée des régressions invisibles. Un modèle peut réintroduire un
ancien artefact non parce qu'il est meilleur, mais parce qu'il n'a plus accès à
la décision qui l'avait écarté.

### Décision et résultat

Le workflow a utilisé :

- des fichiers autoritatifs ;
- des décisions gelées ;
- des phases versionnées ;
- des manifests de validation ;
- des handoffs structurés avec `PROJECT_VERSION`, `VALUES_CHANGED`,
  `FILES_UPDATED`, `VALIDATION`, `VERDICT` et `NEXT_ACTION`.

La continuité entre sessions et modèles est devenue un artefact explicite.

### Leçon

> **Un projet long a besoin d'un état explicite, pas seulement d'une conversation longue.**

## 7. La surédition après le succès augmentait le risque

### Problème observé

Après qu'un résultat avait passé les contrôles demandés, l'agent pouvait
continuer à refactoriser, auditer ou modifier des fichiers voisins.

### Pourquoi c'était important

Une fois le problème résolu, le risque dominant devient la régression. Chaque
modification supplémentaire rend également plus difficile l'attribution de
l'amélioration ou de la dégradation.

### Décision et résultat

Trois règles ont été appliquées :

- plus petit changement sûr ;
- arrêt lorsque le résultat est validé ;
- réouverture formelle pour une couche gelée.

### Leçon

> **Arrêter au bon moment fait partie de l'ingénierie.**

## 8. La confiance d'un seul modèle ne suffisait pas

### Problème observé

Un modèle pouvait produire une argumentation interne persuasive et manquer
pourtant une incohérence entre le niveau de vie et le PIB, ou un problème de
timing du chômage.

### Pourquoi c'était important

Une réponse bien écrite n'est pas une preuve indépendante. La confiance
subjective du même modèle ne doit pas être confondue avec une validation.

### Décision et résultat

Des modèles indépendants ont été utilisés comme critiques, relecteurs
adversariaux et vérificateurs de plausibilité. Le workflow était :

```text
critique → hypothèse → reproduction → vérification des preuves → gate de révision
```

Il ne s'agissait pas de voter entre modèles. Chaque critique devait produire un
test reproductible avant de pouvoir changer une valeur.

### Leçon

> **Le désaccord entre modèles n'est utile que s'il devient testable.**

## 9. Une transformation mathématiquement correcte pouvait être méthodologiquement fausse

### Problème observé

Des jalons de croissance du PIB réel par habitant publiés par la Commission
européenne ont été utilisés pour dériver une trajectoire de niveaux en
euros/personne par capitalisation.

### Pourquoi c'était important

Le calcul était arithmétiquement valide, mais il ajoutait une hypothèse de taux
constant entre les jalons que la source ne garantissait pas.

### Diagnostic et décision

Le problème était sémantique : un jalon de croissance structurelle n'était pas
un niveau institutionnel directement publié. La trajectoire dérivée a été
supprimée ; les jalons de croissance ont été conservés comme références.

### Résultat et leçon

Le benchmark institutionnel de niveau GDPpc à long terme reste `NA`.

> **Une transformation mathématiquement correcte peut être méthodologiquement fausse.**

La provenance et le sens de la variable priment sur l'arithmétique seule.

## 10. La fausse précision était pire que la donnée manquante

### Problème observé

Aucune prévision institutionnelle directement comparable du niveau de vie
médian réel à long terme n'a été trouvée. Un proxy pouvait être envisagé.

### Pourquoi c'était important

Présenter ce proxy comme un benchmark officiel aurait masqué les hypothèses de
distribution des revenus, d'impôts et de transferts et aurait donné une
impression de précision non soutenue.

### Décision et résultat

Le benchmark officiel reste `NA` après l'ancrage observé de 2025. Un éventuel
proxy illustratif reste séparé du benchmark principal et ne devient pas une
valeur de consensus.

### Leçon

> **Une valeur manquante est préférable à une précision artificielle.**

## 11. L'Index composite n'ajoutait plus assez de valeur

### Problème observé

Après la réduction de V8 à trois cibles finales, l'Index composite devenait
redondant.

### Pourquoi c'était important

Les poids égaux étaient normatifs, la normalisation ajoutait une abstraction et
le résultat ne fournissait pas d'information indépendante suffisante par rapport
aux trois variables brutes.

### Décision et résultat

L'Index a été supprimé du framework final. Les cibles brutes sont devenues la
sortie principale, plus lisible et plus directement interprétable.

### Leçon

> **Une abstraction doit être supprimée lorsqu'elle n'ajoute plus d'information.**

Cette décision illustre le jugement produit et la discipline de périmètre.

## 12. Le prompt engineering seul ne suffisait pas

### Problème observé

Une formulation plus précise ne résolvait pas à elle seule la perte d'état, la
dérive de scope, la provenance, la répétition d'échecs ou le comportement
d'arrêt.

### Diagnostic et décision

Le projet a évolué vers le context engineering : scope, état autoritatif,
décisions gelées, typage des sources, contraintes d'outils, gates de validation,
stop conditions et handoffs structurés.

### Résultat et leçon

Les instructions sont devenues un contrat d'exécution plutôt qu'une simple
demande de texte.

> **Le prompt est une partie du système, pas le système entier.**

## 13. Plus de contexte pouvait réduire la qualité

### Problème observé

Les relectures intégrales et les contextes trop larges consommaient des tokens,
diluaient les contraintes utiles et pouvaient réintroduire des décisions
obsolètes.

### Décision et résultat

Le workflow a privilégié les lectures ciblées, les recherches bornées, les
fichiers autoritatifs et l'absence de relecture des fichiers inchangés sans
raison démontrée.

### Leçon

> **Moins de contexte, mieux sélectionné, peut produire un meilleur raisonnement.**

Le context engineering concerne donc la sélection et la hiérarchie, pas
seulement la quantité.

## 14. Les sources institutionnelles n'étaient pas homogènes

### Problème observé

Le matériau institutionnel mélangeait observations, prévisions de court terme,
projections structurelles, hypothèses de scénario et proxies.

### Pourquoi c'était important

Appeler l'ensemble « consensus institutionnel » aurait masqué les différences
d'horizon, de définition et de statut.

### Décision et résultat

La taxonomie explicite a été appliquée :

`OBSERVED`, `DIRECT_FORECAST`, `LONG_RUN_PROJECTION`,
`STRUCTURAL_ASSUMPTION`, `DERIVED_PROXY`.

La référence CE de chômage 20–64 ans est ainsi conservée comme projection
structurelle de long terme, non comme prévision directe homogène avec les
prévisions court terme.

### Leçon

> **Une source fiable peut être mal utilisée si son type est mal compris.**

## 15. Ce qui a changé dans ma pratique d'ingénierie

| Réflexe initial | Pratique mature |
|---|---|
| Ajouter du détail au modèle | Réduire la surface de prévision |
| Demander au modèle de raisonner davantage | Définir des gates d'évaluation |
| Donner davantage de contexte | Curater le contexte autoritatif |
| Réessayer une approche échouée | Forcer un changement de stratégie |
| Laisser l'agent continuer | Utiliser des stop conditions |
| Faire confiance à un modèle fort | Organiser une revue adversariale |
| Lisser une sortie étrange | Exiger une incohérence démontrée |
| Remplir les données manquantes | Préférer `NA` si la preuve manque |
| Conserver une métrique utile en apparence | Supprimer les abstractions redondantes |
| Traiter le prompt comme contrôle principal | Concevoir contexte, état et workflow |

## 16. Les leçons les plus importantes

1. La complexité n'est pas la crédibilité.
2. L'évaluation compte davantage que la génération.
3. La capacité n'est pas la fiabilité.
4. L'état doit être explicite.
5. Les conditions d'arrêt font partie de la spécification.
6. La revue multi-modèles doit être opérationnalisée.
7. La provenance compte autant que l'arithmétique.
8. Une donnée manquante peut être la bonne réponse.
9. La simplification peut renforcer la rigueur.
10. Le jugement humain reste architectural.

## 17. Ce que cela démontre pour un recruteur LLM Engineer

FranceScope démontre une expérience pratique de :

- context engineering, avec scope, état et décisions gelées ;
- contraintes d'agents et discipline d'utilisation des outils ;
- efficacité des tokens par exploration ciblée ;
- gestion d'état sur un projet long ;
- design d'évaluation et contrôle des régressions ;
- revue adversariale multi-modèles ;
- provenance et alignement des définitions ;
- architecture human-in-the-loop ;
- arbitrage de produit et de périmètre.

Chaque compétence correspond à un mécanisme concret : la règle anti-loop, le
gate de provenance, le gel des valeurs, les manifests, la revue des pentes ou
le choix de `NA`. Il ne s'agit pas seulement de mots-clés, mais de contraintes
qui ont modifié le fonctionnement du projet.

## 18. Limites

- Les contrôles ont été principalement implémentés par des instructions
  disciplinées, des fichiers structurés, des scripts et des manifests, plutôt
  que par une plateforme de production d'agents autonome.
- La revue multi-modèles n'est pas une revue scientifique indépendante.
- La prévision de long terme demeure très incertaine.
- Les leçons sont issues de ce projet, même si plusieurs principes sont
  généralisables.

Ces limites renforcent la portée réelle de la démonstration : il s'agit d'un
cas d'étude d'ingénierie et de pilotage, pas d'une preuve d'autonomie générale.

## 19. Documentation connexe

- [README recruteur](../README.md) ;
- [évolution du projet](project_evolution.md) ;
- [workflow LLM fiable](reliable_llm_workflows.md) ;
- [cadre d'évaluation](evaluation_framework.md) ;
- [méthodologie du benchmark institutionnel](institutional_benchmark_methodology.md) ;
- [rapport technique](technical_report.md) — documentation en cours ;
- [état final du projet](FINAL_PROJECT_STATE.md).
