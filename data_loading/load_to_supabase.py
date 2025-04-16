from supabase import create_client, Client
from dotenv import load_dotenv
import os
import pandas as pd
import time

# Load environment variables
load_dotenv()

print("Supabase URL:", os.getenv("SUPABASE_URL"))
print("Service Key starts with:", os.getenv("SUPABASE_SERVICE_KEY")[:10])

# Connect to Supabase
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(url, key)

# Load the cleaned dataset
df = pd.read_csv("data_cleaning/marketing_campaign_cleaned.csv")

# ---------------------------
# INSERT INTO dim_channel
# ---------------------------
channels = df['channel_used'].dropna().unique()

for channel in channels:
    response = supabase.table('dim_channel').upsert(
        {'channel_name': channel},
        on_conflict='channel_name'
    ).execute()
    print("Upserted into dim_channel:", response)

# ---------------------------
# INSERT INTO dim_location
# ---------------------------
locations = df['location'].dropna().unique()

for location in locations:
    city = location.strip()
    response = supabase.table('dim_location').upsert(
        {'city': city},
        on_conflict='city'
    ).execute()
    print("Upserted into dim_location:", response)

# ---------------------------
# INSERT INTO dim_audience
# ---------------------------

audiences = df[['target_audience', 'customer_segment']].dropna().drop_duplicates()

for _, row in audiences.iterrows():
    # Check if audience already exists
    existing = supabase.table('dim_audience').select('audience_id')\
        .eq('target_audience', row['target_audience'])\
        .eq('customer_segment', row['customer_segment']).execute()

    if existing.data:
        continue  # Skip if already exists

    # Insert new audience
    response = supabase.table('dim_audience').insert({
        'target_audience': row['target_audience'],
        'customer_segment': row['customer_segment']
    }).execute()
    print("Inserted into dim_audience:", response)


# ---------------------------
# INSERT INTO dim_campaign_type
# ---------------------------

dim_campaign_type = (
    df[['campaign_type']]
    .drop_duplicates()
    .dropna()
    .reset_index(drop=True)
    .copy()
)
dim_campaign_type['campaign_type_id'] = dim_campaign_type.index + 1
dim_campaign_type = dim_campaign_type[['campaign_type_id', 'campaign_type']]

records = dim_campaign_type.to_dict(orient='records')

response = supabase.table("dim_campaign_type").insert(records).execute()






