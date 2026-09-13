# Workflow LLM fiable sur un projet long

Ce document décrit le systeme de controle operationnel utilise pour faire
travailler des LLM sur un projet long sans derive de scope, sans perte d'etat et
sans boucles inutiles.

Pour le recit complet du projet, voir [la documentation principale](main_documentation.md).
Pour les gates d'acceptation, voir [le cadre d'evaluation](evaluation_framework.md).

## 1. Principe directeur

Un modele peut etre intelligent localement et peu fiable sur plusieurs semaines.
Le probleme n'est donc pas seulement de "mieux prompter", mais de controler :

- ce que le modele sait ;
- ce qu'il peut modifier ;
- ce qu'il doit ignorer ;
- quand il doit s'arreter ;
- quelle preuve valide le resultat.

## 2. Le contexte comme contrat d'execution

Le contexte utile ne se limite pas au texte envoye au modele. Il inclut :

- l'objectif exact de la tache ;
- les fichiers autorises et interdits ;
- les valeurs ou decisions gelees ;
- les artefacts autoritatifs ;
- les validations attendues ;
- les conditions d'arret ;
- le format du handoff suivant.

Regle pratique : **un contexte plus precis vaut mieux qu'un contexte plus long**.

## 3. Fichiers autoritatifs et decisions gelees

Le workflow s'appuie sur un petit nombre d'artefacts stables :

- documentation principale ;
- fichiers finaux de valeurs ;
- registres de sources ;
- manifests de validation ;
- documents methodologiques acceptes.

Quand une decision est gelee :

- elle n'est pas rouverte implicitement ;
- une nouvelle session ne la traite pas comme une question encore ouverte ;
- toute reouverture exige une justification explicite et une revalidation.

## 4. Controle strict du perimetre

Chaque tache doit preciser :

- le resultat attendu ;
- l'espace de travail autorise ;
- les fichiers modifiables ;
- les fichiers intouchables ;
- le niveau d'exploration permis ;
- la validation minimale.

Regle centrale :

> **Every tool call must directly advance the requested task.**

Consequences :

- pas de nettoyage annexe ;
- pas de refactorisation opportuniste ;
- pas d'audit large sans question precise ;
- pas de modification hors perimetre "tant qu'on y est".

## 5. Exploration bornee et lectures ciblees

Avant une recherche ou une lecture, il faut savoir :

1. quelle question doit etre resolue ;
2. quels fichiers ou sources sont plausiblement necessaires ;
3. quelle preuve sera suffisante ;
4. quelle condition d'arret met fin a l'exploration.

Bonnes pratiques :

- lire la section utile, pas le depot entier ;
- eviter de relire un fichier inchange sans raison ;
- preferer une recherche ciblee a une exploration ouverte ;
- documenter `NA` ou "preuve insuffisante" quand la recherche n'aboutit pas.

## 6. Regles anti-loop

Deux garde-fous structurent l'execution :

> **Never repeat the exact same failed tool call.**

> **If an approach fails twice without measurable progress, change the hypothesis, tool, command, file, or implementation strategy.**

Effets attendus :

- transformer l'echec en signal ;
- forcer un changement de strategie ;
- limiter la consommation de temps et de tokens ;
- eviter les repetitions qui donnent une illusion de progres.

## 7. Discipline de tokens

La reduction de tokens n'est pas un objectif cosmetique ; elle ameliore aussi le
raisonnement. Le workflow evite :

- les relectures integrales inutiles ;
- les gros dumps intermediaires ;
- les validations identiques rejouees sans nouveau risque ;
- les longues reformulations qui ne changent aucune decision.

Preferer :

- sections ciblees ;
- controles etroits apres edition ;
- resumes d'etat structures ;
- artefacts de reference reutilisables.

## 8. Gestion d'etat et handoffs

La memoire conversationnelle ne suffit pas sur un projet long. L'etat doit etre
externalise via :

- fichiers autoritatifs ;
- versions ou phases ;
- decisions gelees ;
- manifests ;
- handoffs structures.

Format utile de handoff :

```text
PROJECT_VERSION:
VALUES_CHANGED:
FILES_UPDATED:
VALIDATION:
VERDICT:
NEXT_ACTION:
```

Objectif : permettre a un autre modele ou a une autre session de reprendre sans
reconstruire tout le contexte implicite.

## 9. Plus petit changement sur

Regle :

> **Make the smallest safe change that resolves the demonstrated issue.**

Application :

- modifier seulement les cellules, lignes ou paragraphes concernes ;
- preserver les zones deja validees ;
- eviter les reecritures larges sans benefice demontre ;
- revalider exactement ce qui a ete touche.

Cette regle s'applique autant au code qu'a la documentation ou aux donnees
methodologiques.

## 10. Validation apres modification

Une edition n'est pas terminee tant que la validation adaptee n'a pas ete
faite. Le controle doit etre :

- existant dans le depot ;
- le plus cible possible ;
- coherent avec le risque introduit.

Exemples :

- controle de liens apres edition de documentation ;
- validation d'une valeur ou d'une source apres mise a jour d'un benchmark ;
- revue ciblee d'une coherence temporelle apres ajustement de trajectoire.

## 11. Multi-modeles et revue adversariale

Un second modele n'est pas une autorite ; c'est un generateur d'hypotheses
adversariales.

Workflow :

```text
sortie candidate
-> critique independante
-> hypothese testable
-> reproduction / verification
-> revision seulement si le probleme est demontre
```

Cela evite :

- le vote informel entre modeles ;
- l'acceptation d'une critique non reproductible ;
- la confusion entre desaccord et preuve.

## 12. Human-in-the-loop

Le controle humain reste architectural. Il intervient pour :

- figer les decisions importantes ;
- arbitrer les cas methodologiquement ambigus ;
- decider qu'une preuve est insuffisante ;
- stopper une exploration devenue non rentable ;
- valider qu'une sortie est "assez bonne" pour devenir autoritative.

Le role du systeme n'est pas d'eliminer le jugement humain, mais de le
concentrer sur les decisions a forte portee.

## 13. Conditions d'arret

Un workflow fiable sait aussi s'arreter. Conditions typiques :

- le resultat demande est obtenu ;
- la validation ciblee est passee ;
- aucune decision gelee n'a ete rouverte ;
- aucun risque nouveau ne justifie une passe supplementaire ;
- l'exploration additionnelle n'augmentera plus la qualite de decision.

Il faut alors arreter, plutot que continuer a ameliorer marginalement un
resultat deja acceptable.

## 14. Checklist operationnelle

### Avant la tache

- definir l'objectif exact ;
- lister les fichiers autorises / interdits ;
- identifier les artefacts autoritatifs ;
- preciser la validation minimale ;
- rappeler les decisions gelees.

### Pendant la tache

- lire seulement ce qui repond a la question ;
- eviter les appels d'outils sans pouvoir de decision ;
- changer de strategie apres deux echecs sans progres ;
- maintenir un etat explicite des changements.

### Apres la tache

- valider de maniere ciblee ;
- enregistrer le handoff ;
- arreter une fois le resultat demontre ;
- ne pas rouvrir implicitement le perimetre.

## 15. Limites

Ce systeme reduit les erreurs evitables, mais ne supprime pas :

- l'incertitude du domaine ;
- les ambiguites de source ;
- la necessite d'un jugement humain ;
- le risque qu'un modele fort produise une erreur persuasive.

Pour les cas d'echec qui ont motive ces regles, voir
[echecs et lecons](failures_and_lessons.md).
