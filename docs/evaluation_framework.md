# Cadre d'evaluation de FranceScope

Ce document definit les gates utilises pour accepter, rejeter ou reviser une
sortie candidate. Il ne decrit ni le recit general du projet ni le workflow LLM
complet.

Pour les regles de controle operationnel, voir
[reliable_llm_workflows.md](reliable_llm_workflows.md). Pour la methode
institutionnelle, voir
[institutional_benchmark_methodology.md](institutional_benchmark_methodology.md).

## 1. Objet evalue

Le cadre s'applique a deux familles de sorties :

1. trajectoires et scenarios FranceScope ;
2. valeurs et interpretations institutionnelles destinees au benchmark public.

## 2. Pipeline d'acceptation

```text
Sortie candidate
-> integrite des donnees
-> compatibilite unites / definitions
-> ordre des scenarios
-> coherence temporelle
-> coherence inter-variables
-> plausibilite historique
-> tracabilite des sources
-> integrite d'horizon
-> revue adversariale
-> gate de revision
-> acceptation / rejet / revision / gel
```

Une sortie echoue des qu'un gate critique echoue ; elle n'est pas sauvee par sa
plausibilite sur un autre axe.

## 3. Controles obligatoires

| Gate | Question | Echec typique |
|---|---|---|
| Integrite des donnees | La valeur correspond-elle a la bonne variable, annee, scenario, unite et statut ? | Melange entre observation et forecast, pourcentage vs decimal |
| Definition / unite | Compare-t-on bien le meme concept ? | PIB total pris pour PIB par habitant, nominal pris pour reel |
| Ordre des scenarios | Les scenarios gardent-ils l'ordre voulu ? | Scenario optimiste plus mauvais que le central |
| Coherence temporelle | Les pentes et phases racontent-elles une histoire defendable ? | Degradation trop brutale ou rupture non expliquee |
| Coherence inter-variables | Les trois cibles racontent-elles la meme histoire macroeconomique ? | Niveau de vie trop protege malgre PIB et emploi degrades |
| Plausibilite historique | La combinaison se situe-t-elle dans une plage historiquement defendable ? | Trajectoire sans analogue credible ni mecanisme suffisant |
| Tracabilite | Chaque valeur affichee a-t-elle une source et un statut ? | Valeur orpheline |
| Integrite d'horizon | La source soutient-elle reellement l'horizon affiche ? | Forecast 2028 etendu a 2050 |

## 4. Integrite des donnees

Verifier systematiquement :

- nom de la variable ;
- annee ;
- scenario ;
- unite ;
- reel vs nominal ;
- pourcentage vs decimal ;
- observation vs prevision ;
- source, date et vintage ;
- compatibilite avec les valeurs gelees.

Une erreur de metadonnees invalide la sortie, meme si la courbe "a l'air"
coherente.

## 5. Compatibilite des definitions et des unites

Points de controle prioritaires :

- chomage total vs sous-population specifique ;
- PIB agrege vs PIB par habitant ;
- euros constants vs euros courants ;
- euros vs PPA ;
- revenu median vs autre concept de revenu ;
- annuel vs trimestriel ;
- point historique vs projection.

Si la compatibilite n'est pas defendable, la sortie doit etre revisee, reclassee
ou rejetee.

## 6. Ordre des scenarios

Ordre attendu :

- **chomage** : degradation faible < centrale < forte ;
- **PIB reel par habitant** : degradation faible > centrale > forte ;
- **niveau de vie median reel** : degradation faible > centrale > forte.

Ce gate est necessaire mais insuffisant : un bon ordre n'efface ni une mauvaise
definition ni une dynamique temporelle incoherente.

## 7. Coherence temporelle

L'analyse se fait par segments :

- 2025->2030 ;
- 2030->2040 ;
- 2040->2050.

Verifications :

- pente annualisee ;
- changement de regime ;
- presence ou absence de scarring ;
- compatibilite avec les points recents connus ;
- absence de rupture arbitraire entre segments.

Une correction n'est justifiee que par une incoherence demontree, pas par une
courbe simplement "plus jolie".

## 8. Coherence inter-variables

Le cadre ne force pas une equation unique ; il cherche des contradictions
substantielles entre :

- chomage et PIB reel par habitant ;
- chomage et niveau de vie median ;
- PIB reel par habitant et niveau de vie median.

Question centrale : **les trois series racontent-elles le meme scenario
macroeconomique ?**

## 9. Plausibilite historique

Les analogues historiques servent de contrainte, pas de copier-coller. Ils
permettent de tester si une combinaison de trajectoires :

- a deja existe dans un regime comparable ;
- exige un mecanisme exceptionnel explicite ;
- se situe hors de toute plage defendable.

Un analogue insuffisant n'invalide pas automatiquement la sortie ; il declenche
une revue plus exigeante.

## 10. Tracabilite et provenance

Chaque valeur institutionnelle affichee doit conserver, si disponible :

- institution ;
- publication ;
- date / vintage ;
- variable ;
- annee ;
- unite ;
- definition ;
- statut methodologique ;
- URL ;
- justification.

Principe : **pas de valeur orpheline**.

## 11. Integrite d'horizon

Interdictions explicites :

- extrapoler un forecast court terme vers un horizon non publie ;
- traiter un jalon comme une trajectoire complete ;
- convertir un taux de croissance en niveau comparable sans support suffisant ;
- presenter un proxy comme une prevision officielle.

Pour le detail des statuts autorises, voir
[institutional_benchmark_methodology.md](institutional_benchmark_methodology.md).

## 12. Logique de revision

Une valeur gelee ne change que si l'une des conditions suivantes est remplie :

- incoherence demontree ;
- preuve plus forte ;
- erreur de source ;
- erreur de definition ;
- erreur d'horizon.

Une critique isolee, un lissage plus elegant ou une preference de modele ne
suffisent pas.

## 13. Accept / reject / revise

Etats de sortie :

- **ACCEPT** : la sortie passe les gates applicables ;
- **REVISE** : probleme identifie et correction ciblee necessaire ;
- **REJECT** : la sortie repose sur une definition, une source ou un horizon
  non defendable ;
- **FREEZE** : etat accepte puis rendu autoritatif.

Principe de correction : **plus petite revision sure**.

## 14. Revue adversariale

Une revue par autre modele ou autre passe humaine suit la chaine :

```text
critique
-> hypothese explicite
-> reproduction
-> test contre donnees / definitions / methode
-> revision seulement si le probleme est confirme
```

Le desaccord n'est pas resolu par vote ; il doit devenir testable.

## 15. Criteres de gel final

Une sortie peut etre gelee lorsque :

- les valeurs sont sourcees ;
- les unites et definitions sont coherentes ;
- l'ordre des scenarios est valide ;
- les controles temporels passent ;
- les controles inter-variables passent ;
- l'horizon est respecte ;
- la critique adversariale a ete traitee ;
- aucune faiblesse bloquante ne subsiste ;
- l'arbitrage humain l'accepte.

## 16. Limites du cadre

Le cadre reduit les erreurs evitables, mais ne remplace ni :

- le jugement economique ;
- le jugement methodologique ;
- l'incertitude irreductible ;
- l'arbitrage humain sur les cas ambigus.

Il sert a rendre les decisions d'acceptation explicites, tracables et
repetables.
