# Construire un workflow LLM fiable sur un projet long

FranceScope s'est développé sur de nombreuses itérations et a mobilisé
plusieurs modèles, outils et types de travail : recherche, code, traitement de
données, raisonnement économique, critique, calibration et documentation. La
capacité brute d'un modèle ne suffisait pas. Il fallait maintenir la direction
du projet, contrôler les actions, conserver l'état, vérifier les sources et
arrêter les explorations au bon moment.

> **Un LLM peut être très intelligent localement tout en étant peu fiable à l'échelle d'un projet de plusieurs semaines.**

Le principal défi n'était donc pas d'obtenir une réponse brillante une fois. Il
fallait maintenir des modèles puissants mais imparfaits alignés sur un objectif
complexe pendant la durée du projet, en contrôlant le contexte, les actions, les
boucles, les sources, les validations et les décisions.

Ce document décrit les pratiques qui ont progressivement transformé FranceScope
en cas d'étude de **context engineering**, de contrôle d'agents, de gestion
d'état à long horizon, d'évaluation et de jugement humain dans un workflow
assisté par LLM.

## 1. Pourquoi les workflows LLM longs échouent

### Dérive de l'objectif

Un modèle peut optimiser la tâche locale — répondre à la dernière question,
réécrire un fichier ou poursuivre une recherche — tout en perdant l'objectif
global. Dans FranceScope, une amélioration locale pouvait éloigner le travail
du périmètre final à trois cibles.

### Perte d'état

Les décisions importantes ne sont pas toujours présentes dans le contexte actif
d'une session. Une valeur gelée, une définition de variable ou une contrainte de
provenance peut alors être traitée comme une question encore ouverte.

### Boucles de réflexion

Une exploration peut continuer parce qu'une réponse supplémentaire semble
possible, même lorsqu'elle ne réduit plus l'incertitude pertinente. Le modèle
peut multiplier les recherches, les audits ou les reformulations sans progrès
mesurable.

### Répétition d'approches ratées

Sans règle explicite, une commande ou une hypothèse qui a échoué peut être
relancée presque à l'identique. Cela consomme du temps et des tokens sans
augmenter la probabilité de réussite.

### Actions inutiles

Un appel d'outil peut être techniquement valide et pourtant sans rapport direct
avec le résultat demandé : nettoyage annexe, refactorisation opportuniste,
recherche latérale ou audit sans pouvoir de décision.

### Gaspillage de tokens

Les relectures intégrales, recherches redondantes et longs dumps intermédiaires
augmentent le coût, la latence et le bruit. Ils peuvent aussi rendre le
raisonnement moins fiable en noyant les contraintes importantes.

### Surédition

Après avoir résolu le problème, un agent peut continuer à modifier des fichiers
déjà validés. Le risque n'est plus l'absence de solution, mais la régression.

### Cohérence locale sans cohérence globale

Chaque sortie peut sembler plausible tout en contredisant les autres variables ou
les périodes précédentes. Une trajectoire de chômage raisonnable seule peut être
incompatible avec le PIB et le niveau de vie médian.

### Confusion de provenance

Une transformation peut être correcte arithmétiquement mais incorrecte
sémantiquement. Un taux de croissance institutionnel ne devient pas
automatiquement un niveau institutionnel comparable.

> **Le problème n'était donc pas seulement la qualité des prompts, mais la discipline d'exécution du système.**

## 2. Du prompt engineering au context engineering

Au début, l'approche consistait surtout à chercher une meilleure formulation :

> « Écrire un meilleur prompt. »

L'expérience a déplacé la question vers :

> « Contrôler ce que le modèle sait, ce qu'il peut toucher, ce qu'il peut faire ensuite, quand il doit s'arrêter et ce qui constitue une réussite. »

Dans ce projet, le contexte comprend donc :

- le rappel de l'objectif ;
- l'état autoritatif du projet ;
- le périmètre de la tâche ;
- les fichiers autorisés et interdits ;
- les opérations permises ;
- les décisions gelées ;
- les critères d'évaluation ;
- les conditions d'arrêt ;
- la provenance des sources ;
- la structure du handoff vers l'étape suivante.

> **Le contexte n'est pas seulement le texte envoyé au modèle. C'est aussi l'état, les règles, les frontières et les critères d'acceptation.**

Le gain principal ne vient pas d'un prompt plus long, mais d'un contrat
d'exécution plus explicite.

