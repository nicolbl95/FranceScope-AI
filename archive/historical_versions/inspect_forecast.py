import pandas as pd, numpy as np
cols = ['year','simulation_id','inflation','food_inflation','energy_inflation','france_trade_balance',
          'france_real_exports','france_real_imports','real_gdp','public_debt_gdp',
          'public_deficit_gdp','public_interest_expenditure_gdp','public_expenditure_gdp',
          'mortgage_new_business_rate','corporate_credit_rate','ecb_policy_rate',
          'france_10y_government_rate','housing_cost_burden','compensation_per_employee']
df = pd.read_parquet('data/audits/economic_system/p0_raw_projections_2026_2050.parquet', columns=cols)
# deduplicate columns (there are two 'year' columns)
df = df.loc[:,~df.columns.duplicated()]
print('shape:', df.shape, 'columns:', list(df.columns))
print('years:', sorted(pd.unique(df['year'])))
for v in cols[2:]:
    s = df[df['year'].isin([2026,2027,2028,2029,2030,2035,2040,2045,2050])].groupby('year')[v].median()
    print(f'{v}:')
    print(s.round(4).to_string())
    print()
