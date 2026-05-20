# 💳 NovaPay — Fintech Campaign Analytics

## 🔴 Live Demo
| Platform | Link |
|---|---|
| 🚀 Streamlit App | [fintech-campaign-analyser.streamlit.app](https://fintech-campaign-analyser.streamlit.app) |
| 📊 Tableau Dashboard | [View on Tableau Public](https://public.tableau.com/app/profile/ajinkya.kadam/viz/NovaPay-CampaignPerformanceAnalyticsDashboard/CampaignAnalysis) |

---

## 📌 Project Overview
End-to-end campaign performance analytics tool for a 
fictional fintech company **NovaPay** — simulating real 
marketing analytics workflows used at Razorpay, PhonePe 
and CRED.

Built to demonstrate senior-level data analytics skills 
across Python, SQL, Streamlit and Tableau.

---

## 🎯 Key Metrics Tracked
- **MQL Rate** — Marketing Qualified Lead conversion
- **CPL** — Cost Per Lead by channel and region
- **ROAS** — Return on Ad Spend
- **Funnel Drop-off** — Impressions → Conversions
- **MoM Trends** — Month-over-Month performance
- **Regional Performance** — 5 regions × 5 channels

---

## 🛠️ Tech Stack
| Tool | Purpose |
|---|---|
| Python (Pandas, NumPy) | Synthetic data generation |
| SQL (DuckDB) | Data querying and analysis |
| Streamlit | Interactive web application |
| Plotly | Charts and visualizations |
| Tableau + Figma | Executive BI dashboard |
| GitHub | Version control |

---

## 📁 Project Structure
fintech-campaign-analyser/
├── data/
│   └── generate_data.py
├── app/
│   ├── app.py
│   └── utils.py
├── sql/
│   └── queries.sql
├── tableau/
│   └── dashboard_link.md
└── requirements.txt

---

## 📊 Dataset
- **500,000 rows** of synthetic campaign data
- **Jan 2026 – Jun 2026** (6 months)
- **5 channels** — Google Ads, Meta, Email, Referral, Organic
- **5 regions** — North, South, East, West, International
- **19 columns** — including CTR, CPL, CPA, ROAS, MQL Rate

To regenerate the dataset:
python data/generate_data.py

Run Locally
# Clone the repo
git clone https://github.com/Ajinkyakadam26/Fintech-Campaign-Analyser.git

# Install dependencies
pip install -r requirements.txt

# Generate dataset
python data/generate_data.py

# Run the app
streamlit run app/app.py

## 📱 Streamlit App Features
- 5 KPI summary cards — Total Spend, Revenue, ROAS, MQLs, CPL
- Campaign conversion funnel with drop-off % at each stage
- Month-over-Month trend lines with parameter toggle
- ROAS by channel bar chart
- Region × Channel ROAS heatmap
- Top 10 campaigns by ROAS table

---

## 📊 Tableau Dashboard Features
- MoM % change indicators on all KPI cards
- Interactive filters — Date, Channel, Region, Campaign
- Campaign conversion funnel — Clicks to Conversions
- Region × Channel performance heatmap (red-green)
- Cost Per Lead by Region with ₹100 target benchmark
- Deep Dive channel summary table
- Dark theme designed in Figma + built in Tableau Desktop