## 3. Les règles anti-loop

Deux principes ont été utilisés comme garde-fous opérationnels :

> **Never repeat the exact same failed tool call.**

> **If an approach fails twice without measurable progress, change the hypothesis, tool, command, file, or implementation strategy.**

Ces règles ont quatre effets :

- empêcher la répétition mécanique d'un échec ;
- forcer un changement d'hypothèse ou de stratégie ;
- limiter le gaspillage de tokens et de temps ;
- éviter qu'un agent reste bloqué dans une boucle d'exécution.

Un échec n'est donc pas seulement un message à ignorer. Il devient une
information sur la stratégie actuelle. Après deux tentatives sans progrès, le
workflow doit changer de niveau : lire un fichier plus ciblé, vérifier une
dépendance, utiliser une autre méthode ou reconsidérer l'hypothèse.

## 4. Exploration bornée

La recherche ouverte a progressivement été remplacée par une exploration bornée.
Avant une lecture ou une recherche, le workflow doit préciser :

- quelles sources ou quels fichiers sont nécessaires ;
- quelle question l'action doit résoudre ;
- quelle preuve serait suffisante ;
- quand l'exploration doit s'arrêter.

Les règles pratiques sont :

- nommer les sources exactes à inspecter avant une recherche large ;
- limiter les lectures à la section pertinente ;
- définir une condition d'arrêt ;
- ne pas prolonger une recherche lorsque l'évidence est insuffisante ;
- documenter `NA` plutôt que remplacer l'absence de preuve par une supposition.

> **Explorer davantage n'est utile que si chaque nouvelle action réduit réellement l'incertitude pertinente.**

Cette approche améliore le contrôle des tokens, la latence, la concentration et
la reproductibilité. Elle évite également de confondre une recherche plus longue
avec une recherche plus fiable.

## 5. La règle de pertinence par rapport à l'objectif

Une règle centrale du workflow est :

> **Every tool call must directly advance the requested task.**

Elle empêche les nettoyages sans rapport, les recherches latérales, les
refactorisations non nécessaires et les branches exploratoires sans valeur de
décision. Elle impose une décomposition claire :

1. quel résultat est demandé ;
2. quelle information manque ;
3. quelle action minimale peut l'obtenir ;
4. quelle validation prouve que le résultat est atteint.

Pour un recruteur LLM/AI, cette discipline est aussi une compétence de
décomposition de tâche et de contrôle d'exécution. L'objectif n'est pas de
faire davantage d'actions, mais de faire les actions qui modifient réellement
la décision ou le livrable.

## 6. Une efficacité de tokens qui améliore le raisonnement

Les pratiques apprises ont été :

- préférer les recherches ciblées ;
- lire une portion de fichier plutôt que le fichier entier ;
- ne pas relire les fichiers inchangés ;
- ne pas relancer une validation identique ;
- exécuter des contrôles étroits après une modification ;
- éviter les dumps intermédiaires verbeux ;
- utiliser un contrôle local lorsqu'il suffit ;
- réserver les audits plus larges aux risques démontrés.

La minimisation des tokens n'est pas seulement une réduction de coût. Un
contexte plus court, mais mieux sélectionné, réduit les ambiguïtés et rend les
contraintes importantes plus visibles.

> **Moins de contexte, mieux sélectionné, peut être supérieur à davantage de contexte.**

## 7. Le contrôle du périmètre

Les consignes ont progressivement distingué les types de tâches :

- recherche ;
- modification de code ou de données ;
- validation ;
- présentation ;
- documentation uniquement.

Elles précisent également :

- l'espace de travail autorisé ;
- les fichiers qui peuvent être modifiés ;
- les fichiers qui doivent rester intacts ;
- si une recherche externe est nécessaire ou interdite ;
- quelles valeurs sont gelées ;
- quand il faut s'arrêter.

Dans la phase de documentation publique, par exemple, les valeurs V8 et le
benchmark institutionnel étaient explicitement intouchables, V7/V3 devaient
rester historiques, et l'Index ne devait pas être recréé. Ces frontières
réduisent les régressions accidentelles et empêchent qu'une tâche de
présentation devienne une recalibration implicite.

## 8. Le plus petit changement sûr

La règle de modification est :

> **Make the smallest safe change that resolves the demonstrated issue.**

