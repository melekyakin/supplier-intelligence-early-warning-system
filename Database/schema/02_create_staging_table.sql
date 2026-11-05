-- Staging procurement data
-- Typed and quality-checked procurement records.

CREATE TABLE IF NOT EXISTS staging.stg_purchase_orders (
    po_id TEXT,
    supplier TEXT,
    order_date DATE,
    delivery_date DATE,
    item_category TEXT,
    order_status TEXT,
    quantity INTEGER,
    unit_price NUMERIC,
    negotiated_price NUMERIC,
    defective_units NUMERIC,
    compliance TEXT,
    data_quality_issue TEXT,
    data_quality_status TEXT,
    loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
