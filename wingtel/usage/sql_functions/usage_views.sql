DROP VIEW IF EXISTS usage_records_view;
CREATE OR REPLACE VIEW usage_records_view AS
    SELECT 
        ROW_NUMBER() OVER() AS id, 
        subscription_id,
        type_of_usage,
        price,
        usage_date,
        used
    FROM (
            SELECT subscription_id_id AS subscription_id,
                    'data' AS type_of_usage,
                    SUM(price) AS price,
                    SUM(kilobytes_used) AS used,
                    DATE_TRUNC('day', usage_date)::DATE AS usage_date
            FROM usage_datausagerecord
            GROUP BY DATE_TRUNC('day', usage_date), subscription_id_id

            UNION
            SELECT subscription_id_id AS subscription_id,
                    'voice' AS type_of_usage,
                    SUM(price) AS price,
                    SUM(seconds_used) AS used,
                    DATE_TRUNC('day', usage_date)::DATE AS usage_date
            FROM usage_voiceusagerecord
            GROUP BY DATE_TRUNC('day', usage_date), subscription_id_id
        ) AS t;
