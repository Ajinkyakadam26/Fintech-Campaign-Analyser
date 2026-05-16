
-- NovaPay Campaign Analytics - SQL Queries
-- Tool: DuckDB | Dataset: campaigns.csv


-- Total Spend, Revenue & ROAS by Channel

SELECT
    channel,
    ROUND(SUM(spend), 2)                        AS total_spend,
    ROUND(SUM(revenue), 2)                      AS total_revenue,
    ROUND(SUM(revenue) / SUM(spend), 2)         AS ROAS,
    SUM(conversions)                             AS total_conversions
FROM campaigns
GROUP BY channel
ORDER BY ROAS DESC;


-- Cost Per Lead (CPL) by Channel & Region

SELECT
    channel,
    region,
    ROUND(SUM(spend) / SUM(leads), 2)           AS CPL,
    SUM(leads)                                   AS total_leads,
    ROUND(SUM(spend), 2)                        AS total_spend
FROM campaigns
GROUP BY channel, region
ORDER BY CPL ASC;


-- MQL Volume & MQL Rate by Month

SELECT
    STRFTIME('%Y-%m', date)                      AS month,
    SUM(MQLs)                                    AS total_MQLs,
    SUM(leads)                                   AS total_leads,
    ROUND(SUM(MQLs) * 100.0 / SUM(leads), 2)   AS MQL_Rate_Pct
FROM campaigns
GROUP BY month
ORDER BY month ASC;


-- Top 10 Campaigns by ROAS

SELECT
    campaign_id,
    campaign_name,
    channel,
    region,
    ROUND(SUM(spend), 2)                        AS total_spend,
    ROUND(SUM(revenue), 2)                      AS total_revenue,
    ROUND(SUM(revenue) / SUM(spend), 2)         AS ROAS,
    SUM(conversions)                             AS total_conversions
FROM campaigns
GROUP BY campaign_id, campaign_name, channel, region
ORDER BY ROAS DESC
LIMIT 10;


-- Funnel Drop-off Analysis

SELECT
    SUM(impressions)                                            AS impressions,
    SUM(clicks)                                                 AS clicks,
    SUM(leads)                                                  AS leads,
    SUM(MQLs)                                                   AS MQLs,
    SUM(SQLs)                                                   AS SQLs,
    SUM(conversions)                                            AS conversions,
    ROUND(SUM(clicks) * 100.0 / SUM(impressions), 2)          AS CTR_Pct,
    ROUND(SUM(leads) * 100.0 / SUM(clicks), 2)                AS Click_to_Lead_Pct,
    ROUND(SUM(MQLs) * 100.0 / SUM(leads), 2)                  AS Lead_to_MQL_Pct,
    ROUND(SUM(SQLs) * 100.0 / SUM(MQLs), 2)                   AS MQL_to_SQL_Pct,
    ROUND(SUM(conversions) * 100.0 / SUM(SQLs), 2)            AS SQL_to_Conv_Pct
FROM campaigns;


-- Month-over-Month CPL & ROAS Change

WITH monthly AS (
    SELECT
        STRFTIME('%Y-%m', date)                          AS month,
        ROUND(SUM(spend) / SUM(leads), 2)               AS CPL,
        ROUND(SUM(revenue) / SUM(spend), 2)             AS ROAS,
        SUM(MQLs)                                        AS MQLs
    FROM campaigns
    GROUP BY month
)
SELECT
    month,
    CPL,
    ROAS,
    MQLs,
    ROUND(CPL - LAG(CPL) OVER (ORDER BY month), 2)      AS CPL_MoM_Change,
    ROUND(ROAS - LAG(ROAS) OVER (ORDER BY month), 2)    AS ROAS_MoM_Change,
    MQLs - LAG(MQLs) OVER (ORDER BY month)              AS MQL_MoM_Change
FROM monthly
ORDER BY month ASC;


-- Region x Channel Performance Matrix

SELECT
    region,
    channel,
    ROUND(SUM(spend), 2)                        AS total_spend,
    ROUND(SUM(revenue), 2)                      AS total_revenue,
    ROUND(SUM(revenue) / SUM(spend), 2)         AS ROAS,
    ROUND(SUM(spend) / SUM(leads), 2)           AS CPL,
    SUM(MQLs)                                    AS total_MQLs
FROM campaigns
GROUP BY region, channel
ORDER BY region, ROAS DESC;
