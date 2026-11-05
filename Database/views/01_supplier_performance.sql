-- Supplier Performance Analytics
-- Aggregated procurement KPIs by supplier.

CREATE OR REPLACE VIEW analytics.v_supplier_performance AS
SELECT
    supplier,
    COUNT(*) AS total_orders,

    COUNT(*) FILTER (
        WHERE order_status = 'Delivered'
    ) AS delivered_orders,

    COUNT(*) FILTER (
        WHERE order_status = 'Partially Delivered'
    ) AS partially_delivered_orders,

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

    ROUND(
        AVG(delivery_date - order_date) FILTER (
            WHERE order_status IN ('Delivered', 'Partially Delivered')
              AND delivery_date >= order_date
        ),
        2
    ) AS avg_delivery_lead_time_days,

    ROUND(
        SUM(
            (unit_price - negotiated_price) * quantity::numeric
        ),
        2
    ) AS estimated_savings

FROM staging.stg_purchase_orders
GROUP BY supplier;
