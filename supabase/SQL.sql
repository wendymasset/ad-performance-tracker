CREATE TABLE public.dim_channel (
  channel_id SERIAL PRIMARY KEY,
  channel_name TEXT UNIQUE NOT NULL
);

CREATE TABLE public.dim_location (
  location_id SERIAL PRIMARY KEY,
  city TEXT,
  country TEXT,
  region TEXT
);

CREATE TABLE public.dim_audience (
  audience_id SERIAL PRIMARY KEY,
  target_audience TEXT,
  customer_segment TEXT
);



CREATE TABLE IF NOT EXISTS public.dim_campaign_type (
    campaign_type_id INT PRIMARY KEY,
    campaign_type TEXT UNIQUE NOT NULL
);



CREATE TABLE dim_campaign (
    campaign_id TEXT PRIMARY KEY,
    company TEXT,
    campaign_type TEXT,
    duration TEXT,
    language TEXT
);

CREATE TABLE IF NOT EXISTS public.fact_campaign_performance (
    campaign_id TEXT PRIMARY KEY,
    campaign_type_id INT REFERENCES dim_campaign_type(campaign_type_id),
    channel_id INT REFERENCES dim_channel(channel_id),
    location_id INT REFERENCES dim_location(location_id),
    audience_id INT REFERENCES dim_audience(audience_id),
    duration INT,
    impressions INT,
    clicks INT,
    acquisition_cost NUMERIC,
    conversion_rate NUMERIC,
    ctr NUMERIC,
    cpc NUMERIC,
    roas NUMERIC
);
