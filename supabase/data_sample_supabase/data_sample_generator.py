from supabase import create_client, Client
from dotenv import load_dotenv
import os
import pandas as pd

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(url, key)

# Folder to store the sample CSVs
output_dir = "data_sample_supabase"
os.makedirs(output_dir, exist_ok=True)

# Helper function to export samples
def export_sample_csv(table_name, limit=10):
    response = supabase.table(table_name).select("*").limit(limit).execute()
    df = pd.DataFrame(response.data)
    csv_path = os.path.join(output_dir, f"{table_name}_sample.csv")
    df.to_csv(csv_path, index=False)
    print(f"✅ Exported {csv_path}")

# Tables to sample
tables = [
    "dim_campaign_type",
    "dim_channel",
    "dim_location",
    "dim_audience",
    "fact_campaign_performance"
]

# Export each table
for table in tables:
    export_sample_csv(table)
