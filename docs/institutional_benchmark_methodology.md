# Méthodologie du benchmark institutionnel

Comparer FranceScope aux institutions n'était pas simplement une question
d'aligner des chiffres dans un tableau. Il fallait déterminer ce que chaque
institution publiait réellement, à quel horizon, avec quelle définition et
sous quel statut méthodologique.

> **Une prévision directe à deux ans, une projection structurelle à vingt-cinq ans et un scénario conditionnel ne sont pas des objets statistiques équivalents.**

La couche institutionnelle a été ajoutée pour rendre les divergences
interprétables sans transformer des références hétérogènes en un faux consensus.
Elle distingue les observations, les prévisions directes, les projections de
long terme, les hypothèses et les proxies dérivés.

## 1. Objectif de la couche institutionnelle

Le benchmark poursuit cinq objectifs :

1. fournir des points de référence externes ;
2. montrer où FranceScope diverge ;
3. comprendre pourquoi les institutions obtiennent des trajectoires
   différentes ;
4. empêcher une prévision auto-référentielle ;
5. rendre explicites l'incertitude et les données manquantes.

Cette couche n'est **pas un quatrième scénario FranceScope**. Les scénarios
FranceScope sont conditionnels et construits autour de trois cibles. La couche
institutionnelle répond à une autre question : quelles observations et quelles
projections officielles existent réellement, avec quelles limites de
comparabilité ?

## 2. Sources examinées et sources retenues

Les sources institutionnelles retenues dans le registre public comprennent :

- la Banque de France ;
- la Commission européenne, notamment l'*Autumn Economic Forecast* ;
- le rapport *Ageing Report* de la Commission européenne ;
- l'OCDE ;
- le FMI ;
- l'INSEE.

Eurostat apparaît également comme source statistique de plusieurs ancrages
observés, notamment pour le chômage harmonisé et le PIB par habitant. Il ne
faut toutefois pas confondre une série statistique observée avec une prévision
institutionnelle.

Une source peut être :

- examinée et retenue numériquement ;
- utilisée pour documenter une définition ou une méthode ;
- conservée comme contexte ;
- trouvée mais non retenue parce que l'horizon, la définition ou la
  comparabilité n'étaient pas suffisants.

Le registre distingue ce qui soutient une valeur affichée de ce qui a seulement
orienté la recherche. Il évite ainsi d'impliquer qu'une institution a contribué
numériquement à un agrégat lorsqu'elle n'a fourni qu'un contexte méthodologique.

## 3. Hiérarchie des sources

La hiérarchie préférée est :

1. source officielle primaire ;
2. jeu de données ou tableau téléchargeable officiel ;
3. publication officielle ;
4. communiqué ou page pays officielle ;
5. source secondaire uniquement pour naviguer, jamais comme preuve finale
   lorsqu'une source primaire est accessible.

Cette hiérarchie réduit la dérive de citation, les erreurs de transcription et
les ambiguïtés de définition. Elle améliore aussi la reproductibilité : un
relecteur doit pouvoir retrouver le document, la date, l'horizon et le concept
qui soutiennent une valeur.

## 4. Taxonomie des types de source

Chaque valeur conservée reçoit une classification :

| Classification | Définition | Exemple dans FranceScope | Ce que le label n'autorise pas |
|---|---|---|---|
| `OBSERVED` | Valeur historique mesurée ou ancrage statistique | Chômage 2025 à 7,725 % | La présenter comme une prévision |
| `DIRECT_FORECAST` | Prévision publiée explicitement pour une variable et un horizon | Chômage Banque de France 2026–2028 | La prolonger jusqu'en 2050 |
| `LONG_RUN_PROJECTION` | Trajectoire structurelle conditionnelle sous hypothèses | Chômage CE 2030–2050 | La traiter comme un consensus de court terme |
| `STRUCTURAL_REFERENCE` | Hypothèse ou jalon structurel publié, sans niveau comparable | Jalons CE de croissance GDPpc | Le convertir automatiquement en niveau |
| `DERIVED_INSTITUTIONAL_REFERENCE` | Transformation reproductible de séries institutionnelles compatibles | PIB réel / population, si les deux séries et conventions sont vérifiées | Le présenter comme une prévision officielle directe |
| `ILLUSTRATIVE_PROXY` | Approximation explicitement non équivalente à la cible | Proxy de niveau de vie, s'il est utilisé | Le présenter comme un benchmark institutionnel |
| `NA` | Valeur absente faute de comparabilité défendable | Niveau GDPpc 2050 ou médiane 2050, si non sourcés | Combler le manque par interpolation ou hypothèse |

Cette taxonomie protège la frontière entre ce qui est observé, ce qui est
publié comme prévision et ce qui relève d'une interprétation ou d'une
transformation.

