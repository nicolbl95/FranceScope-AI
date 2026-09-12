# V8.02b Probability Consistency Reconciliation

## Contradictions found

The underlying `V8_crisis_probability_estimates.csv` had the two range tuples
reversed during generation: the first tuple was written as `probability_low`
and the second as `probability_high`, although the first was numerically larger
for each risk. This caused lower bounds to exceed upper bounds. The central
estimate was the midpoint and was therefore retained.

The previous prose summary also transcribed some ranges inconsistently
(notably global recession and banking/financial crisis). Those were summary
errors. The range inversion was an underlying-data error.

## Corrections

`V8_crisis_probability_estimates_final.csv` swaps the affected lower and upper
semantics, retains every central estimate, standardizes the exact probability
field names, and labels all values `JUDGMENT_SYNTHESIS`. Probabilities are
cumulative probabilities of at least one qualifying event within the horizon.
The original research artifact remains unchanged.

The sovereign concepts remain separate: material French sovereign/debt stress,
severe funding/refinancing crisis, and formal default/restructuring. These are
not collapsed into a single default probability.

Global recession means at least one qualifying global recession, not a French
recession, ordinary slowdown, or equity bear market. Banking crisis, asset-price
crash and credit crisis remain separate but correlated risks and must not be
treated as independent in V8.03.

## Final ranking

The authoritative ranking is in `V8_02b_top_25y_ranking.csv` and is calculated
directly from 25-year central estimates in the final table.

## Sovereign-default language

“France will default within 25 years” remains **NOT_SUPPORTED / TOO_STRONG**.
The defensible wording is that France faces material long-run sovereign funding
stress risk, while formal default or restructuring remains a low-probability
tail event.
