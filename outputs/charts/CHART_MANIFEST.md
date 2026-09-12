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

| Fichier | Usage | Source de données | README | Brief recruteur | Rapport technique |
|---|---|---|:---:|:---:|:---:|
| `unemployment.png` | Trajectoire du chômage et divergence des scénarios | `data/final/final_three_target_forecasts.csv` | Oui | Oui | Oui |
| `real_gdp_per_capita.png` | Trajectoire du PIB réel par habitant | `data/final/final_three_target_forecasts.csv` | Oui | Oui | Oui |
| `real_median_living.png` | Trajectoire du niveau de vie médian réel | `data/final/final_three_target_forecasts.csv` | Oui | Oui | Oui |
| `institutional_unemployment.png` | Comparaison FranceScope / références institutionnelles | `data/final/final_three_target_forecasts.csv`, `data/institutional/institutional_near_term_consensus.csv`, `data/institutional/institutional_long_run_reference.csv` | Oui | Oui | Oui |
| `institutional_real_gdp_per_capita.png` | Scénarios FranceScope sans faux niveau institutionnel | `data/final/final_three_target_forecasts.csv`, `data/institutional/institutional_long_run_reference.csv` | Non | Oui | Oui |
| `institutional_real_median_living_standard.png` | Scénarios FranceScope et absence de benchmark officiel comparable | `data/final/final_three_target_forecasts.csv`, `data/institutional/institutional_long_run_reference.csv` | Non | Oui | Oui |
| `final_scenario_comparison.png` | Tableau de lecture rapide des résultats 2050 | `data/final/final_three_target_forecasts.csv` | Non | Oui | Oui |

## Sélections par support

### README

Les quatre graphiques conservés sont `unemployment.png`,
`real_gdp_per_capita.png`, `real_median_living.png` et
`institutional_unemployment.png`. Ils montrent respectivement les trois cibles
et la comparaison institutionnelle la plus défendable.

### Brief recruteur

La sélection recommandée est `final_scenario_comparison.png`,
`unemployment.png`, `institutional_unemployment.png`,
`real_gdp_per_capita.png` et `real_median_living.png`. Elle privilégie une
lecture rapide des résultats, sans recréer un indice composite.

### Rapport technique

Le rapport peut inclure les trois trajectoires, la comparaison institutionnelle
du chômage, les deux graphiques institutionnels avec leurs réserves et le
dashboard 2050. Les graphiques institutionnels GDPpc et niveau de vie ne sont
pas sélectionnés dans le README afin d’éviter de surcharger la page d’accueil.

## Décisions et limites

- Aucun graphique historique supplémentaire n’a été créé : le fichier
  `final_historical_targets.csv` ne fournit pas une série annuelle complète
  homogène pour les trois cibles ; relier artificiellement les points
  disponibles donnerait une continuité trompeuse.
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