## 5. Méthodologie du consensus de court terme

Le terme **consensus institutionnel** n'est utilisé que lorsque deux
observations institutionnelles au moins sont comparables pour la même variable,
la même année et une définition compatible.

Pour ces observations, la table conserve :

- le nombre d'institutions ;
- la médiane ;
- la moyenne ;
- le minimum ;
- le maximum ;
- l'écart-type.

La médiane est la statistique de présentation privilégiée : elle est robuste
aux valeurs extrêmes, adaptée à un petit nombre d'institutions et facile à
interpréter. Elle ne transforme pas pour autant des prévisions différentes en
une trajectoire unique.

### Exemples vérifiés

| Variable / année | Nombre | Médiane | Moyenne | Min–max | Écart-type |
|---|---:|---:|---:|---:|---:|
| Chômage 2026 | 2 | 8,2 % | 8,2 % | 8,1–8,3 % | 0,1 |
| Chômage 2027 | 2 | 8,4 % | 8,4 % | 8,1–8,7 % | 0,3 |
| Croissance du PIB réel 2026 | 4 | 0,85 % | 0,8 % | 0,5–1,0 % | 0,1871 |
| Croissance du PIB réel 2027 | 3 | 1,0 % | 1,0 % | 0,9–1,1 % | 0,0816 |

Les valeurs de croissance du PIB agrégé ne sont pas mélangées avec des valeurs
de PIB réel par habitant. Elles restent dans leur propre catégorie.

## 6. La référence institutionnelle de long terme

À long terme, il existe souvent une seule source utilisable, des définitions
hétérogènes et des hypothèses structurelles plutôt qu'une prévision directe
comparable. Le terme approprié est donc **référence institutionnelle de long
terme**, et non consensus.

L'exemple principal est le scénario structurel du rapport *Ageing Report* de la
Commission européenne pour le chômage des personnes âgées de 20 à 64 ans :

| Année | Référence chômage | Statut |
|---|---:|---|
| 2030 | 7,1 % | `LONG_RUN_PROJECTION` |
| 2040 | 6,7 % | `LONG_RUN_PROJECTION` |
| 2050 | 6,3 % | `LONG_RUN_PROJECTION` |

Cette référence est utile pour situer les scénarios FranceScope, mais elle ne
doit pas être présentée comme identique à la définition FranceScope ni comme
une prévision directe de court terme. Le périmètre d'âge, les hypothèses de
participation et le statut structurel sont conservés dans les métadonnées.

## 7. PIB agrégé contre PIB par habitant

La croissance du PIB réel agrégé n'est pas le PIB réel par habitant. Une
conversion nécessite au minimum une hypothèse de population compatible, ainsi
qu'une convention de prix et de période.

Il est donc interdit de :

- convertir silencieusement une prévision de PIB agrégé en niveau de PIB par
  habitant ;
- présenter une croissance comme un niveau ;
- mélanger une série en euros avec une série en parité de pouvoir d'achat ;
- traiter un proxy comme un forecast direct.

FranceScope conserve les références institutionnelles de croissance lorsqu'elles
sont pertinentes, mais n'invente pas un niveau institutionnel de PIB par
habitant pour 2050.

## 8. L'erreur des jalons de PIB par habitant de la Commission

Les données européennes de long terme comprenaient des jalons de croissance du
PIB par habitant. Une première interprétation les a utilisées trop agressivement
comme des taux constants afin de construire une trajectoire de niveau en euros.

L'opération de capitalisation était mathématiquement valide. La sémantique de la
source ne justifiait toutefois ni un taux constant entre les jalons, ni un
niveau institutionnel directement comparable. La trajectoire dérivée en
euros/personne a donc été supprimée. Les jalons de croissance restent conservés
comme références structurelles :

- 0,4 % annuel en 2030 ;
- 1,4 % annuel en 2040 ;
- 1,4 % annuel en 2050.

> **Une transformation correcte mathématiquement peut être incorrecte méthodologiquement.**

Cette expérience est devenue une règle permanente d'intégrité de l'horizon :
aucune transformation ne doit dépasser ce que la source permet réellement
d'affirmer.

## 9. Le benchmark du niveau de vie médian

La recherche n'a pas trouvé de prévision institutionnelle de long terme
directement comparable pour le niveau de vie médian réel français. Cette
absence est méthodologiquement importante :

- les revenus des ménages nécessitent des hypothèses de distribution ;
- les impôts et transferts évoluent selon des choix institutionnels ;
- le concept de revenu disponible médian n'est pas équivalent au PIB par
  habitant ;
- les publications de long terme donnent rarement une trajectoire complète de
  cette variable.

