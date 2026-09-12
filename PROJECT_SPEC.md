# FranceScope AI — Project Specification

## Objective

FranceScope AI is an agentic probabilistic forecasting and scenario-intelligence system
for studying the future evolution of living standards and well-being in France.

The final system will combine economic, fiscal, demographic, social, climate,
energy and geopolitical data with econometrics, machine learning, deep learning
and probabilistic simulations.

The LLM must never invent economic forecasts. Numerical outputs must come from
data, statistical models or executable tools.

## Geographic scope

France is the only country for which detailed outcomes are forecast.

External variables may represent:

- euro area
- European Union
- Germany
- United States
- United Kingdom
- Spain
- global economy
- world trade
- global energy markets
- climate
- geopolitical shocks

## Time horizon

- Historical index: approximately 2010 onward
- 2026–2035: probabilistic forecasting horizon
- 2036–2045: conditional scenario horizon

Three final scenarios:

1. Optimistic
2. Central
3. Pessimistic

## FranceScope Well-Being Index

Base-100 composite index describing French living standards and well-being.

Six dimensions:

1. Material living standards
2. Employment and economic security
3. Poverty and inequality
4. Health
5. Subjective well-being and social cohesion
6. Safety

Weights must be transparent and tested through sensitivity analysis.

## Structural blocks

### Block 1 — Demography, employment and human capital

Population structure, ageing, labour-force participation, unemployment,
underemployment, job quality, wages, education, skills and health.

### Block 2 — Production, technology, AI and productivity

GDP, investment, production, productivity, firm activity, R&D,
automation and AI adoption.

### Block 3 — Climate, energy and resources

Climate shocks, agriculture, water, energy, commodities, adaptation
and ecological transition.

### Block 4 — Trade, geopolitics and global environment

Exports, imports, external demand, supply chains, world growth,
protectionism, wars and geopolitical shocks.

### Block 5 — Public finance, taxation, inflation and financial conditions

Inflation, ECB policy, interest rates, credit, taxation, public revenue,
public expenditure, deficit, debt and financing conditions.

### Block 6 — Living standards, well-being and society

Disposable income, consumption, poverty, inequality, life satisfaction,
health, social cohesion and safety.

## Variable roles

### outcome

A variable we explicitly want to measure, explain or forecast.

### core_driver

A structurally important variable justified by economic mechanisms.
It is not automatically removed because a feature-selection algorithm gives it
low importance during one period.

### candidate_predictor

A possible predictor whose inclusion depends on data quality and demonstrated
out-of-sample predictive value.

## Variable-selection strategy

Expected long-term scale:

- 150–250 raw candidate series
- 35–45 structural core variables
- 15–40 features per target/model after selection
- 15–25 indicators maximum in the final Well-Being Index

Selection will later combine:

- economic reasoning
- causal graph structure
- data quality
- redundancy analysis
- walk-forward validation
- permutation importance
- SHAP
- stability across historical periods

## Future quantitative architecture

Planned model families:

- econometric baseline
- gradient-boosting model
- PyTorch temporal model
- probabilistic ensemble where justified
- Monte-Carlo scenario simulation

## Future agentic architecture

Four planned responsibilities:

1. Data & Evidence Agent
2. Scenario Planner Agent
3. Model & Simulation Agent
4. Audit & Explanation Agent

Three planned MCP servers:

1. Data MCP
2. Model MCP
3. Scenario MCP

These components are intentionally not implemented in the initial foundation.

## LLM responsibilities

Future LLM use will focus on:

- planning
- tool calling
- structured extraction
- metadata interpretation
- context engineering
- audit
- failure diagnosis
- grounded explanations

All economic calculations remain deterministic or model-driven.
