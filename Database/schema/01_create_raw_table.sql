-- Raw procurement data
-- Source CSV values are stored as TEXT to preserve original input.

CREATE TABLE IF NOT EXISTS raw.raw_purchase_orders (
    po_id TEXT,
    supplier TEXT,
    order_date TEXT,
    delivery_date TEXT,
    item_category TEXT,
    order_status TEXT,
    quantity TEXT,
    unit_price TEXT,
    negotiated_price TEXT,
    defective_units TEXT,
    compliance TEXT,
    loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
