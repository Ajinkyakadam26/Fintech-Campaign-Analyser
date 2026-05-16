import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Reproducible results
np.random.seed(42)
random.seed(42)

# Config
NUM_ROWS = 500000
START_DATE = datetime(2026, 1, 1)
END_DATE = datetime(2026, 6, 30)

channels = ['Google Ads', 'Meta', 'Email', 'Referral', 'Organic']
regions = ['North', 'South', 'East', 'West', 'International']
campaign_names = [
    'NovaPay Launch Q1', 'Referral Boost Jan', 'Meta Spring Sale',
    'Google Brand Awareness', 'Email Reactivation', 'BNPL Push Feb',
    'Organic SEO Mar', 'Meta Retargeting', 'Google Performance Max',
    'Referral Elite Apr', 'Email Nurture May', 'NovaPay Anniversary',
    'South Region Blitz', 'North Expansion', 'International Push'
]

# Generate dates
date_range = (END_DATE - START_DATE).days
dates = [START_DATE + timedelta(days=random.randint(0, date_range))
         for _ in range(NUM_ROWS)]

# Generate base data
df = pd.DataFrame({
    'campaign_id': [f'CMP{str(i).zfill(4)}' for i in np.random.randint(1, 200, NUM_ROWS)],
    'campaign_name': np.random.choice(campaign_names, NUM_ROWS),
    'channel': np.random.choice(channels, NUM_ROWS, p=[0.30, 0.25, 0.20, 0.15, 0.10]),
    'region': np.random.choice(regions, NUM_ROWS, p=[0.25, 0.25, 0.20, 0.20, 0.10]),
    'date': dates,
})

# Realistic impressions by channel
channel_impressions = {
    'Google Ads': (5000, 50000),
    'Meta': (8000, 60000),
    'Email': (2000, 15000),
    'Referral': (500, 5000),
    'Organic': (1000, 20000)
}

impressions = []
for ch in df['channel']:
    low, high = channel_impressions[ch]
    impressions.append(np.random.randint(low, high))
df['impressions'] = impressions

# Realistic CTR by channel
channel_ctr = {
    'Google Ads': 0.045,
    'Meta': 0.038,
    'Email': 0.12,
    'Referral': 0.08,
    'Organic': 0.055
}

df['clicks'] = (df.apply(
    lambda r: int(r['impressions'] * np.random.normal(channel_ctr[r['channel']], 0.01)),
    axis=1)).clip(lower=1)

# Funnel conversion rates
df['leads'] = (df['clicks'] * np.random.uniform(0.10, 0.30, NUM_ROWS)).astype(int).clip(lower=1)
df['MQLs'] = (df['leads'] * np.random.uniform(0.20, 0.45, NUM_ROWS)).astype(int).clip(lower=0)
df['SQLs'] = (df['MQLs'] * np.random.uniform(0.30, 0.55, NUM_ROWS)).astype(int).clip(lower=0)
df['conversions'] = (df['SQLs'] * np.random.uniform(0.20, 0.40, NUM_ROWS)).astype(int).clip(lower=0)

# Spend and revenue
channel_cpl = {
    'Google Ads': (80, 200),
    'Meta': (60, 160),
    'Email': (10, 40),
    'Referral': (20, 80),
    'Organic': (5, 30)
}

spend = []
for idx, row in df.iterrows():
    low, high = channel_cpl[row['channel']]
    cpl = np.random.uniform(low, high)
    spend.append(round(cpl * row['leads'], 2))
df['spend'] = spend

df['revenue'] = (df['conversions'] * np.random.uniform(800, 3000, NUM_ROWS)).round(2)

# Derived metrics
df['CTR'] = (df['clicks'] / df['impressions']).round(4)
df['CPL'] = (df['spend'] / df['leads'].clip(lower=1)).round(2)
df['CPA'] = (df['spend'] / df['conversions'].clip(lower=1)).round(2)
df['ROAS'] = (df['revenue'] / df['spend'].clip(lower=0.01)).round(2)
df['MQL_Rate'] = (df['MQLs'] / df['leads'].clip(lower=1)).round(4)
df['Conversion_Rate'] = (df['conversions'] / df['leads'].clip(lower=1)).round(4)

# Sort by date
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

# Save
df.to_csv('data/campaigns.csv', index=False)
print(f"✅ Dataset generated: {len(df):,} rows")
print(f"📊 Columns: {list(df.columns)}")
print(df.head(3))
