import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# === 1. Load environment and connect to Supabase ===
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(url, key)

# === 2. Load main dataset ===
df = pd.read_csv("data_cleaning/marketing_campaign_cleaned.csv")

# === 3. Clean duration ===
df['duration'] = (
    df['duration']
    .astype(str)
    .str.extract(r'(\d+)')
    .astype(float)
    .fillna(0)
    .astype(int)
)

# === 4. Fetch dimension tables from Supabase ===
dim_campaign_type = pd.DataFrame(supabase.table("dim_campaign_type").select("*").execute().data)
dim_channel = pd.DataFrame(supabase.table("dim_channel").select("*").execute().data)
dim_location = pd.DataFrame(supabase.table("dim_location").select("*").execute().data)
dim_audience = pd.DataFrame(supabase.table("dim_audience").select("*").execute().data)

# === 5. Merge foreign keys ===
df = df.merge(dim_campaign_type, on="campaign_type", how="left")
df = df.merge(dim_channel, left_on="channel_used", right_on="channel_name", how="left")
df = df.merge(dim_location, left_on="location", right_on="city", how="left")
df = df.merge(dim_audience, on=["target_audience", "customer_segment"], how="left")

df = df.drop(columns=["channel_name", "city", "campaign_type", "channel_used", "location", "target_audience", "customer_segment"])

# === 6. Drop rows with missing foreign keys (optional but clean) ===
df = df.dropna(subset=[
    'campaign_type_id',
    'channel_id',
    'location_id',
    'audience_id'
])

# === 7. Drop duplicates (keep first occurrence of each campaign) ===
df = df.drop_duplicates(subset="campaign_id")

# === 8. Select fact table columns ===
fact_df = df[[
    'campaign_id',
    'campaign_type_id',
    'channel_id',
    'location_id',
    'audience_id',
    'duration',
    'impressions',
    'clicks',
    'acquisition_cost',
    'conversion_rate',
    'ctr',
    'cpc',
    'roas'
]]

# === 9. Export to CSV ===
fact_df.to_csv("fact_campaign_performance.csv", index=False)
print("✅ Exported fact_campaign_performance.csv")

