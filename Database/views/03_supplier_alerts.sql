-- Supplier Alert Rules
-- Identifies suppliers requiring operational or quality review.

CREATE OR REPLACE VIEW analytics.v_supplier_alerts AS

SELECT
    supplier,
    'HIGH_SUPPLIER_RISK'::text AS alert_type,
    'CRITICAL'::text AS severity,
    supplier_risk_score AS metric_value,
    'Supplier risk score reached critical threshold'::text AS alert_message
FROM analytics.v_supplier_risk
WHERE supplier_risk_score >= 70

UNION ALL

SELECT
    supplier,
    'MEDIUM_SUPPLIER_RISK'::text,
    'WARNING'::text,
    supplier_risk_score,
    'Supplier requires risk review'::text
FROM analytics.v_supplier_risk
WHERE supplier_risk_score >= 40
  AND supplier_risk_score < 70

UNION ALL

SELECT
    supplier,
    'LOW_COMPLIANCE'::text,
    'WARNING'::text,
    compliance_rate_pct,
    'Compliance rate is below 80 percent'::text
FROM analytics.v_supplier_performance
WHERE compliance_rate_pct < 80

UNION ALL

SELECT
    supplier,
    'HIGH_DEFECT_RATE'::text,
    'WARNING'::text,
    defect_rate_pct,
    'Defect rate reached 8 percent or higher'::text
FROM analytics.v_supplier_performance
WHERE defect_rate_pct >= 8

UNION ALL

SELECT
    supplier,
    'DATA_QUALITY_ISSUE'::text,
    'WARNING'::text,
    data_quality_risk,
    'Data quality review rate reached 25 percent or higher'::text
FROM analytics.v_supplier_risk
WHERE data_quality_risk >= 25;
