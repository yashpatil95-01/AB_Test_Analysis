import pandas as pd
from statsmodels.stats.proportion import proportions_ztest  # correct import

# Load dataset
csv_file = "data/ab_testing.csv"
df = pd.read_csv(csv_file)

df.info()
print("First 5 rows:")
print(df.head())

# Extract groups and convert "Yes"/"No" to 1/0
group_a = df[df['Group'] == 'A']['Conversion'].map({'Yes': 1, 'No': 0})
group_b = df[df['Group'] == 'B']['Conversion'].map({'Yes': 1, 'No': 0})

# Calculate conversion rates
conv_rate_a = group_a.mean()
conv_rate_b = group_b.mean()

print(f"Conversion rate A: {conv_rate_a:.4f}")
print(f"Conversion rate B: {conv_rate_b:.4f}")

count = [group_a.sum(), group_b.sum()]
nobs = [group_a.count(), group_b.count()]

# Perform z-test for proportions
stat, pval = proportions_ztest(count, nobs)

print(f"Z-statistic: {stat:.4f}")
print(f"P-value: {pval:.4f}")

alpha = 0.05
conclusion = "Reject null hypothesis - significant difference found." if pval < alpha else "Fail to reject null hypothesis - no significant difference."
print(conclusion)

# Save results
results = {
    'Group': ['A', 'B'],
    'Conversion Rate': [conv_rate_a, conv_rate_b],
    'Conversions': count,
    'Total Observations': nobs,
    'Z-statistic': [stat, ''],
    'P-value': [pval, ''],
    'Conclusion': [conclusion, '']
}

import os

output_dir = "results"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

results_df = pd.DataFrame(results)  
results_df.to_csv(os.path.join(output_dir, "ab_test_summary.csv"), index=False)
print("Results saved to ab_test_summary.csv")
