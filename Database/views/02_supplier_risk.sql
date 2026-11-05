-- Supplier Risk Analytics
-- Weighted supplier risk scoring model.

CREATE OR REPLACE VIEW analytics.v_supplier_risk AS

WITH supplier_metrics AS (
    SELECT
        supplier,
        COUNT(*) AS total_orders,

        COUNT(*) FILTER (
            WHERE order_status = 'Pending'
        ) AS pending_orders,

        COUNT(*) FILTER (
            WHERE order_status = 'Cancelled'
        ) AS cancelled_orders,

        ROUND(
            (100.0 * COUNT(*) FILTER (WHERE compliance = 'Yes')::numeric) /
            NULLIF(
                COUNT(*) FILTER (WHERE compliance IN ('Yes', 'No')),
                0
            )::numeric,
            2
        ) AS compliance_rate_pct,

        ROUND(
            (100.0 * SUM(defective_units) FILTER (
                WHERE defective_units IS NOT NULL
            )) /
            NULLIF(
                SUM(quantity) FILTER (
                    WHERE defective_units IS NOT NULL
                ),
                0
            )::numeric,
            2
        ) AS defect_rate_pct,

        COUNT(*) FILTER (
            WHERE data_quality_status = 'REVIEW_REQUIRED'
        ) AS review_required

    FROM staging.stg_purchase_orders
    GROUP BY supplier
),

risk_components AS (
    SELECT
        *,
        ROUND(100.0 - compliance_rate_pct, 2) AS compliance_risk,

        LEAST(
            100.0,
            ROUND((defect_rate_pct / 10.0) * 100, 2)
        ) AS defect_risk,

        ROUND(
            (100.0 * (pending_orders + cancelled_orders)::numeric) /
            NULLIF(total_orders, 0)::numeric,
            2
        ) AS operational_risk,

        ROUND(
            (100.0 * review_required::numeric) /
            NULLIF(total_orders, 0)::numeric,
            2
        ) AS data_quality_risk

    FROM supplier_metrics
),

scored_suppliers AS (
    SELECT
        *,
        ROUND(
            compliance_risk * 0.40 +
            defect_risk * 0.35 +
            operational_risk * 0.15 +
            data_quality_risk * 0.10,
            2
        ) AS supplier_risk_score
    FROM risk_components
)

SELECT
    supplier,
    total_orders,
    pending_orders,
    cancelled_orders,
    compliance_rate_pct,
    defect_rate_pct,
    review_required,
    compliance_risk,
    defect_risk,
    operational_risk,
    data_quality_risk,
    supplier_risk_score,

    CASE
        WHEN supplier_risk_score >= 70 THEN 'HIGH'
        WHEN supplier_risk_score >= 40 THEN 'MEDIUM'
        ELSE 'LOW'
    END AS risk_level

FROM scored_suppliers;
