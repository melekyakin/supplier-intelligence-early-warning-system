-- Performance indexes for procurement analytics.

CREATE INDEX IF NOT EXISTS idx_raw_purchase_orders_po_id
    ON raw.raw_purchase_orders (po_id);

CREATE INDEX IF NOT EXISTS idx_raw_purchase_orders_supplier
    ON raw.raw_purchase_orders (supplier);

CREATE INDEX IF NOT EXISTS idx_stg_purchase_orders_supplier
    ON staging.stg_purchase_orders (supplier);

CREATE INDEX IF NOT EXISTS idx_stg_purchase_orders_order_date
    ON staging.stg_purchase_orders (order_date);

CREATE INDEX IF NOT EXISTS idx_stg_purchase_orders_quality_status
    ON staging.stg_purchase_orders (data_quality_status);

CREATE INDEX IF NOT EXISTS idx_alert_notification_log_alert_date
    ON analytics.alert_notification_log (alert_date);