Elle limite les régressions, facilite la revue, protège les résultats déjà
validés et évite les refactorisations spéculatives. Dans les passes de
recalibration, les changements ont été limités aux points dont une revue
temporelle ou cross-variable démontrait le problème. Le reste de la trajectoire
était conservé.

La même règle s'applique à la documentation : remplacer un placeholder par un
document fondé sur les artefacts existants, sans réécrire les données ni
réinventer l'histoire du projet.

## 9. L'état gelé

Une couche qui a passé sa validation devient autoritative et n'est rouverte que
par une revue explicite. Les exemples comprennent :

- la couche de probabilités de crise ;
- l'architecture des scénarios ;
- les points de prévision finaux ;
- la décision de ne pas utiliser l'Index ;
- la méthodologie du benchmark institutionnel.

Le gel protège contre le comportement de « moving target » : une décision déjà
validée ne doit pas être remise en question simplement parce qu'une nouvelle
session préfère une autre formulation.

> **Un projet long devient beaucoup plus fiable quand le modèle sait non seulement ce qu'il doit faire, mais aussi ce qu'il n'a plus le droit de remettre en question.**

Le gel n'est pas une interdiction absolue de réviser. C'est une exigence de
réouvrir explicitement la question, de justifier la nouvelle revue et de
revalider les conséquences.

## 10. Les handoffs structurés

Chaque étape importante s'est terminée par des champs structurés, notamment :

- `PROJECT_VERSION` ;
- `VALUES_CHANGED` ;
- `FILES_UPDATED` ;
- `FILES_CREATED` ;
- `VALIDATION` ;
- `VERDICT` ;
- `NEXT_ACTION`.

Un handoff utile sépare les faits vérifiés des commentaires et indique ce que
l'étape suivante peut réellement supposer. Il permet à un autre modèle ou à une
autre session de continuer sans reconstruire tout le raisonnement.

Exemple générique :

```text
PROJECT_VERSION: V8.11c
VALUES_CHANGED: none
FILES_CREATED: data/final/...
VALIDATION: forecast values and links passed
VERDICT: ready for documentation
NEXT_ACTION: write recruiter-facing project evolution
```

Cette structure réduit l'ambiguïté, facilite le débogage et transforme la
continuité du projet en artefact vérifiable plutôt qu'en mémoire implicite du
modèle.

## 11. Les conditions d'arrêt

Les conditions d'arrêt sont devenues une partie explicite de la spécification :

- arrêter lorsque le résultat demandé passe la validation ;
- ne pas ajouter d'audit sans risque identifié ;
- ne pas faire de nettoyage annexe ;
- ne pas lancer de refactorisation « tant qu'on y est » ;
- ne pas rouvrir une décision gelée ;
- signaler une insuffisance de preuve plutôt que prolonger artificiellement la
  recherche.

> **Les conditions d'arrêt font partie de la spécification, pas d'un ajout a posteriori.**

Un agent fiable ne se définit pas seulement par la qualité de ce qu'il produit,
mais aussi par sa capacité à reconnaître que le résultat est suffisant.

## 12. Évaluer avant d'accepter

Le workflow est passé d'une logique de génération d'abord à une logique
d'évaluation avant acceptation. La question n'était plus seulement :

> « Le modèle peut-il produire une prévision ? »

Mais :

- est-elle cohérente avec elle-même ?
- respecte-t-elle la temporalité ?
- correspond-elle à la définition de la source ?
- contredit-elle une autre cible ?
- une autre revue identifie-t-elle un problème réel ?
- la révision améliore-t-elle effectivement le système ?

Les sorties n'étaient gelées qu'après des contrôles explicites. Cela a conduit à
revoir certains points de chômage 2030 lorsque leur relation avec l'ancrage
observé et les phases du PIB et du niveau de vie n'était pas satisfaisante.

## 13. Évaluations temporelles et cross-variable

Les évaluations principales comprenaient :

### Cohérence temporelle

- 2025→2030 ;
- 2030→2040 ;
- 2040→2050 ;
- comparaison des pentes annualisées.

### Cohérence entre variables

- chômage ↔ PIB réel par habitant ;
- chômage ↔ niveau de vie médian ;
- PIB réel par habitant ↔ niveau de vie médian.

### Ordre des scénarios

Les trajectoires devaient conserver l'ordre intentionnel entre dégradation
faible, centrale et forte, sans transformer « least-bad » en scénario de
prospérité.

### Relations et ratios

