# Méthodologie du benchmark institutionnel

Ce document ne raconte pas le projet FranceScope. Il définit uniquement les
règles utilisées pour décider si une valeur institutionnelle peut entrer dans le
benchmark public, sous quel statut, et avec quel niveau de comparabilité.

Pour le récit général du projet, voir [la documentation principale](main_documentation.md).

## 1. Objet exact du benchmark

Le benchmark institutionnel sert à :

- documenter ce que les institutions publient réellement ;
- distinguer observation, prévision directe, projection structurelle et proxy ;
- empêcher les conversions qui créent une comparabilité artificielle ;
- conserver `NA` lorsque la preuve ne permet pas une valeur défendable.

Il ne sert pas à :

- produire un "quatrième scénario" FranceScope ;
- lisser des sources hétérogènes dans un faux consensus ;
- transformer une hypothèse de long terme en forecast officiel ;
- remplir les lacunes par interpolation ou capitalisation opportuniste.

## 2. Hiérarchie des sources

Ordre de préférence :

1. tableau ou base officielle téléchargeable ;
2. publication officielle primaire ;
3. page institutionnelle officielle ;
4. source secondaire uniquement pour orienter la recherche.

Règles :

- une source secondaire ne valide jamais seule une valeur finale ;
- Eurostat peut valider un ancrage observé, pas une prévision institutionnelle ;
- une source retenue doit permettre de retrouver la variable, l'horizon, l'unité
  et le statut méthodologique.

## 3. Statuts autorisés

| Statut | Usage autorisé | Non autorisé |
|---|---|---|
| `OBSERVED` | Ancrage historique mesuré | Le présenter comme une prévision |
| `DIRECT_FORECAST` | Valeur explicitement publiée pour une variable et un horizon donnés | La prolonger au-delà de l'horizon publié |
| `LONG_RUN_PROJECTION` | Référence structurelle de long terme sous hypothèses | La traiter comme un consensus court terme |
| `STRUCTURAL_REFERENCE` | Jalon, hypothèse ou indication structurelle utile mais non directement comparable | Le convertir automatiquement en niveau comparable |
| `DERIVED_INSTITUTIONAL_REFERENCE` | Transformation reproductible à partir de séries compatibles et documentées | La présenter comme une valeur directement publiée |
| `ILLUSTRATIVE_PROXY` | Approximation explicitement séparée du benchmark principal | L'appeler benchmark institutionnel |
| `NA` | Absence volontaire de valeur défendable | La remplacer par une estimation ad hoc |

## 4. Typologie des références

### Prévision directe

Une institution publie explicitement la valeur de la cible pour un horizon
donné. La valeur peut entrer comme `DIRECT_FORECAST` si la définition est
compatible.

### Projection de long terme

Une institution publie une trajectoire structurelle conditionnelle. Elle entre
comme `LONG_RUN_PROJECTION`, avec ses limites de définition, de population et
de statut conservées dans les métadonnées.

### Référence structurelle

La source informe le raisonnement mais ne fournit pas un niveau comparable
affichable. Exemple typique : jalons de croissance de long terme.

### Référence institutionnelle dérivée

Autorisée seulement si la transformation est :

- reproductible ;
- compatible en unité et en définition ;
- soutenue par des séries officielles suffisantes ;
- explicitement étiquetée comme dérivée.

### Proxy illustratif

Utile pour éclairer un ordre de grandeur, jamais pour remplacer une absence de
benchmark direct.

## 5. Exigences minimales de provenance

Chaque valeur retenue doit pouvoir être rattachée à :

- institution ;
- publication ou base ;
- date de publication / vintage ;
- nom exact de la variable ;
- année ou horizon ;
- unité ;
- définition ;
- statut (`OBSERVED`, `DIRECT_FORECAST`, etc.) ;
- URL ;
- note de comparabilité ou de transformation.

Principe : **pas de valeur orpheline**.

## 6. Contrôles de comparabilité

Avant de retenir une valeur, vérifier :

- **définition** : chômage total vs 20-64 ans, PIB total vs PIB par habitant,
  revenu médian vs revenu disponible d'un autre concept ;
