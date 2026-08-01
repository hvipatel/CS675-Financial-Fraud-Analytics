ALTER TABLE credit_card_transactions
SET TBLPROPERTIES (
    'use.null.for.invalid.data' = 'true'
);



SELECT
    CAST(t.zip_code AS INTEGER) AS zip_code,
    COUNT(*) AS fraud_transactions,
    ROUND(
        SUM(
            CAST(
                REPLACE(REPLACE(t.amount, '$', ''), ',', '')
                AS DOUBLE
            )
        ),
        2
    ) AS fraud_amount,
    MAX(z.latitude) AS latitude,
    MAX(z.longitude) AS longitude
FROM credit_card_transactions AS t
LEFT JOIN zcta_lookup AS z
    ON LPAD(
        CAST(CAST(t.zip_code AS INTEGER) AS VARCHAR),
        5,
        '0'
    ) = z.geoid
WHERE t.is_fraud = 'Yes'
  AND t.zip_code IS NOT NULL
GROUP BY CAST(t.zip_code AS INTEGER)
ORDER BY fraud_transactions DESC
LIMIT 20;