Le ratio niveau de vie médian / PIB par habitant, les écarts de chômage et les
phases de détérioration ont été examinés pour éviter une protection implicite
non soutenable ou une accélération sans mécanisme.

Cela constitue aussi un problème d'ingénierie LLM : le système doit évaluer des
relations, pas seulement générer des nombres qui ont chacun une apparence
plausible.

## 14. L'orchestration multi-modèles

Des modèles externes ont été utilisés comme :

- critiques ;
- relecteurs indépendants ;
- vérificateurs de plausibilité ;
- évaluateurs adversariaux.

Ils n'ont pas été utilisés comme un système de vote. Le workflow était :

```text
Résultat candidat
        ↓
Critique par un autre modèle
        ↓
Conversion de la critique en hypothèse explicite
        ↓
Reproduction du problème
        ↓
Test contre les données et la méthodologie
        ↓
Révision seulement si le problème est démontré
```

> **Le désaccord entre modèles n'était utile qu'après avoir été transformé en test.**

Cette approche évite de remplacer le jugement humain par une majorité de
réponses. Elle exploite plutôt la diversité des angles pour améliorer la
couverture des tests.

## 15. Le raisonnement fondé sur les sources

Les LLM peuvent produire des affirmations institutionnelles plausibles mais
non soutenues. Des règles de provenance ont donc été introduites :

- privilégier les sources primaires ou institutionnelles ;
- rattacher chaque valeur affichée à une source ;
- conserver la date de publication ;
- préciser la définition de la variable ;
- indiquer le type de prévision ;
- conserver l'horizon ;
- documenter la justification et la confiance.

La taxonomie utilisée distingue :

- `OBSERVED` ;
- `DIRECT_FORECAST` ;
- `LONG_RUN_PROJECTION` ;
- `STRUCTURAL_ASSUMPTION` ;
- `DERIVED_PROXY`.

> **Une bonne réponse n'est pas seulement correcte en apparence : elle doit être traçable.**

## 16. Le context engineering orienté provenance

La qualité du contexte inclut donc :

- l'autorité de la source ;
- la date et la vintage ;
- la définition exacte ;
- l'historique des transformations ;
- l'horizon ;
- la comparabilité ;
- le niveau de confiance.

L'exemple du PIB réel par habitant de la Commission européenne résume cette
leçon. Des jalons de croissance ont été utilisés pour dériver un niveau. Le
calcul était arithmétiquement correct, mais l'interprétation ne respectait pas
la sémantique de la source. Le niveau dérivé a été supprimé ; les jalons restent
des références de croissance.

> **La qualité du contexte n'est pas seulement une question de sélection de tokens : c'est aussi un contrôle de provenance.**

## 17. Préférer `NA` à la fausse précision

La règle de décision est simple : lorsqu'une valeur institutionnelle de long
terme directement comparable n'existe pas, utiliser `NA`.

Cette règle s'applique notamment :

- au benchmark institutionnel de niveau de vie médian réel après 2025 ;
- aux niveaux institutionnels de PIB par habitant qui ne peuvent pas être
  justifiés à partir de simples jalons de croissance.

Ce choix réduit la précision hallucinée, améliore la confiance et montre qu'un
workflow fiable sait préserver une absence de connaissance.

## 18. Une architecture human-in-the-loop

Les LLM ont accéléré :

- la recherche ;
- la génération de code ;
- la critique ;
- la synthèse ;
- la documentation ;
- l'analyse de candidats.

L'humain a conservé la responsabilité de :

- définir l'objectif ;
- décider l'architecture ;
- établir les critères d'acceptation ;
- juger la confiance dans une source ;
- interpréter le sens d'un scénario ;
- décider si une critique est pertinente ;
- choisir quand simplifier ;
- décider ce qui doit être gelé ;
- déterminer quand le résultat est terminé.

> **Le workflow est devenu dirigé par l'humain et accéléré par la machine, non autonome du modèle.**

Cette séparation est centrale pour un système fiable : l'agent peut proposer,
chercher, coder et critiquer, mais il ne décide pas seul de ce qui devient la
réalité officielle du projet.

## 19. L'évolution des règles en pratique