Le benchmark officiel conserve donc l'ancrage observé de 2025, puis `NA` après
2025. Un éventuel proxy illustratif doit rester séparé du benchmark principal,
être explicitement nommé comme dérivé et ne jamais être utilisé comme consensus.

> **`NA` est parfois une meilleure donnée qu'un chiffre artificiellement précis.**

## 10. Compatibilité des définitions

Chaque comparaison est soumise à des contrôles de compatibilité :

- périmètre d'âge du chômage ;
- fréquence annuelle ou trimestrielle ;
- valeur nominale ou réelle ;
- base de prix ;
- euros ou parité de pouvoir d'achat ;
- PIB total ou PIB par habitant ;
- définition du revenu médian ;
- unité ménage, personne ou unité de consommation ;
- statut historique ou prospectif.

Le chômage européen des 20–64 ans est un exemple de référence utile mais non
identique à toutes les définitions du chômage FranceScope. La différence est
documentée, pas effacée par une simple égalité de pourcentage.

## 11. Intégrité de l'horizon

Les règles d'horizon sont explicites :

- ne pas extrapoler une prévision 2028 jusqu'en 2050 ;
- ne pas prolonger les hypothèses de court terme ;
- ne pas traiter un jalon comme une moyenne de décennie ;
- ne pas transformer une hypothèse structurelle en forecast officiel ;
- ne pas fabriquer une trajectoire lorsque la source ne la fournit pas.

Ces règles protègent contre la fausse précision. Une institution peut publier
une prévision à deux ans et une projection démographique à trente ans ; ces
objets ne doivent pas être fusionnés sans signaler leur nature.

## 12. Provenance au niveau de la valeur

Le registre de sources et les fichiers d'explication structurent chaque valeur
retenue avec, lorsque disponible :

- institution ;
- publication ;
- date de publication ;
- vintage ;
- nom exact de la variable ;
- année ;
- valeur ;
- unité ;
- définition ;
- type de prévision ;
- URL ;
- tableau, section ou page ;
- justification ;
- confiance ;
- notes de comparabilité.

Cette approche applique le principe :

> **Pas de valeur orpheline.**

Une valeur affichée dans un tableau public doit pouvoir être reliée à une
source, une définition et un horizon. Les explications au niveau des valeurs
séparent ce qui est explicitement déclaré de ce qui relève de notre analyse.

## 13. Explication institutionnelle contre interprétation FranceScope

La méthodologie distingue deux champs :

### Explication déclarée par la source

Ce que l'institution indique explicitement sur ses hypothèses, sa définition ou
sa trajectoire.

### Interprétation FranceScope

Notre lecture des raisons pour lesquelles un scénario FranceScope diverge :
pression budgétaire, investissement, productivité, scarring ou récupération.

Si aucune explication explicite n'est retrouvée, le fichier doit le dire. Il est
interdit de reconstruire une justification plausible et de l'attribuer à
l'institution.

Cette séparation est essentielle pour la Banque de France et la Commission
européenne : leurs chiffres peuvent être comparés à FranceScope sans prétendre
que FranceScope connaît ou conteste toute leur logique interne.

## 14. Pourquoi FranceScope diffère

Les références institutionnelles donnent généralement davantage de poids à :

- des trajectoires démographiques standard ;
- des hypothèses de participation ;
- une convergence progressive de la productivité ;
- une normalisation graduelle ;
- un scarring permanent plus limité dans la référence centrale.

FranceScope donne davantage de poids, dans ses scénarios conditionnels, à :

- la pression budgétaire persistante ;
- la charge de la dette et des intérêts ;
- le sous-investissement et la faiblesse du capital productif ;
- la faiblesse de productivité ;
- la compétitivité et la désindustrialisation ;
- les contraintes politiques ;
- les crises répétées ;
- l'hystérèse du chômage ;
- le scarring cumulé ;
- une récupération plus faible.

FranceScope n'affirme pas que les institutions ont tort. Il explore une
question conditionnelle différente et rend les hypothèses divergentes
explicites.

## 15. Quatre produits de comparaison

Les sorties institutionnelles sont séparées en quatre produits :

1. **Actualité historique** : ancrage observé, par exemple 2025 ;
2. **Consensus institutionnel de court terme** : agrégat autorisé seulement
   lorsque plusieurs valeurs comparables existent ;
3. **Référence institutionnelle de long terme** : projection structurelle
   explicitement étiquetée ;
4. **Proxy dérivé illustratif** : transformation secondaire, exclue du benchmark
   principal.

Ces produits doivent rester distincts visuellement et sémantiquement. Les
regrouper dans une seule colonne « institutions » masquerait les différences de
statut et d'incertitude.

