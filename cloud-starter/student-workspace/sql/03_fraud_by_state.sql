SELECT
    merchant_state,
    COUNT(*) AS fraud_transactions,
    ROUND(
        SUM(
            CAST(
                REPLACE(REPLACE(amount, '$', ''), ',', '')
                AS DOUBLE
            )
        ),
        2
    ) AS fraud_amount
FROM credit_card_transactions
WHERE is_fraud = 'Yes'
  AND merchant_state IS NOT NULL
  AND LENGTH(TRIM(merchant_state)) = 2
GROUP BY merchant_state
ORDER BY fraud_transactions DESC
LIMIT 20;