| Problème observé | Règle ajoutée | Effet recherché |
|---|---|---|
| Échec répété d'un outil | Anti-loop | Forcer un changement de stratégie |
| Recherche sans fin | Exploration bornée | Réduire la latence et le bruit |
| Dérive de périmètre | Scope explicite | Protéger l'objectif réel |
| Relectures et tokens gaspillés | Lectures ciblées | Garder le contexte pertinent |
| Régression après validation | État gelé | Protéger les décisions autoritatives |
| Surédition | Plus petit changement sûr | Limiter les effets de bord |
| Discontinuité entre sessions | Handoff structuré | Préserver l'état du projet |
| Valeur institutionnelle non soutenue | Gate de provenance | Empêcher la fausse précision |
| Amélioration sans fin | Stop condition | Reconnaître qu'une tâche est terminée |

## 20. Avant / après du workflow LLM

| Dimension | Workflow initial | Workflow mature |
|---|---|---|
| Prompting | Objectif large | Contrat d'exécution borné |
| Contexte | Large et implicite | Sélectionné et autoritatif |
| Exploration | Ouverte | Bornée |
| Outils | Opportunistes | Directement liés à l'objectif |
| État | Principalement conversationnel | Fichiers gelés et manifests |
| Validation | Après production | Gates explicites avant acceptation |
| Multi-modèles | Occasionnel | Revue adversariale |
| Sources | Récupération de contenu | Provenance contrôlée |
| Arrêt | Implicite | Condition explicite |
| Rôle humain | Correction des sorties | Architecture du workflow |

## 21. Ce que j'ai appris

- **Capacité ≠ fiabilité.** Un modèle brillant localement peut dériver sur un
  projet long.
- **Plus de raisonnement ≠ meilleure exécution.** Une réflexion prolongée sans
  décision ou test supplémentaire est une boucle.
- **Plus de contexte ≠ meilleur contexte.** La sélection et la hiérarchie
  comptent davantage que le volume.
- **L'évaluation compte souvent davantage que la génération.** Une sortie est
  un candidat tant qu'elle n'est pas vérifiée.
- **Les stop conditions font partie du prompt design.** Elles définissent le
  comportement attendu après la résolution.
- **L'état gelé est critique.** Il transforme une décision validée en repère
  stable.
- **La revue multi-modèles est plus utile comme test adversarial que comme
  vote.**
- **La provenance compte autant que le contenu.** Une valeur sans définition ni
  horizon peut être trompeuse.
- **La simplicité peut améliorer la correction.** Réduire les sorties a renforcé
  l'auditabilité de FranceScope.
- **Le jugement humain reste architectural.** Le modèle accélère le système
  sans en devenir l'autorité finale.

## 22. Ce que cela démontre pour l'ingénierie LLM

FranceScope fournit une expérience pratique de :

- prompt engineering ;
- context engineering ;
- contraintes d'agents ;
- gestion d'état sur un horizon long ;
- design d'évaluation ;
- orchestration multi-modèles ;
- discipline d'utilisation des outils ;
- réflexion sur l'efficacité des tokens ;
- contrôle de provenance ;
- reproductibilité ;
- systèmes human-in-the-loop.

Ces compétences ne sont pas présentées comme des mots-clés isolés. Elles sont
incarnées par des règles, des artefacts, des validations et des décisions de
périmètre. La valeur du projet réside dans la capacité à faire fonctionner un
workflow complexe de manière contrôlée, puis à simplifier l'architecture
lorsque les preuves ne justifient pas sa complexité.

## 23. Limites

Ce projet n'est pas une plateforme de production d'agents autonomes. Une grande
partie des contrôles a été mise en œuvre par des instructions disciplinées, des
fichiers d'état, des manifests et des validations ciblées, plutôt que par un
framework d'orchestration dédié.

Certaines règles restent donc procédurales : elles dépendent de leur
application correcte par l'agent et par l'humain. Elles pourraient être
renforcées dans un système logiciel avec permissions, journalisation, budget
d'actions et gates automatiques.

Enfin, la prévision de long terme reste intrinsèquement incertaine. La
discipline du workflow réduit les erreurs évitables ; elle ne transforme pas
des scénarios conditionnels en certitudes.

## 24. Documentation connexe

- [README recruteur](../README.md) ;
- [évolution du projet](project_evolution.md) ;
- [cadre d'évaluation](evaluation_framework.md) — documentation en cours ;
- [méthodologie du benchmark institutionnel](institutional_benchmark_methodology.md) ;
- [échecs et leçons](failures_and_lessons.md) — documentation en cours ;
- [rapport technique](technical_report.md) — documentation en cours ;
- [état final du projet](FINAL_PROJECT_STATE.md).

