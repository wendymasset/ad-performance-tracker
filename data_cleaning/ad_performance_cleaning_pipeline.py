import pandas as pd
import numpy as np
import os

# Load data
df = pd.read_csv("data_cleaning/marketing_campaign_raw.csv")

# Clean column names
df.columns = (
    df.columns.str.strip()
              .str.lower()
              .str.replace(' ', '_')
              .str.replace('-', '_')
)

# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Convert 'duration' column to numeric (days)
df['duration'] = df['duration'].str.replace(' days', '', regex=False).astype(int)

# Convert text columns to category
categorical_cols = [
    'company', 'campaign_type', 'target_audience', 'channel_used',
    'location', 'language', 'customer_segment'
]

for col in categorical_cols:
    df[col] = df[col].astype('category').str.strip()

# CLEAN 'acquisition_cost' before converting it
def clean_currency_column(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
              .str.replace(r"[\$,]", "", regex=True)
              .str.strip()
              .replace(r'^\s*$', np.nan, regex=True)
              .astype(float)
    )

df['acquisition_cost'] = clean_currency_column(df['acquisition_cost'])

# Now convert the rest to numeric
cols_to_convert = ['clicks', 'impressions', 'conversion_rate']  # acquisition_cost is already clean
for col in cols_to_convert:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Calculate KPIs
df['ctr'] = df['clicks'] / df['impressions']
df['cpc'] = df['acquisition_cost'] / df['clicks']
df['roas'] = (df['conversion_rate'] * df['impressions']) / df['acquisition_cost']


df.to_csv("marketing_campaign_cleaned.csv", index=False)


# Get the folder where the script is running
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create the full path for the CSV
output_path = os.path.join(script_dir, "marketing_campaign_cleaned.csv")

# Save the DataFrame
df.to_csv(output_path, index=False)

print(f"✅ File saved to: {output_path}")

