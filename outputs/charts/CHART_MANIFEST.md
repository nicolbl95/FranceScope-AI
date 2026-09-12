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
- Références institutionnelles : gris/bleu, pointillés et marqueurs distincts.
- L’ordre des scénarios reste faible, centrale, forte dans tous les graphiques.

## Graphiques finaux

| Fichier | Usage | Source de données | README | Documentation principale |
|---|---|---|:---:|:---:|
| `unemployment.png` | Trajectoire du chômage et divergence des scénarios | `data/final/final_three_target_forecasts.csv` | Non | Référence |
| `real_gdp_per_capita.png` | Trajectoire du PIB réel par habitant | `data/final/final_three_target_forecasts.csv` | Non | Référence |
| `real_median_living.png` | Trajectoire du niveau de vie médian réel | `data/final/final_three_target_forecasts.csv` | Non | Référence |
| `institutional_unemployment.png` | Comparaison FranceScope / références institutionnelles | `data/final/final_three_target_forecasts.csv`, `data/institutional/institutional_near_term_consensus.csv`, `data/institutional/institutional_long_run_reference.csv` | Non | Référence |
| `institutional_real_gdp_per_capita.png` | Scénarios FranceScope sans faux niveau institutionnel | `data/final/final_three_target_forecasts.csv`, `data/institutional/institutional_long_run_reference.csv` | Non | Référence |
| `institutional_real_median_living_standard.png` | Scénarios FranceScope et absence de benchmark officiel comparable | `data/final/final_three_target_forecasts.csv`, `data/institutional/institutional_long_run_reference.csv` | Non | Référence |
| `final_scenario_comparison.png` | Tableau de lecture rapide des résultats 2050 | `data/final/final_three_target_forecasts.csv` | Oui | Oui |
| `unemployment_2010_2050.png` | Historique disponible, scénarios et repères institutionnels du chômage | `data/final/final_historical_targets.csv`, `data/final/final_three_target_forecasts.csv`, `data/institutional/institutional_near_term_consensus.csv`, `data/institutional/institutional_long_run_reference.csv` | Non | Oui |
| `gdp_per_capita_2010_2050.png` | Historique disponible et scénarios du PIB réel par habitant | `data/final/final_historical_targets.csv`, `data/final/final_three_target_forecasts.csv` | Non | Oui |
| `median_living_2010_2050.png` | Historique disponible et scénarios du niveau de vie médian réel | `data/final/final_historical_targets.csv`, `data/final/final_three_target_forecasts.csv` | Non | Oui |
| `pessimistic_scenario_annotated.png` | Moteurs narratifs du scénario de forte détérioration | `data/final/final_three_target_forecasts.csv` | Non | Oui |
| `central_scenario_annotated.png` | Moteurs narratifs du scénario central | `data/final/final_three_target_forecasts.csv` | Non | Oui |

## Sélections par support

### README

Le README conserve uniquement `final_scenario_comparison.png` afin de rester
lisible et recruteur-friendly.

### Documentation principale

La documentation principale utilise `unemployment_2010_2050.png`,
`gdp_per_capita_2010_2050.png`, `median_living_2010_2050.png`,
`pessimistic_scenario_annotated.png`, `central_scenario_annotated.png` et
`institutional_unemployment.png`. Les séries institutionnelles absentes ne
sont pas fabriquées.

## Décisions et limites

- L’historique public de `final_historical_targets.csv` est affiché sous forme
  de points disponibles ; aucune continuité annuelle artificielle n’est
  dessinée entre deux observations espacées.
- Pas de niveau institutionnel GDPpc long terme directement comparable n’est dessiné jusqu’en 2050. Les jalons CE
  de croissance `0,4 %`, `1,4 %`, `1,4 %` sont rappelés comme information
  séparée, sans conversion implicite en euros.
- Pas de prévision institutionnelle de long terme directement comparable du
  niveau de vie médian n’est dessinée : le graphique affiche explicitement
  cette absence.
- Aucun intervalle probabiliste n’est affiché : les fourchettes approuvées ne
  constituent pas une incertitude statistique calibrée.
- Les fichiers temporaires de mise en page ne font pas partie du paquet public.

## Validation attendue

Après génération, vérifier que les PNG existent, que les valeurs des points
correspondent aux CSV publics, que les libellés sont français et qu’aucun
graphique d’Index composite ou de benchmark institutionnel fabriqué n’est
présenté comme résultat.
