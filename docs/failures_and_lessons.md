# Echecs utiles et lecons

Ce document conserve uniquement les echecs qui ont change l'architecture, la
methode ou le workflow. Chaque cas suit la structure :

**Probleme -> Diagnostic -> Decision -> Lecon**

Pour les regles operationnelles stabilisees, voir
[reliable_llm_workflows.md](reliable_llm_workflows.md). Pour les gates
d'acceptation, voir [evaluation_framework.md](evaluation_framework.md). Pour les
erreurs de benchmark institutionnel, voir
[institutional_benchmark_methodology.md](institutional_benchmark_methodology.md).

## 1. Complexite causale excessive

**Probleme**  
Les premieres versions multipliaient les variables intermediaires et les liens
causaux.

**Diagnostic**  
La surface numerique devenait plus difficile a defendre que le raisonnement
qu'elle etait censee clarifier.

**Decision**  
Reduire la sortie finale a trois cibles et garder le reste comme structure
explicative.

**Lecon**  
La complexite du modele n'est pas un substitut a la credibilite.

## 2. Sorties localement plausibles mais globalement incoherentes

**Probleme**  
Chaque variable pouvait sembler plausible prise isolement, tout en contredisant
les autres par ses pentes, ses ratios ou son timing.

**Diagnostic**  
La validation univariee etait insuffisante.

**Decision**  
Introduire des revues temporelles et cross-variable avant acceptation.

**Lecon**  
Une bonne valeur locale peut rester un mauvais scenario global.

## 3. Derive de modele et perte d'etat

**Probleme**  
Des decisions deja validees redevenaient "ouvertes" selon la session ou le
modele actif.

**Diagnostic**  
La memoire conversationnelle seule ne protege pas un projet long.

**Decision**  
Externaliser l'etat : fichiers autoritatifs, decisions gelees, manifests et
handoffs structures.

**Lecon**  
Un projet long a besoin d'un etat explicite, pas d'une conversation plus longue.

## 4. Boucles d'outils et repetition d'approches echouees

**Probleme**  
Le systeme pouvait relancer presque la meme commande, recherche ou hypothese
apres un echec.

**Diagnostic**  
Sans contrainte explicite, l'agent peut confondre activite et progres.

**Decision**  
Appliquer deux regles : ne jamais repeter le meme appel echoue ; changer de
strategie apres deux echecs sans progres mesurable.

**Lecon**  
L'echec doit declencher une bifurcation, pas une repetition.

## 5. Exploration trop large et lectures inutiles

**Probleme**  
Plus de recherche semblait utile meme quand les elements decisifs etaient deja
trouves.

**Diagnostic**  
L'absence de stop condition faisait deriver cout, latence et qualite.

**Decision**  
Imposer exploration bornee, lectures ciblees et preuve suffisante definie a
l'avance.

**Lecon**  
Plus de raisonnement n'aide que s'il reduit l'incertitude pertinente.

## 6. Suredition apres resolution

**Probleme**  
Une fois le probleme resolu, l'agent continuait parfois a modifier, reformuler
ou "ameliorer" des zones deja validees.

**Diagnostic**  
Apres le succes, le risque principal devient la regression.

**Decision**  
Appliquer la regle du plus petit changement sur et arreter apres validation
etroite.

**Lecon**  
Savoir s'arreter fait partie de l'ingenierie.

## 7. Mismatch source / definition

**Probleme**  
Des valeurs comparables en apparence ne decrivaient pas le meme concept :
population, unite, frequence, reel/nominal, agrege/par habitant.

**Diagnostic**  
La precision visuelle masquait une incompatibilite semantique.

**Decision**  
Rendre obligatoires les controles de definition et de statut avant toute
comparaison.

**Lecon**  
Une source fiable peut etre mal utilisee si sa definition est mal alignee.

## 8. Mauvais usage des horizons

**Probleme**  
Des forecasts de court terme, jalons de croissance et projections structurelles
pouvaient etre traites comme s'ils avaient le meme statut.