## 16. Politique de données manquantes

Si au moins une des conditions suivantes est satisfaite :

- aucune source comparable n'existe ;
- le décalage de définition est trop important ;
- l'horizon n'est pas soutenu ;
- la transformation n'est pas justifiée ;

alors le résultat est `NA`.

Cette politique s'applique notamment au niveau institutionnel de PIB par
habitant à long terme et au niveau de vie médian après 2025. `NA` est une
fonction de qualité : il évite de convertir une absence de preuve en certitude
visuelle.

## 17. Règles de validation

La couche institutionnelle est acceptée seulement si :

- chaque valeur possède une source ;
- la date de publication est présente ;
- la classification est présente ;
- l'horizon n'est pas extrapolé ;
- aucun niveau de PIB par habitant non soutenu n'est ajouté ;
- aucun forecast long terme du niveau de vie médian n'est inventé ;
- la référence chômage de la Commission est étiquetée
  `LONG_RUN_PROJECTION` ;
- les valeurs FranceScope restent inchangées ;
- l'Index n'est pas recréé.

Ces règles sont vérifiées avec les fichiers de registre, d'explication, de
consensus et de référence long terme.

## 18. Instantané actuel du benchmark

| Cible / année | Valeur institutionnelle | Statut |
|---|---:|---|
| Chômage 2026 | 8,2 % | Consensus court terme, 2 institutions |
| Chômage 2027 | 8,4 % | Consensus court terme, 2 institutions |
| Chômage 2028 | 7,8 % | Prévision directe Banque de France |
| Chômage 2030 | 7,1 % | Référence CE long terme, 20–64 ans |
| Chômage 2040 | 6,7 % | Référence CE long terme, 20–64 ans |
| Chômage 2050 | 6,3 % | Référence CE long terme, 20–64 ans |
| Croissance PIB réel agrégé 2026 | 0,85 % médiane | Consensus court terme, 4 institutions |
| Croissance PIB réel agrégé 2027 | 1,0 % médiane | Consensus court terme, 3 institutions |
| Niveau PIB réel par habitant long terme | `NA` | Aucun niveau institutionnel comparable |
| Niveau de vie médian réel long terme | `NA` | Aucun forecast institutionnel direct comparable |

Les valeurs de croissance du PIB dans ce tableau ne sont pas des niveaux de PIB
par habitant. Les valeurs FranceScope restent dans les fichiers finaux séparés.

## 19. Produits de données publics

Le dossier [`data/institutional/`](../data/institutional/) contient :

- `institutional_source_registry.csv` : institutions, publications, dates,
  types de source et URLs ;
- `institutional_forecast_explanations.csv` : valeurs au niveau cible avec
  classification, source et notes ;
- `institutional_near_term_consensus.csv` : agrégats autorisés de court terme ;
- `institutional_long_run_reference.csv` : observations, forecasts directs,
  projection CE et jalons de croissance ;
- `francescope_vs_institutions_explanation.csv` : explication synthétique des
  divergences par variable.

Ces fichiers sont des produits publics lisibles et auditables, pas un simple
export opaque d'une session de recherche.

## 20. Ce que cela démontre pour l'IA et la data engineering

La construction de cette couche démontre :

- une récupération orientée provenance ;
- un typage des sources ;
- un alignement des définitions ;
- une intégrité des horizons ;
- une gestion explicite de l'incertitude ;
- une politique de non-fausse-précision ;
- des métadonnées structurées ;
- des comparaisons reproductibles ;
- une prévention des hallucinations LLM par contrats d'évidence.

> **Le problème n'était pas seulement de trouver une source, mais de savoir si cette source pouvait réellement supporter la valeur que le modèle voulait utiliser.**

## 21. Limites

- La couverture institutionnelle est inégale.
- Les projections de long terme directement comparables sont rares.
- Les définitions diffèrent selon les institutions et les horizons.
- Certaines institutions fournissent une méthodologie sans trajectoire numérique
  récupérable.
- Les références institutionnelles sont conditionnelles, et non des certitudes.
- L'absence de données comparables empêche une comparaison institutionnelle
  complète des trois cibles en 2050.

Ces limites sont conservées dans le produit final au lieu d'être masquées par
des transformations supplémentaires.

## 22. Documentation connexe

- [README recruteur](../README.md) ;
- [évolution du projet](project_evolution.md) ;
- [workflow LLM fiable](reliable_llm_workflows.md) ;
- [cadre d'évaluation](evaluation_framework.md) ;
- [échecs et leçons](failures_and_lessons.md) — documentation en cours ;
- [rapport technique](technical_report.md) — documentation en cours ;
- [registre institutionnel](../data/institutional/institutional_source_registry.csv).
