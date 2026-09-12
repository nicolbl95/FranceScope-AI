# FranceScope Economic Index v2

## Objective

FranceScope is now a focused economic index for France.

It is not intended to measure general happiness, health, crime,
social cohesion, or overall quality of life.

The index is designed to summarize the economic situation experienced
by people in France using a compact set of directly interpretable
economic indicators.

## Architecture

There are no block indices and no subindices.

Each core variable is normalized and contributes directly to the
FranceScope Economic Index using a variable-specific weight.

Weights will be determined only after:

1. all ten core variables have historical data;
2. annual historical series are aligned;
3. pairwise level and annual-change correlations are reviewed;
4. redundancy decisions are frozen;
5. normalization sensitivity is tested.

## Core variables

1. average_net_pension — higher is better
2. effective_retirement_age — lower is better
3. inflation — lower is better
4. social_benefits_to_tax_contributions_ratio — higher is better
5. real_gdp — higher is better
6. unemployment_rate — lower is better
7. temporary_contract_share — lower is better
8. median_living_standard_real — higher is better
9. poverty_rate — lower is better
10. housing_cost_burden — lower is better

## Auxiliary variables

Historical variables previously collected by FranceScope are preserved.

They may be used as:

- forecasting predictors;
- scenario drivers;
- causal/context variables;
- institutional validation inputs.

They do not receive a direct weight in the Economic Index unless they
are explicitly promoted into the core-variable configuration.

## Legacy Well-Being Index

The previous Well-Being Index architecture is retained only for
historical reference.

It is not the active FranceScope index architecture.
