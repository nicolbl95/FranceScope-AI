# Manifeste des graphiques FranceScope V8

Ce manifeste décrit le paquet visuel public généré par
[`scripts/create_chart_package.py`](../../scripts/create_chart_package.py).
Les PNG sont dérivés uniquement des CSV publics autoritatifs ; aucune valeur
de scénario ou de benchmark n’est redéfinie dans le code.

## Système visuel

- Fond clair, grille discrète et palette commune.
- **Dégradation faible** : vert `#2A9D8F`.
- **Dégradation centrale** : ambre `#E9C46A`.
- **Dégradation forte** : corail `#E76F51`.
- Observation 2025 : marqueur et ligne neutres.
- Références institutionnelles : famille bleu pétrole, avec pointillés et
  marqueurs distincts selon le statut.
- L’ordre des scénarios reste faible, centrale, forte dans tous les graphiques.

## PRIMARY PUBLIC CHARTS

| Fichier | Usage | Source de données | README | Documentation principale |
|---|---|---|:---:|:---:|
| `unemployment_2010_2050.png` | Historique disponible, scénarios et repères institutionnels du chômage | `data/final/final_historical_targets.csv`, `data/final/final_three_target_forecasts.csv`, `data/institutional/institutional_near_term_consensus.csv`, `data/institutional/institutional_long_run_reference.csv` | Non | Oui |
| `gdp_per_capita_2010_2050.png` | Historique disponible et scénarios du PIB réel par habitant | `data/final/final_historical_targets.csv`, `data/final/final_three_target_forecasts.csv` | Non | Oui |
| `median_living_2010_2050.png` | Historique disponible et scénarios du niveau de vie médian réel | `data/final/final_historical_targets.csv`, `data/final/final_three_target_forecasts.csv` | Non | Oui |

## Sélections par support

### README

Le README conserve uniquement `unemployment_2010_2050.png` afin de rester
lisible et recruteur-friendly.

### Documentation principale

La documentation principale utilise uniquement les trois graphiques publics
principaux : `unemployment_2010_2050.png`, `gdp_per_capita_2010_2050.png` et
`median_living_2010_2050.png`.

## Décisions et limites

- L’historique public de `final_historical_targets.csv` est distingué des
  trajectoires scénarisées ; aucune année intermédiaire n’est inventée.
- Pas de niveau institutionnel GDPpc long terme directement comparable n’est dessiné jusqu’en 2050. Les jalons CE
  de croissance `0,4 %`, `1,4 %`, `1,4 %` sont rappelés comme information
  séparée, sans conversion implicite en euros.
- Pas de prévision institutionnelle de long terme directement comparable du
  niveau de vie médian n’est dessinée : le graphique affiche explicitement
  cette absence.
- Les moteurs de scénarios sont expliqués dans la documentation en texte, non
  par des graphiques autonomes.
- Aucun intervalle probabiliste n’est affiché : les fourchettes approuvées ne
  constituent pas une incertitude statistique calibrée.
- Les fichiers temporaires de mise en page ne font pas partie du paquet public.

## Validation attendue

Après génération, vérifier que les PNG existent, que les valeurs des points
correspondent aux CSV publics, que les libellés sont français et qu’aucun
graphique d’Index composite ou de benchmark institutionnel fabriqué n’est
présenté comme résultat.