**Diagnostic**  
L'erreur d'horizon est parfois plus grave qu'une erreur de calcul.

**Decision**  
Separer explicitement prevision directe, projection long terme, reference
structurelle et `NA`.

**Lecon**  
Un horizon non supporte doit bloquer la valeur, pas etre "complete".

## 9. Transformations mathematiquement valides mais methodologiquement fausses

**Probleme**  
Des jalons de croissance GDPpc de long terme ont servi a deriver une trajectoire
de niveaux en euros/personne.

**Diagnostic**  
Le calcul etait propre ; l'interpretation ne l'etait pas.

**Decision**  
Supprimer le niveau derive, conserver les jalons comme reference structurelle et
laisser le benchmark de niveau a `NA`.

**Lecon**  
L'arithmetique ne suffit pas ; le sens methodologique prime.

## 10. Fausse precision

**Probleme**  
Lorsqu'une source manquait, la tentation etait forte de produire un proxy precis.

**Diagnostic**  
La precision ajoutee n'etait pas soutenue par la preuve disponible.

**Decision**  
Preferer `NA` ou un proxy explicitement separe du benchmark principal.

**Lecon**  
Une donnee manquante est parfois plus honnete qu'un chiffre elegant.

## 11. Redondance de l'Index composite

**Probleme**  
Apres reduction a trois cibles finales, l'Index composite n'apportait plus assez
d'information independante.

**Diagnostic**  
Il ajoutait surtout une couche normative de ponderation et d'abstraction.

**Decision**  
Supprimer l'Index du framework final.

**Lecon**  
Une abstraction doit disparaitre lorsqu'elle ne cree plus de valeur nette.

## 12. Le prompt seul ne controlait pas le systeme

**Probleme**  
Un meilleur prompt ne resolvait ni la perte d'etat, ni la derive de scope, ni
les erreurs de provenance.

**Diagnostic**  
Le projet avait besoin d'un systeme d'execution, pas seulement d'une meilleure
formulation.

**Decision**  
Passer au context engineering : scope, fichiers autoritatifs, etat gele, regles
anti-loop, validation et handoffs.

**Lecon**  
Le prompt est un composant ; le workflow est le systeme.

## 13. La confiance d'un seul modele etait insuffisante

**Probleme**  
Un modele pouvait produire une explication persuasive tout en manquant une vraie
incoherence.

**Diagnostic**  
La confiance interne d'un modele n'est pas une validation independante.

**Decision**  
Utiliser des critiques adversariales multi-modeles, puis convertir chaque
critique en test reproductible.

**Lecon**  
Le desaccord n'est utile que s'il devient testable.

## 14. Besoin d'un jugement architectural humain

**Probleme**  
Certaines decisions n'etaient ni purement statistiques ni purement textuelles :
geler une couche, accepter `NA`, supprimer un artefact devenu inutile.

**Diagnostic**  
Le systeme automatise produit des candidats et des tests, mais pas l'arbitrage
final de portee.

**Decision**  
Maintenir un human-in-the-loop sur les decisions de structure, de freeze et de
reouverture.

**Lecon**  
L'automatisation robuste ne remplace pas le jugement architectural ; elle le
rend plus cible.

## 15. Resume des changements durables

| Echec | Changement durable |
|---|---|
| Complexite excessive | Reduction a trois cibles finales |
| Coherence seulement locale | Revue temporelle et inter-variables |
| Derive / perte d'etat | Fichiers autoritatifs et handoffs |
| Boucles d'outils | Regles anti-loop explicites |
| Suredition | Plus petit changement sur + stop conditions |
| Mismatch definition / source | Controles de comparabilite obligatoires |
| Mauvais horizon | Taxonomie de statuts et integrite d'horizon |
| Fausse precision | Preference pour `NA` |
| Index redondant | Suppression de l'abstraction |
| Limites d'autonomie | Arbitrage humain architectural |
