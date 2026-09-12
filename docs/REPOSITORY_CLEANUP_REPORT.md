# Repository cleanup report

## Original major folders

The project contains `src/`, `scripts/`, `data/`, `docs/`, frontend assets,
versioned V3/V4/V7/V8 research and report outputs, and local development
environments. The `.venv/`, frontend dependency, cache, and build directories
are local/generated material rather than public project content.

## New public-facing structure

Clean copies now live in `data/final/`, `data/institutional/`, and
`outputs/{forecasts,comparisons,charts}/`. `archive/historical_versions/` and
`reports/` establish the historical and report-package boundaries.

## Files copied

- Final three-target forecasts, historical targets, and scenario definitions.
- Current forecast tables, institutional comparison tables, and final charts.
- Institutional source registry, explanations, near-term consensus, long-run
  reference, and FranceScope comparison explanation.

## Files moved

None. Versioned source paths were retained because scripts depend on them.

## Files archived

No existing files were moved. `archive/historical_versions/README.md` documents
the archival boundary and the status of V3/V7/Index artifacts.

## Files deleted

None. No deletion was necessary to create the public layer safely.

## Files intentionally left unchanged

Authoritative V8 research/report files, V7/V3 historical artifacts, raw source
data, scripts, and the existing README were left unchanged.

## Possible remaining cleanup issues

- The repository still contains large local development directories and a long
  historical script/data inventory.
- Existing versioned paths are not yet physically relocated.
- `requirements.txt` and `LICENSE` were not present at the project root during
  this pass.

## Secrets, local paths, and sensitive-data scan

The public-facing files created in this pass contain no credentials or local
absolute paths. The repository contains local development artifacts (including
`.env.local`, caches, `.venv/`, and dependency directories) that should remain
unpublished and are covered where practical by `.gitignore`. No personal
credentials were printed or copied.

## Final validation

The copied final forecast layer was checked against the authoritative V8
source: 2025 unemployment 7.725%, GDP per capita 38360, median living
25952.514017; and all requested low, central, and high 2030/2040/2050 values
match exactly. Institutional NA values and classifications are preserved.

## Verdict

REPOSITORY_READY_FOR_README

## Next action

Write the recruiter-facing README using the cleaned public structure.
