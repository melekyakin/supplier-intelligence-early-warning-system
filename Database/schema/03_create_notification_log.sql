-- Alert notification history
-- Stores sent supplier alerts and prevents duplicate daily notifications.

-- 1. Create sequence first
CREATE SEQUENCE IF NOT EXISTS analytics.alert_notification_log_notification_id_seq;

-- 2. Create notification log table
CREATE TABLE IF NOT EXISTS analytics.alert_notification_log (
    notification_id BIGINT NOT NULL
        DEFAULT nextval('analytics.alert_notification_log_notification_id_seq'::regclass),
    alert_date DATE NOT NULL DEFAULT CURRENT_DATE,
    supplier TEXT NOT NULL,
    alert_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    metric_value NUMERIC,
    alert_message TEXT,
    sent_at TIMESTAMPTZ,
    CONSTRAINT alert_notification_log_pkey
        PRIMARY KEY (notification_id),
    CONSTRAINT alert_notification_log_alert_date_supplier_alert_type_key
        UNIQUE (alert_date, supplier, alert_type)
);

-- 3. Link sequence ownership to notification_id
ALTER SEQUENCE analytics.alert_notification_log_notification_id_seq
    OWNED BY analytics.alert_notification_log.notification_id;