- **unité** : pourcentage, euros, euros constants, PPA, personne, ménage,
  unité de consommation ;
- **temporalité** : annuel vs trimestriel, historique vs prospectif ;
- **horizon** : année exacte, point de projection, jalon, moyenne implicite ;
- **statut** : observation, forecast, hypothèse, projection structurelle.

Si un de ces points reste ambigu ou incompatible, la valeur reste `NA` ou est
rétrogradée en `STRUCTURAL_REFERENCE` / `ILLUSTRATIVE_PROXY`.

## 7. Intégrité d'horizon

Transformations interdites :

- prolonger une prévision 2026-2028 jusqu'en 2050 ;
- traiter un jalon comme une trajectoire annuelle complète ;
- convertir un taux de croissance en niveau sans support méthodologique
  suffisant ;
- fusionner court terme et long terme comme s'il s'agissait du même objet.

Le benchmark distingue donc :

1. **consensus court terme** si plusieurs valeurs comparables existent ;
2. **référence long terme** si une projection structurelle existe ;
3. **absence de valeur** sinon.

## 8. Règles de transformation

Une transformation n'est autorisée que si :

1. les séries sources sont officielles et identifiées ;
2. la définition cible reste compatible après transformation ;
3. l'horizon transformé est réellement soutenu par la source ;
4. les hypothèses ajoutées sont limitées, explicites et auditables.

Sinon :

- la transformation est refusée ;
- la valeur cible reste `NA` ;
- la source peut être conservée comme contexte ou `STRUCTURAL_REFERENCE`.

## 9. Pourquoi certaines valeurs restent `NA`

Une valeur reste `NA` lorsque :

- aucune source comparable n'existe ;
- la définition diffère trop fortement ;
- l'horizon publié ne couvre pas la cible ;
- la transformation nécessaire ajouterait une hypothèse non supportée ;
- le résultat donnerait une précision visuelle sans base méthodologique.

`NA` est ici une sortie de qualité, pas un manque de travail.

## 10. Cas d'échec méthodologiques à éviter

### 10.1 Conversion invalide de jalons de croissance en niveaux de long terme

Cas critique : des jalons de croissance du PIB réel par habitant de la
Commission européenne ont été interprétés comme base de capitalisation vers une
trajectoire de niveaux en euros/personne.

Pourquoi c'était invalide :

- la source fournissait des jalons de croissance structurelle, pas un niveau
  institutionnel directement publié ;
- la capitalisation introduisait des hypothèses intermédiaires non données ;
- le résultat devenait arithmétiquement propre mais méthodologiquement faux.

Règle permanente :

- conserver les jalons comme `STRUCTURAL_REFERENCE` ;
- ne pas en déduire un niveau institutionnel comparable ;
- laisser le benchmark long terme GDPpc à `NA` si aucun niveau robuste n'est
  publié.

### 10.2 Confusion entre PIB agrégé et PIB par habitant

Une prévision de croissance du PIB total ne valide pas un niveau de PIB réel par
habitant sans hypothèse de population compatible et documentée.

### 10.3 Substitution d'un proxy au benchmark officiel

Un proxy de niveau de vie médian peut être utile à titre illustratif ; il ne
devient jamais une valeur institutionnelle officielle tant que la source
directement comparable manque.

## 11. Règles d'acceptation du benchmark

Une valeur institutionnelle n'entre dans le benchmark que si :

- la source est retrouvable ;
- la classification est explicite ;
- la définition est compatible ou l'écart est documenté ;
- l'horizon est respecté ;
- la transformation, s'il y en a une, est défendable ;
- le statut visuel du résultat ne sur-vend pas la comparabilité.

Sinon, la bonne sortie est :

- `NA` ;
- ou une conservation comme référence structurelle séparée.

## 12. Artefacts publics à conserver

Le dossier [data/institutional/](../data/institutional/) contient les artefacts
de provenance utilisés par cette méthode, notamment le
[registre institutionnel](../data/institutional/institutional_source_registry.csv).

Ils documentent les sources, statuts, dates, URLs et notes de comparabilité ;
ils ne doivent pas être remplacés par un simple résumé narratif.
